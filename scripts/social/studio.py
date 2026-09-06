"""Export an offline-capable workspace containing public article data only."""
import json
import os
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from .content import PLATFORMS, caption
from .providers import automatic_platforms


def export_studio(root, out, articles, config, state=None, preview=False, env=os.environ):
    folder = out / "social-studio"
    folder.mkdir(parents=True, exist_ok=True)
    for source in (root / "social/studio").iterdir():
        if source.is_file():
            shutil.copy2(source, folder / source.name)
    platforms = automatic_platforms(env)
    enabled = env.get("SOCIAL_PUBLISH_ENABLED") == "true" and not preview
    repository = env.get("GITHUB_REPOSITORY") or "Axis-koji/robu-travel-journal"
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("リポジトリ名が不正です")
    items = []
    for a in sorted(articles, key=lambda a: (a.get("published", ""), a["id"]), reverse=True):
        # Explicit allowlist: never serialize tokens, env, arbitrary config or local paths.
        items.append({**{k: a[k] for k in ("id", "title", "description", "url", "published", "ai_image")},
                      "image": "../assets/social/" + a["id"] + "/instagram.jpg",
                      "pin": "../assets/social/" + a["id"] + "/pinterest.jpg",
                      "video": "../assets/social/" + a["id"] + "/tiktok.mp4",
                      "posts": {p: caption(a, p) for p in PLATFORMS}})
    data = {"version": 2, "site_name": config["site_name"], "site_url": config["site_url"],
            "repository": repository, "generated_at": datetime.now(timezone.utc).isoformat(),
            "preview": preview, "automatic": platforms, "enabled": enabled,
            "state": public_state(state or {}), "articles": items}
    encoded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    (folder / "data.js").write_text("window.ROBU_SOCIAL_MANIFEST = " + encoded + ";\n", encoding="utf-8")
    # Portable app works after extraction with a double-click; no local server needed.
    with zipfile.ZipFile(out / "social-posting-app.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for source in folder.iterdir():
            if source.is_file():
                archive.write(source, source.relative_to(out))
        for a in items:
            for key in ("image", "pin", "video"):
                source = (folder / a[key]).resolve()
                archive.write(source, source.relative_to(out.resolve()))
    return data


def public_state(state):
    statuses = {"published", "accepted", "submitting", "uncertain", "rejected", "manual_done"}
    return {"posts": {k: {"status": v["status"], "attempted_at": v.get("attempted_at", "")}
                      for k, v in state.get("posts", {}).items() if v.get("status") in statuses},
            "channels": {k: {"excluded": v.get("excluded", [])}
                         for k, v in state.get("channels", {}).items() if k in PLATFORMS}}
