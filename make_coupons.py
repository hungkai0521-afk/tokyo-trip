#!/usr/bin/env python3
"""Generate coupons.html for the Tokyo trip site: Japan shopping coupons relevant
to this itinerary (上野/御徒町 base + Day 4 秋葉原 3C). Each card embeds an offline
QR (segno, data-URI) that opens the store's official coupon page, plus a tap link.
No dates/PII — safe for the public site."""
import io, base64, segno, html

COUPONS = [
 {"emoji":"🏬","name":"多慶屋 Takeya","area":"御徒町(就在你飯店旁)",
  "disc":"免稅 10% ＋ 額外 5~7%","detail":"滿 ¥5,000→5%、滿 ¥30,000→7%(折扣上限 ¥10,000)",
  "howto":"結帳出示優惠畫面 ＋ 護照","valid":"約至 2027/4/30",
  "url":"https://www.takeya.co.jp/"},
 {"emoji":"📷","name":"Bic Camera / Sofmap","area":"秋葉原(Day 4 採購)",
  "disc":"免稅 10% ＋ 最高 7%","detail":"相機/家電/手錶 7%、藥妝 5%、酒 3%;Apple・遊戲機・名牌錶等僅免稅不折扣",
  "howto":"出示券 ＋ 護照(須辦免稅)","valid":"券會定期更新,以官方頁為準",
  "url":"https://www.biccamera.com/bc/c/inbound/"},
 {"emoji":"🐧","name":"唐吉訶德 Don Quijote","area":"到處有(Day 4 / 宵夜補貨)",
  "disc":"免稅 10% ＋ 最高 7%","detail":"滿 ¥10,000(未稅)再 +5%;電子券即時可用",
  "howto":"出示電子券 ＋ 護照","valid":"電子券,以官方頁為準",
  "url":"https://japanportal.donki-global.com/coupon/"},
 {"emoji":"💊","name":"松本清 Matsumoto Kiyoshi","area":"藥妝,到處有",
  "disc":"免稅 ＋ 折扣券","detail":"美妝/藥品折扣;部分限 app 會員",
  "howto":"出示券 ＋ 護照","valid":"以官方頁為準",
  "url":"https://www.matsukiyo.co.jp/"},
 {"emoji":"🛍️","name":"Laox","area":"免稅電器 / 伴手禮",
  "disc":"免稅 10% ＋ 8%","detail":"手機出示券給店員掃描即可",
  "howto":"出示券 ＋ 護照","valid":"以官方頁為準",
  "url":"https://www.laox.co.jp/"},
 {"emoji":"🔌","name":"Yodobashi 友都八喜","area":"秋葉原(Day 4)",
  "disc":"⚠️ 通常只有免稅 10%","detail":"多半沒有額外 % 折扣券,別空等;主打齊全與集點",
  "howto":"結帳辦免稅 ＋ 護照","valid":"—",
  "url":"https://www.yodobashi.com/"},
]

def qr_datauri(url):
    q = segno.make(url, error='m')
    b = io.BytesIO(); q.save(b, kind='png', scale=4, border=2, dark='#7c2d12', light='#ffffff')
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def esc(s): return html.escape(str(s), quote=True)

cards = []
for c in COUPONS:
    cards.append(f'''<div class="cp">
  <div class="cp-h"><span class="cp-emoji">{c["emoji"]}</span>
    <div><div class="cp-name">{esc(c["name"])}</div><div class="cp-area">📍 {esc(c["area"])}</div></div>
    <span class="cp-disc">{esc(c["disc"])}</span></div>
  <div class="cp-body">
    <div class="cp-info">
      <p class="cp-detail">{esc(c["detail"])}</p>
      <div class="cp-meta"><span>🧾 {esc(c["howto"])}</span><span>🗓️ {esc(c["valid"])}</span></div>
      <a class="cp-link" href="{esc(c["url"])}" target="_blank" rel="noopener">開啟官方券頁 ↗</a>
    </div>
    <div class="cp-qr"><img src="{qr_datauri(c["url"])}" alt="{esc(c["name"])} 官方券頁 QR" width="112" height="112"><span>掃我開券頁</span></div>
  </div>
</div>''')

