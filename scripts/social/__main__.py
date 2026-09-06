import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from .content import PLATFORMS, caption, catalog
from .media import render
from .publish import Buffer, DeliveryError, Ledger, publish, resolve


def config_for(root):
    config = json.loads((root / "social/config.json").read_text())
    if set(config["platforms"]) != set(PLATFORMS):
        raise ValueError("platformsには指定された6つのSNSを設定してください")
    if not 1 <= config["max_articles_per_run"] <= 20:
        raise ValueError("max_articles_per_runは1〜20です")
    return config


def ledger_for(config):
    return Ledger(os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN"), config["site_url"])


def copy_site(root, out):
    excluded = {".git", ".github", ".openai", ".social", "scripts", "tests", "docs", "records", "social"}
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    for name in names:
        if not name or Path(name).parts[0] in excluded or name.endswith((".md", ".py", ".ps1")):
            continue
        source = root / name
        if source.is_symlink():
            raise ValueError(f"公開対象にシンボリックリンクがあります: {name}")
        if source.is_file():
            target = out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    (out / ".nojekyll").touch()


def main():
    parser = argparse.ArgumentParser(description="ブログ公開・6SNS自動投稿")
    parser.add_argument("command", choices=["catalog", "build", "initialize", "check", "publish", "resolve"])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("_site"))
    parser.add_argument("--plan", type=Path, default=Path("_social/plan.json"))
    parser.add_argument("--preview-article", help="プレビュー用。既存記事を1本指定（送信しません）")
    parser.add_argument("--ledger", action="store_true", help="GitHubの初期化済み投稿記録を使用")
    parser.add_argument("--key")
    parser.add_argument("--outcome", choices=["accepted", "retry"])
    parser.add_argument("--post-id", default="")
    args = parser.parse_args()
    root = args.root.resolve()
    config = config_for(root)
    if args.command == "catalog":
        print(json.dumps(catalog(root, config), ensure_ascii=False, indent=2))
    elif args.command == "initialize":
        articles = catalog(root, config)
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
        ledger_for(config).initialize([a["id"] for a in articles], head)
        print(f"{len(articles)}本の既存記事を対象外として初期化しました。SNSへの投稿はありません。")
    elif args.command == "check":
        token = os.environ.get("BUFFER_API_KEY")
        if not token and sys.stdin.isatty():
            import getpass
            token = getpass.getpass("Buffer API key（画面には表示されません）: ")
        client = Buffer(token)
        # IDs are shown only during an explicitly requested setup check.
        print(json.dumps(client.channels(), ensure_ascii=False, indent=2))
    elif args.command == "build":
        articles = catalog(root, config)
        if args.ledger:
            excluded = set(ledger_for(config).load()["excluded"])
        else:
            excluded = set(json.loads((root / "social/baseline.json").read_text())["excluded"])
        selected = [a for a in articles if a["id"] not in excluded or a["id"] == args.preview_article]
        if args.preview_article and not any(a["id"] == args.preview_article for a in articles):
            raise ValueError("プレビュー記事が存在しないか、下書き／未来日です")
        out = args.out.resolve()
        if out == root or root.is_relative_to(out):
            raise ValueError("出力先には専用サブフォルダを指定してください")
        out.mkdir(parents=True, exist_ok=True)
        copy_site(root, out)
        plan = [render(root, a, out, config) for a in selected]
        # Marker ties publishing to this exact deployed commit; prevents stale/manual sends.
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
        (out / "social-release.json").write_text(json.dumps({"commit": head}), encoding="utf-8")
        args.plan.parent.mkdir(parents=True, exist_ok=True)
        args.plan.write_text(json.dumps({"commit": head, "articles": plan}, ensure_ascii=False, indent=2), encoding="utf-8")
        previews = [{"article": a["id"], "posts": {p: caption(a, p) for p in PLATFORMS}} for a in plan]
        (args.plan.parent / "captions.json").write_text(json.dumps(previews, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{len(articles)}記事を検出、{len(plan)}記事分のSNS素材を用意しました。")
    elif args.command == "publish":
        import urllib.request
        plan = json.loads(args.plan.read_text())
        with urllib.request.urlopen(config["site_url"] + "/social-release.json", timeout=30) as response:
            release = json.load(response)
        if release.get("commit") != plan["commit"]:
            raise DeliveryError("公開済みのコミットと投稿対象が一致しません。送信を停止しました")
        publish(plan["articles"], config, ledger_for(config), Buffer(os.environ.get("BUFFER_API_KEY")))
    elif args.command == "resolve":
        if not args.key or not args.outcome:
            raise ValueError("--keyと--outcomeが必要です")
        resolve(ledger_for(config), args.key, args.outcome, args.post_id)


if __name__ == "__main__":
    try:
        main()
    except (DeliveryError, ValueError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Credentials and remote response bodies must never leak into public Actions logs.
        print(f"処理に失敗しました（{type(e).__name__}）。接続・設定・素材を確認してください。", file=sys.stderr)
        sys.exit(1)
