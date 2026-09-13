"""Build a compact, first-party landing page for Instagram visitors."""
from html import escape


def export_instagram_landing(out, articles, config, state=None, limit=24):
    posts = (state or {}).get("posts", {})

    def recency(item):
        post = posts.get(item["id"] + ":instagram", {})
        posted_at = post.get("attempted_at", "") if post.get("status") in {"published", "accepted", "uncertain"} else ""
        return (bool(posted_at), posted_at, item.get("published", ""), item["id"])

    ordered = sorted(articles, key=recency, reverse=True)[:limit]
    cards = []
    for article in ordered:
        cards.append(
            '<article class="card">'
            f'<a href="{escape(article["url"], quote=True)}">'
            f'<h2>{escape(article["title"])}</h2>'
            f'<p>{escape(article["description"])}</p>'
            '<span>記事を読む →</span></a></article>'
        )
    site = config["site_url"].rstrip("/")
    page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instagramで紹介した記事｜{escape(config["site_name"])}</title>
<meta name="description" content="Instagramで紹介した最新記事を、新しい順にまとめています。">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{site}/instagram/">
<style>
:root{{--ink:#102933;--sea:#0e6c78;--paper:#fffdf9;--line:#dfe7e6;--accent:#ef765c}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Yu Gothic",Meiryo,system-ui,sans-serif}}
header,main,footer{{width:min(760px,calc(100% - 32px));margin:auto}}header{{padding:52px 0 26px;border-bottom:1px solid var(--line)}}
.brand{{color:var(--sea);font-size:14px;font-weight:800;text-decoration:none}}h1{{margin:12px 0;font-size:clamp(30px,7vw,48px);line-height:1.25}}
.lead{{color:#536368;line-height:1.8}}main{{padding:24px 0 52px;display:grid;gap:14px}}.card{{background:#fff;border:1px solid var(--line);border-radius:14px}}
.card a{{display:block;padding:20px;color:inherit;text-decoration:none}}.card h2{{margin:0 0 8px;font-size:19px;line-height:1.55}}.card p{{margin:0 0 12px;color:#536368;line-height:1.7;font-size:14px}}
.card span{{color:var(--sea);font-weight:800}}.card a:hover,.card a:focus-visible{{outline:3px solid #9edbd7;outline-offset:2px;border-radius:14px}}
footer{{padding:22px 0 42px;border-top:1px solid var(--line);font-size:13px;color:#647276}}footer a{{color:var(--sea)}}
</style></head><body>
<header><a class="brand" href="/">{escape(config["site_name"])}</a><h1>Instagramで紹介した記事</h1><p class="lead">気になった投稿のタイトルを選ぶと、詳しい記事へ移動できます。</p></header>
<main>{''.join(cards)}</main>
<footer><a href="/">ブログのトップへ戻る</a><p>記事にはアフィリエイト広告を含む場合があります。</p></footer>
</body></html>'''
    target = out / "instagram" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    return target