page = f'''<!DOCTYPE html>
<html lang="zh-TW"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#7c2d12"><title>日本購物優惠券 · 東京行</title>
<style>
:root{{--maple:#c2410c;--maple-deep:#7c2d12;--ginkgo:#d97706;--gold:#f59e0b;--ink:#292018;--muted:#8a7a6d;--bg:#faf6f0;--card:#fff;--line:#eee3d6}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,system-ui,"Noto Sans TC",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7}}
.wrap{{max-width:760px;margin:0 auto;padding:0 18px 40px}}
.hero{{background:linear-gradient(160deg,#431407,#7c2d12 55%,#9a3412);color:#fff7ed;text-align:center;padding:calc(env(safe-area-inset-top) + 40px) 20px 34px;margin-bottom:18px}}
.hero h1{{font-size:1.6rem;font-weight:900;letter-spacing:1px}}
.hero p{{font-size:.85rem;opacity:.9;margin-top:6px}}
.back{{display:inline-block;margin:16px 0 4px;color:var(--maple);font-weight:800;text-decoration:none;font-size:.9rem}}
.note{{background:#fffaf2;border:1.5px solid #ecc894;border-radius:14px;padding:12px 15px;font-size:.85rem;color:var(--maple-deep);margin-bottom:16px}}
.cp{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 17px;margin-bottom:14px;box-shadow:0 5px 18px -14px rgba(124,45,18,.3)}}
.cp-h{{display:flex;align-items:center;gap:11px;flex-wrap:wrap}}
.cp-emoji{{font-size:1.7rem;flex:none}}
.cp-name{{font-weight:900;font-size:1.05rem}}
.cp-area{{font-size:.76rem;color:var(--muted);font-weight:700}}
.cp-disc{{margin-left:auto;background:linear-gradient(140deg,var(--gold),var(--maple));color:#fff;font-weight:900;font-size:.82rem;border-radius:20px;padding:5px 13px;white-space:nowrap}}
.cp-body{{display:flex;gap:14px;align-items:center;margin-top:12px}}
.cp-info{{flex:1;min-width:0}}
.cp-detail{{font-size:.86rem;color:#4b3f35}}
.cp-meta{{display:flex;flex-wrap:wrap;gap:6px;margin:9px 0 10px}}
.cp-meta span{{font-size:.72rem;font-weight:700;color:var(--muted);background:#faf4ea;border:1px solid var(--line);border-radius:20px;padding:3px 10px}}
.cp-link{{display:inline-block;font-size:.85rem;font-weight:900;color:#fff;background:linear-gradient(140deg,var(--ginkgo),var(--maple));border-radius:10px;padding:8px 14px;text-decoration:none}}
.cp-qr{{flex:none;text-align:center}}
.cp-qr img{{display:block;border:1px solid var(--line);border-radius:10px;background:#fff}}
.cp-qr span{{font-size:.68rem;color:var(--muted);font-weight:700;display:block;margin-top:3px}}
.foot{{text-align:center;color:var(--muted);font-size:.75rem;margin-top:22px;line-height:1.9}}
@media(max-width:400px){{.cp-body{{flex-direction:column;align-items:stretch}}.cp-qr{{align-self:center}}}}
</style></head><body>
<div class="hero"><h1>🎫 日本購物優惠券</h1><p>東京行 · 掃 QR 或點連結開官方券頁 · 結帳出示畫面＋護照</p></div>
<div class="wrap">
<a class="back" href="index.html">← 回行程</a>
<div class="note">⚠️ <b>共通規則</b>:多數優惠<b>須先辦免稅</b>(同店同日通常滿 ¥5,000)、<b>結帳出示手機畫面＋護照</b>。<b>Apple、遊戲機/軟體、名牌錶</b>等常僅免稅、不再打折。券內容與效期<b>以各店官方為準,出發前再確認</b>。<br>🧾 別忘了 <b>2026/11 起的退稅新制</b>是「先付後退」,出境在成田終端機刷護照退 10%。</div>
{chr(10).join(cards)}
<div class="foot">優惠僅供參考,實際折扣/排除品項以各店現場與官方公告為準 · Generated with Claude Code 🍁</div>
</div></body></html>'''

open("coupons.html","w",encoding="utf-8").write(page)
print(f"wrote coupons.html ({len(COUPONS)} 券, {len(page)} bytes)")
