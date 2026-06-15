#!/usr/bin/env python
"""ツールサイト ジェネレータ (精査版)。

需要を 精査して 採用した ツールだけを 量産する。
低需要(IDE/Word/Google等で 代替可能)は 除外、高需要+独自性のあるものを 採用。

実行: python _generate.py
"""

import os
from pathlib import Path

BASE = Path(__file__).parent

SITE_URL = "https://patto-tool.com"  # 独自ドメイン (Xserverで取得済)
GA4_ID = "G-XXXXXXXXXX"  # Google Analytics 4 計測ID (デプロイ時に 設定)
ADSENSE_CLIENT = "ca-pub-XXXXXXXXXXXXXXXX"  # AdSense クライアントID (審査通過後に 設定)

PAGE_TPL = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}｜無料ツール・登録不要</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="SITE_URL/{slug}/">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">

<!-- OGP (Facebook・Slack・Discord 等) -->
<meta property="og:type" content="website">
<meta property="og:url" content="SITE_URL/{slug}/">
<meta property="og:title" content="{title}｜無料ツール・登録不要">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="SITE_URL/og.png">
<meta property="og:site_name" content="便利ツール">
<meta property="og:locale" content="ja_JP">

<!-- Twitter Card (X) -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}｜無料ツール・登録不要">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="SITE_URL/og.png">

<!-- 構造化データ (WebApplication) -->
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication","name":"{title}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"JPY"}},"description":"{desc}"}}
</script>

<link rel="stylesheet" href="../style.css">

<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA4_ID"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','GA4_ID');</script>

<!-- AdSense (審査通過後 有効化) -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ADSENSE_CLIENT" crossorigin="anonymous"></script>
</head>
<body>
<header class="site"><div class="wrap"><a class="logo" href="../">便利<span>ツール</span></a><nav><a href="../">ツール一覧</a></nav></div></header>

<main class="wrap">
  <h1>{icon} {title}</h1>
  <p class="lead">{desc}</p>

  <div class="tool">
{body}
    <p class="note">🔒 すべて ブラウザ内 処理。サーバーには 何も 送信されません。</p>
  </div>

  <!-- 記事内 広告 -->
  <ins class="adsbygoogle" style="display:block;text-align:center;margin:24px 0;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ADSENSE_CLIENT" data-ad-slot="0000000000"></ins>
  <script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>

  {extra}

  <!-- 関連 ツール (内部リンク 強化・回遊率UP) -->
  <h2>🔗 関連 ツール</h2>
  <div class="grid" id="relatedTools"></div>
</main>

<footer class="site"><div class="wrap">© 便利ツール — 無料・登録不要のオンラインツール集 ｜ <a href="../about/">サイト について</a> ｜ <a href="../privacy/">プライバシー</a></div></footer>

<!-- 関連 ツール 動的 挿入 -->
<script>
(function(){{
  const all = ALL_TOOLS_JSON;
  const cur = '{slug}';
  const others = all.filter(t => t.slug !== cur).sort(()=>Math.random()-0.5).slice(0, 4);
  const html = others.map(t => `<a class="card" href="../${{t.slug}}/"><div class="ico">${{t.icon}}</div><div class="ttl">${{t.title}}</div><div class="dsc">${{t.desc}}</div></a>`).join('');
  const el = document.getElementById('relatedTools');
  if (el) el.innerHTML = html;
}})();
</script>
{script}
</body>
</html>
"""

# (slug, icon, title, desc, body_html, script_js, faq_html)
TOOLS = []


# =========================================================================
# A. 開発者向け 高需要 (5)
# =========================================================================

# ---------- 1. JSON フォーマッタ ----------
TOOLS.append((
    "json-format", "🧩", "JSON フォーマッタ",
    "JSON を 整形（インデント）して 見やすく 表示。入力ミスの 検出にも。",
    """    <textarea id="in" class="in" placeholder="JSON を 貼り付けてください...例: {&quot;a&quot;:1}"></textarea>
    <div class="bar">
      <button type="button" class="btn primary" id="fmt">整形</button>
      <button type="button" class="btn ghost" id="mini">圧縮</button>
      <button type="button" class="btn ghost" id="copy">コピー</button>
      <button type="button" class="btn ghost" id="clear">クリア</button>
    </div>
    <textarea id="out" class="in" readonly placeholder="ここに 結果が 表示されます"></textarea>
    <p id="err" style="color:#c00;min-height:1.4em;"></p>
""",
    """
const $in = document.getElementById('in');
const $out = document.getElementById('out');
const $err = document.getElementById('err');
function go(indent) {
  $err.textContent = '';
  try {
    const obj = JSON.parse($in.value);
    $out.value = JSON.stringify(obj, null, indent);
  } catch (e) {
    $err.textContent = 'JSON エラー: ' + e.message;
    $out.value = '';
  }
}
document.getElementById('fmt').onclick = () => go(2);
document.getElementById('mini').onclick = () => go(0);
document.getElementById('clear').onclick = () => { $in.value=''; $out.value=''; $err.textContent=''; };
document.getElementById('copy').onclick = () => { if (!$out.value) return; navigator.clipboard.writeText($out.value); };
""",
    "<dt>JSON エラーの 場合は？</dt><dd>赤字で エラー位置が 表示されます。クォート・カンマ漏れを 確認してください。</dd>",
))


# ---------- 2. URL エンコード/デコード ----------
TOOLS.append((
    "url-encode", "🔗", "URL エンコード / デコード",
    "URL に 含められない 文字 (日本語・記号) を %XX 形式に 変換、その 逆も。",
    """    <textarea id="in" class="in" placeholder="エンコード/デコード する 文字列を 入力"></textarea>
    <div class="bar">
      <button type="button" class="btn primary" id="enc">エンコード</button>
      <button type="button" class="btn ghost" id="dec">デコード</button>
      <button type="button" class="btn ghost" id="copy">コピー</button>
      <button type="button" class="btn ghost" id="clear">クリア</button>
    </div>
    <textarea id="out" class="in" readonly></textarea>
""",
    """
const $in = document.getElementById('in');
const $out = document.getElementById('out');
document.getElementById('enc').onclick = () => $out.value = encodeURIComponent($in.value);
document.getElementById('dec').onclick = () => { try { $out.value = decodeURIComponent($in.value); } catch (e) { $out.value = 'エラー: ' + e.message; } };
document.getElementById('clear').onclick = () => { $in.value=''; $out.value=''; };
document.getElementById('copy').onclick = () => $out.value && navigator.clipboard.writeText($out.value);
""",
    "",
))


# ---------- 3. Unix タイム変換 ----------
TOOLS.append((
    "unixtime", "⏰", "Unix タイム ⇔ 日時 変換",
    "Unix タイムスタンプ（秒/ミリ秒）と JST 日時を 相互 変換。",
    """    <h2>Unix → 日時</h2>
    <input id="ts" class="in" placeholder="例: 1700000000" />
    <div class="bar"><button type="button" class="btn primary" id="t2d">変換</button></div>
    <div id="ts_out" class="num"></div>
    <h2>日時 → Unix</h2>
    <input id="dt" type="datetime-local" class="in" />
    <div class="bar"><button type="button" class="btn primary" id="d2t">変換</button></div>
    <div id="dt_out" class="num"></div>
    <div class="bar"><button type="button" class="btn ghost" id="now">今すぐ</button></div>
""",
    """
const fmt = (d) => d.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo', hour12: false });
document.getElementById('t2d').onclick = () => {
  let v = parseInt(document.getElementById('ts').value, 10);
  if (isNaN(v)) return;
  if (v < 1e12) v *= 1000;
  document.getElementById('ts_out').textContent = fmt(new Date(v));
};
document.getElementById('d2t').onclick = () => {
  const v = document.getElementById('dt').value;
  if (!v) return;
  const t = Math.floor(new Date(v).getTime() / 1000);
  document.getElementById('dt_out').textContent = t + ' (' + Math.floor(t * 1000) + 'ms)';
};
document.getElementById('now').onclick = () => {
  const now = Date.now();
  document.getElementById('ts').value = Math.floor(now / 1000);
  document.getElementById('dt').value = new Date(now - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
};
""",
    "",
))


# ---------- 4. ハッシュ生成 ----------
TOOLS.append((
    "hash", "🔐", "ハッシュ生成 (SHA-256)",
    "テキストの ハッシュ値を 計算。データ 改変チェックや パスワード 比較に。",
    """    <textarea id="in" class="in" placeholder="ハッシュ化 する テキスト"></textarea>
    <div class="bar">
      <button type="button" class="btn primary" id="calc">SHA-256</button>
      <button type="button" class="btn ghost" id="copy">コピー</button>
    </div>
    <textarea id="out" class="in" readonly></textarea>
""",
    """
const $in = document.getElementById('in');
const $out = document.getElementById('out');
document.getElementById('calc').onclick = async () => {
  const buf = new TextEncoder().encode($in.value);
  const hash = await crypto.subtle.digest('SHA-256', buf);
  $out.value = Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2,'0')).join('');
};
document.getElementById('copy').onclick = () => $out.value && navigator.clipboard.writeText($out.value);
""",
    "",
))


# ---------- 5. UUID 生成 ----------
TOOLS.append((
    "uuid", "🆔", "UUID v4 生成",
    "ランダムな UUID (Universally Unique Identifier) を 生成。",
    """    <div class="bar">
      <button type="button" class="btn primary" id="gen">生成</button>
      <button type="button" class="btn ghost" id="gen10">10個 生成</button>
      <button type="button" class="btn ghost" id="copy">コピー</button>
    </div>
    <textarea id="out" class="in" readonly style="height:200px"></textarea>
""",
    """
const $out = document.getElementById('out');
const make = () => crypto.randomUUID();
document.getElementById('gen').onclick = () => $out.value = make();
document.getElementById('gen10').onclick = () => $out.value = Array.from({length:10}, make).join('\\n');
document.getElementById('copy').onclick = () => $out.value && navigator.clipboard.writeText($out.value);
""",
    "",
))


# =========================================================================
# B. お金 / 計算 (高需要) (8)
# =========================================================================

# ---------- 6. 住宅ローン 月返済 ----------
TOOLS.append((
    "loan", "🏠", "住宅ローン 月返済 計算",
    "借入額・金利・年数を 入れると 元利均等の 月返済額と 総支払額を 計算。",
    """    <label>借入額 (万円):</label>
    <input id="p" class="in" type="number" value="3500" />
    <label>金利 (年率 %):</label>
    <input id="r" class="in" type="number" step="0.01" value="1.0" />
    <label>返済期間 (年):</label>
    <input id="y" class="in" type="number" value="35" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="monthly">¥0</div><div class="cap">月返済額</div></div>
      <div class="cell"><div class="num" id="total">¥0</div><div class="cap">総支払額</div></div>
      <div class="cell"><div class="num" id="interest">¥0</div><div class="cap">利息合計</div></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const p = (parseFloat(document.getElementById('p').value) || 0) * 10000;
  const r = (parseFloat(document.getElementById('r').value) || 0) / 100 / 12;
  const n = (parseInt(document.getElementById('y').value, 10) || 0) * 12;
  if (!p || !n) return;
  const m = r === 0 ? p / n : (p * r) / (1 - Math.pow(1 + r, -n));
  const tot = m * n;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('monthly').textContent = fmt(m);
  document.getElementById('total').textContent = fmt(tot);
  document.getElementById('interest').textContent = fmt(tot - p);
};
""",
    "",
))


# ---------- 7. ガソリン代 計算 ----------
TOOLS.append((
    "gas-cost", "⛽", "ガソリン代 計算",
    "走行距離・燃費・ガソリン単価から 費用を 算出。旅行費用 試算に。",
    """    <label>走行距離 (km):</label>
    <input id="km" class="in" type="number" value="500" />
    <label>燃費 (km/L):</label>
    <input id="kmpl" class="in" type="number" step="0.1" value="15" />
    <label>ガソリン単価 (円/L):</label>
    <input id="yen" class="in" type="number" value="175" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="liters">0</div><div class="cap">使用量 (L)</div></div>
      <div class="cell"><div class="num" id="cost">¥0</div><div class="cap">ガソリン代</div></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const km = parseFloat(document.getElementById('km').value) || 0;
  const kmpl = parseFloat(document.getElementById('kmpl').value) || 1;
  const yen = parseFloat(document.getElementById('yen').value) || 0;
  const l = km / kmpl;
  document.getElementById('liters').textContent = l.toFixed(1);
  document.getElementById('cost').textContent = '¥' + Math.round(l * yen).toLocaleString('ja-JP');
};
""",
    "",
))


# ---------- 8. 時給→年収 ----------
TOOLS.append((
    "hourly-yearly", "💴", "時給 → 月収・年収 換算",
    "時給と 1日労働時間・週日数で 月収・年収を 自動計算。",
    """    <label>時給 (円):</label>
    <input id="hourly" class="in" type="number" value="1200" />
    <label>1日 労働時間:</label>
    <input id="hours" class="in" type="number" step="0.5" value="8" />
    <label>週 労働日数:</label>
    <input id="days" class="in" type="number" value="5" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="daily">¥0</div><div class="cap">日給</div></div>
      <div class="cell"><div class="num" id="weekly">¥0</div><div class="cap">週収</div></div>
      <div class="cell"><div class="num" id="monthly">¥0</div><div class="cap">月収目安</div></div>
      <div class="cell"><div class="num" id="yearly">¥0</div><div class="cap">年収目安</div></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const h = parseFloat(document.getElementById('hourly').value) || 0;
  const hr = parseFloat(document.getElementById('hours').value) || 0;
  const d = parseFloat(document.getElementById('days').value) || 0;
  const daily = h * hr;
  const weekly = daily * d;
  const monthly = weekly * 52 / 12;
  const yearly = weekly * 52;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('daily').textContent = fmt(daily);
  document.getElementById('weekly').textContent = fmt(weekly);
  document.getElementById('monthly').textContent = fmt(monthly);
  document.getElementById('yearly').textContent = fmt(yearly);
};
""",
    "",
))


# ---------- 9. 偏差値 計算 ----------
TOOLS.append((
    "deviation", "📊", "偏差値 計算",
    "得点・平均・標準偏差から 偏差値を 計算。試験 結果 分析に。",
    """    <label>自分の得点:</label>
    <input id="score" class="in" type="number" value="70" />
    <label>平均点:</label>
    <input id="avg" class="in" type="number" value="60" />
    <label>標準偏差:</label>
    <input id="sd" class="in" type="number" value="10" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="t">0</div><div class="cap">偏差値</div></div>
      <div class="cell"><div class="num" id="rank">0</div><div class="cap">上位 (%)</div></div>
    </div>
""",
    """
function erf(x) { const a=0.3275911,p=[0.254829592,-0.284496736,1.421413741,-1.453152027,1.061405429]; const s=Math.sign(x); x=Math.abs(x); const t=1/(1+a*x); const y=1-(((((p[4]*t+p[3])*t)+p[2])*t+p[1])*t+p[0])*t*Math.exp(-x*x); return s*y; }
document.getElementById('calc').onclick = () => {
  const score = parseFloat(document.getElementById('score').value) || 0;
  const avg = parseFloat(document.getElementById('avg').value) || 0;
  const sd = parseFloat(document.getElementById('sd').value) || 1;
  const t = 50 + 10 * (score - avg) / sd;
  document.getElementById('t').textContent = t.toFixed(2);
  const z = (score - avg) / sd;
  const p = (1 - 0.5 * (1 + erf(z / Math.SQRT2))) * 100;
  document.getElementById('rank').textContent = p.toFixed(2) + '%';
};
""",
    "",
))


# ---------- 10. 割り勘 計算 [新規:高需要] ----------
TOOLS.append((
    "warikan", "🍻", "割り勘 計算 (幹事 補助付き)",
    "合計金額と 人数を 入力。端数 切り上げ・幹事 多めなど 柔軟に 対応。",
    """    <label>合計金額 (円):</label>
    <input id="total" class="in" type="number" value="36800" />
    <label>人数:</label>
    <input id="people" class="in" type="number" value="5" min="1" />
    <label>幹事 多め (1人 追加負担):</label>
    <select id="extra" class="in">
      <option value="0">なし (均等割り)</option>
      <option value="500">+500円</option>
      <option value="1000" selected>+1000円</option>
      <option value="2000">+2000円</option>
      <option value="3000">+3000円</option>
    </select>
    <label>端数:</label>
    <select id="round" class="in">
      <option value="100" selected>100円 単位 切り上げ</option>
      <option value="500">500円 単位 切り上げ</option>
      <option value="1000">1000円 単位 切り上げ</option>
      <option value="1">1円 単位 (切り上げなし)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="each">¥0</div><div class="cap">参加者 1人</div></div>
      <div class="cell"><div class="num" id="lead">¥0</div><div class="cap">幹事 (多め)</div></div>
      <div class="cell"><div class="num" id="diff">¥0</div><div class="cap">集金 - 合計 (剰余)</div></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const total = parseFloat(document.getElementById('total').value) || 0;
  const n = parseInt(document.getElementById('people').value, 10) || 1;
  const extra = parseFloat(document.getElementById('extra').value) || 0;
  const round = parseFloat(document.getElementById('round').value) || 1;
  if (n < 1) return;
  // 幹事1人 + 一般(n-1)人 で 一般 (per) と 幹事 (per + extra)
  // total = (n-1)*per + (per + extra) = n*per + extra → per = (total - extra) / n
  let per = (total - extra) / n;
  per = Math.ceil(per / round) * round;
  const lead = per + extra;
  const collected = per * (n - 1) + lead;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('each').textContent = fmt(per);
  document.getElementById('lead').textContent = fmt(lead);
  document.getElementById('diff').textContent = fmt(collected - total) + ' (受け取り 超過分)';
};
""",
    "<dt>幹事 多めって 何ですか？</dt><dd>幹事は 場所予約・支払い等で 負担が 多いため、参加者より 多く 出す 慣習を サポートします。</dd>",
))


# ---------- 11. 電気代 計算 [新規:超高需要] ----------
TOOLS.append((
    "electricity-cost", "💡", "電気代 シミュレータ",
    "家電の 消費電力(W) × 使用時間 × 単価 で 電気代を 算出。電気代 高騰 対策に。",
    """    <label>消費電力 (W):</label>
    <input id="w" class="in" type="number" value="1200" />
    <label>1日 使用時間 (時間):</label>
    <input id="h" class="in" type="number" step="0.5" value="3" />
    <label>1ヶ月 使用日数:</label>
    <input id="d" class="in" type="number" value="30" />
    <label>電気単価 (円/kWh):</label>
    <input id="rate" class="in" type="number" step="0.01" value="31" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="daily">¥0</div><div class="cap">1日あたり</div></div>
      <div class="cell"><div class="num" id="monthly">¥0</div><div class="cap">1ヶ月</div></div>
      <div class="cell"><div class="num" id="yearly">¥0</div><div class="cap">1年間</div></div>
    </div>
    <h2>家電の 消費電力 目安</h2>
    <p>エアコン: 600〜1500W ／ 電子レンジ: 1300W ／ ドライヤー: 1200W ／ 冷蔵庫: 100〜300W (常時) ／ 炊飯器: 700〜1300W ／ こたつ: 500W ／ ホットカーペット: 700W ／ 洗濯機: 400W ／ 食洗機: 1200W</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const w = parseFloat(document.getElementById('w').value) || 0;
  const h = parseFloat(document.getElementById('h').value) || 0;
  const d = parseFloat(document.getElementById('d').value) || 0;
  const rate = parseFloat(document.getElementById('rate').value) || 0;
  const daily = (w / 1000) * h * rate;
  const monthly = daily * d;
  const yearly = daily * 365;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('daily').textContent = fmt(daily);
  document.getElementById('monthly').textContent = fmt(monthly);
  document.getElementById('yearly').textContent = fmt(yearly);
};
""",
    "<dt>電気単価は どこを 見れば 分かりますか？</dt><dd>毎月の 電気料金明細に 記載されています。標準的な 従量電灯B は 1kWhあたり 約30〜35円です（地域・契約により 異なります）。</dd>",
))


# ---------- 12. つみたて NISA シミュレータ [新規:高需要] ----------
TOOLS.append((
    "nisa-sim", "📈", "つみたて NISA / 積立投資 シミュレータ",
    "毎月の 積立額・年利・期間から 将来 評価額を 複利計算。新NISA 対応。",
    """    <label>毎月 積立額 (円):</label>
    <input id="monthly" class="in" type="number" value="33333" />
    <label>想定 年利 (%):</label>
    <input id="rate" class="in" type="number" step="0.1" value="5" />
    <label>積立 期間 (年):</label>
    <input id="years" class="in" type="number" value="20" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="principal">¥0</div><div class="cap">投資 元本</div></div>
      <div class="cell"><div class="num" id="future">¥0</div><div class="cap">評価額 (満期)</div></div>
      <div class="cell"><div class="num" id="gain">¥0</div><div class="cap">運用益</div></div>
    </div>
    <h2>10年 ごとの 推移</h2>
    <div id="table" class="cards" style="grid-template-columns:repeat(2,1fr);"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const m = parseFloat(document.getElementById('monthly').value) || 0;
  const r = (parseFloat(document.getElementById('rate').value) || 0) / 100 / 12;
  const yrs = parseInt(document.getElementById('years').value, 10) || 0;
  const n = yrs * 12;
  // 月複利: FV = m * (((1+r)^n - 1) / r)
  const fv = r === 0 ? m * n : m * (Math.pow(1+r, n) - 1) / r;
  const principal = m * n;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('principal').textContent = fmt(principal);
  document.getElementById('future').textContent = fmt(fv);
  document.getElementById('gain').textContent = fmt(fv - principal);
  // 期間内 ごとの 推移
  const table = document.getElementById('table');
  table.innerHTML = '';
  for (let y = 5; y <= yrs; y += 5) {
    const nn = y * 12;
    const v = r === 0 ? m * nn : m * (Math.pow(1+r, nn) - 1) / r;
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.innerHTML = `<div class="num">${fmt(v)}</div><div class="cap">${y}年後</div>`;
    table.appendChild(cell);
  }
};
""",
    "<dt>新NISA の 上限は？</dt><dd>つみたて投資枠 月10万円 (年120万円)、成長投資枠 年240万円。合計 年360万円・生涯1800万円 (2024〜)。本ツールは 上限内なら 非課税で 受け取れます。</dd>",
))


# ---------- 13. 労働時間 集計 [新規:高需要] ----------
TOOLS.append((
    "work-hours", "🕐", "労働時間 集計 (始業・終業・休憩)",
    "始業 / 終業 / 休憩から 1日の 労働時間と 賃金を 計算。複数日 集計も。",
    """    <label>始業 時刻:</label>
    <input id="start" class="in" type="time" value="09:00" />
    <label>終業 時刻:</label>
    <input id="end" class="in" type="time" value="18:00" />
    <label>休憩 (分):</label>
    <input id="rest" class="in" type="number" value="60" />
    <label>時給 (円):</label>
    <input id="wage" class="in" type="number" value="1200" />
    <label>日数 (集計したい 日数):</label>
    <input id="days" class="in" type="number" value="20" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="hours">0</div><div class="cap">1日 労働時間</div></div>
      <div class="cell"><div class="num" id="daily">¥0</div><div class="cap">1日 賃金</div></div>
      <div class="cell"><div class="num" id="total_hours">0</div><div class="cap">合計 時間</div></div>
      <div class="cell"><div class="num" id="total_wage">¥0</div><div class="cap">合計 賃金</div></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const s = document.getElementById('start').value;
  const e = document.getElementById('end').value;
  const rest = parseFloat(document.getElementById('rest').value) || 0;
  const wage = parseFloat(document.getElementById('wage').value) || 0;
  const days = parseFloat(document.getElementById('days').value) || 0;
  if (!s || !e) return;
  const [sh, sm] = s.split(':').map(Number);
  const [eh, em] = e.split(':').map(Number);
  let mins = (eh * 60 + em) - (sh * 60 + sm);
  if (mins < 0) mins += 24 * 60; // 夜勤対応
  mins -= rest;
  if (mins < 0) mins = 0;
  const hours = mins / 60;
  const daily = hours * wage;
  document.getElementById('hours').textContent = hours.toFixed(2) + '時間';
  document.getElementById('daily').textContent = '¥' + Math.round(daily).toLocaleString('ja-JP');
  document.getElementById('total_hours').textContent = (hours * days).toFixed(1) + '時間';
  document.getElementById('total_wage').textContent = '¥' + Math.round(daily * days).toLocaleString('ja-JP');
};
""",
    "",
))


# ---------- 14. 副業 実時給 計算 [新規:独自] ----------
TOOLS.append((
    "side-job-wage", "🏷", "副業 実時給 (本当の 時給)",
    "月収 を 実労働時間で 割って 「本当の 時給」 を 可視化。経費考慮も。",
    """    <label>月の 副業収入 (円):</label>
    <input id="income" class="in" type="number" value="50000" />
    <label>月の 作業時間 (時間):</label>
    <input id="hours" class="in" type="number" step="0.5" value="40" />
    <label>月の 経費 (材料・サーバー等, 円):</label>
    <input id="cost" class="in" type="number" value="3000" />
    <label>税金率 (副業 雑所得・概算 %):</label>
    <input id="tax" class="in" type="number" step="1" value="20" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="gross">¥0</div><div class="cap">表面 時給</div></div>
      <div class="cell"><div class="num" id="net">¥0</div><div class="cap">手取り 実時給</div></div>
      <div class="cell"><div class="num" id="annual">¥0</div><div class="cap">手取り 年収目安</div></div>
    </div>
    <p id="msg" class="note" style="font-size:16px;"></p>
""",
    """
document.getElementById('calc').onclick = () => {
  const income = parseFloat(document.getElementById('income').value) || 0;
  const hours = parseFloat(document.getElementById('hours').value) || 1;
  const cost = parseFloat(document.getElementById('cost').value) || 0;
  const tax = (parseFloat(document.getElementById('tax').value) || 0) / 100;
  const gross = income / hours;
  const net = (income - cost) * (1 - tax) / hours;
  const annual = (income - cost) * (1 - tax) * 12;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('gross').textContent = fmt(gross);
  document.getElementById('net').textContent = fmt(net);
  document.getElementById('annual').textContent = fmt(annual);
  let msg = '';
  if (net < 800) msg = '⚠️ 実時給が 最低賃金以下です。やり方の 見直しが おすすめ。';
  else if (net < 1500) msg = '💡 単価アップ や 効率化の 余地が ありそう。';
  else if (net < 3000) msg = '✅ 一般的な 副業 水準。継続できれば 大きな 収入に。';
  else msg = '🎉 高単価 副業！再現性が あれば 本業化も 検討できます。';
  document.getElementById('msg').textContent = msg;
};
""",
    "<dt>なぜ 実時給を 計算するの？</dt><dd>月5万円の 副業でも 100時間 かけていたら 時給500円。コンビニバイトより 低いことも。「時間あたり 価値」を 知らないと 続けるべきか 判断できません。</dd>",
))


# ---------- 15. 72の法則 (資産 倍化) [新規:独自] ----------
TOOLS.append((
    "rule-72", "⏫", "72の法則 (資産 倍化 計算)",
    "年利○% で 資産が 2倍に なるのは 何年後？72÷利率 の 早見表 で 直感的に。",
    """    <label>年利 (%):</label>
    <input id="rate" class="in" type="number" step="0.1" value="5" />
    <div class="bar"><button type="button" class="btn primary" id="r2y">何年で 倍に？</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="years">0</div><div class="cap">資産が 倍に なる 年数</div></div>
      <div class="cell"><div class="num" id="precise">0</div><div class="cap">正確 計算</div></div>
    </div>
    <hr>
    <label>目標: 何年で 倍に したい？</label>
    <input id="targetY" class="in" type="number" value="10" />
    <div class="bar"><button type="button" class="btn primary" id="y2r">必要な 年利</button></div>
    <div class="num" id="needRate" style="font-size:32px;text-align:center;"></div>
    <h2>早見表</h2>
    <div class="cards">
      <div class="cell"><div class="num">14.4年</div><div class="cap">年利 5% (NISA 想定)</div></div>
      <div class="cell"><div class="num">10.3年</div><div class="cap">年利 7% (米国株 平均)</div></div>
      <div class="cell"><div class="num">7.2年</div><div class="cap">年利 10% (積極運用)</div></div>
      <div class="cell"><div class="num">360年</div><div class="cap">年利 0.2% (定期預金)</div></div>
    </div>
""",
    """
document.getElementById('r2y').onclick = () => {
  const r = parseFloat(document.getElementById('rate').value) || 0;
  if (r <= 0) { document.getElementById('years').textContent = '∞'; document.getElementById('precise').textContent = '∞'; return; }
  const approx = 72 / r;
  const precise = Math.log(2) / Math.log(1 + r / 100);
  document.getElementById('years').textContent = approx.toFixed(1) + '年 (概算)';
  document.getElementById('precise').textContent = precise.toFixed(2) + '年';
};
document.getElementById('y2r').onclick = () => {
  const y = parseFloat(document.getElementById('targetY').value) || 0;
  if (y <= 0) return;
  document.getElementById('needRate').textContent = '年利 ' + (72 / y).toFixed(2) + '%';
};
""",
    "<dt>72の法則とは？</dt><dd>「72÷年利」で 元本が 倍に なる 年数を 近似 計算できる 法則。例: 年利6% なら 12年、年利3% なら 24年。複利 計算の 直感的 ショートカット です。</dd>",
))


# =========================================================================
# C. 時間 / タイマー (4)
# =========================================================================

# ---------- 16. ストップウォッチ ----------
TOOLS.append((
    "stopwatch", "⏱", "ストップウォッチ",
    "ミリ秒 単位の 計測。ラップ 記録 機能 付き。",
    """    <div class="num" id="display" style="font-size:48px;text-align:center;font-variant-numeric:tabular-nums;">00:00.00</div>
    <div class="bar">
      <button type="button" class="btn primary" id="start">開始</button>
      <button type="button" class="btn ghost" id="lap">ラップ</button>
      <button type="button" class="btn ghost" id="reset">リセット</button>
    </div>
    <ol id="laps" style="font-variant-numeric:tabular-nums;"></ol>
""",
    """
let t0 = 0, running = false, raf = null, elapsed = 0;
const $d = document.getElementById('display');
function fmt(ms) {
  const m = Math.floor(ms / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  const c = Math.floor((ms % 1000) / 10);
  return `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}.${String(c).padStart(2,'0')}`;
}
function tick() {
  $d.textContent = fmt(elapsed + (Date.now() - t0));
  raf = requestAnimationFrame(tick);
}
document.getElementById('start').onclick = (e) => {
  if (running) { elapsed += Date.now() - t0; running = false; cancelAnimationFrame(raf); e.target.textContent = '再開'; }
  else { t0 = Date.now(); running = true; tick(); e.target.textContent = '停止'; }
};
document.getElementById('lap').onclick = () => {
  if (!running) return;
  const li = document.createElement('li');
  li.textContent = fmt(elapsed + (Date.now() - t0));
  document.getElementById('laps').appendChild(li);
};
document.getElementById('reset').onclick = () => {
  elapsed = 0; running = false; cancelAnimationFrame(raf);
  $d.textContent = '00:00.00';
  document.getElementById('laps').innerHTML = '';
  document.getElementById('start').textContent = '開始';
};
""",
    "",
))


# ---------- 17. カウントダウン タイマー ----------
TOOLS.append((
    "timer", "⏳", "カウントダウン タイマー",
    "分秒を 指定 して 開始。終了時 アラーム 音。",
    """    <input id="m" class="in" type="number" min="0" value="3" /> 分
    <input id="s" class="in" type="number" min="0" max="59" value="0" /> 秒
    <div class="bar">
      <button type="button" class="btn primary" id="start">開始</button>
      <button type="button" class="btn ghost" id="stop">停止</button>
    </div>
    <div class="num" id="display" style="font-size:64px;text-align:center;font-variant-numeric:tabular-nums;">--:--</div>
""",
    """
let timerId = null, endAt = 0;
const $d = document.getElementById('display');
function tick() {
  const remain = Math.max(0, endAt - Date.now());
  const mm = Math.floor(remain / 60000);
  const ss = Math.floor((remain % 60000) / 1000);
  $d.textContent = `${String(mm).padStart(2,'0')}:${String(ss).padStart(2,'0')}`;
  if (remain === 0) {
    clearInterval(timerId); timerId = null;
    try { const ctx = new AudioContext(); const o = ctx.createOscillator(); o.frequency.value = 880; o.connect(ctx.destination); o.start(); setTimeout(()=>o.stop(),800); } catch {}
    alert('時間です！');
  }
}
document.getElementById('start').onclick = () => {
  const m = parseInt(document.getElementById('m').value, 10) || 0;
  const s = parseInt(document.getElementById('s').value, 10) || 0;
  endAt = Date.now() + (m * 60 + s) * 1000;
  if (timerId) clearInterval(timerId);
  timerId = setInterval(tick, 200);
  tick();
};
document.getElementById('stop').onclick = () => {
  if (timerId) clearInterval(timerId);
  timerId = null;
};
""",
    "",
))


# ---------- 18. ポモドーロタイマー ----------
TOOLS.append((
    "pomodoro", "🍅", "ポモドーロ タイマー",
    "25分 集中 → 5分 休憩 を 繰り返す 学習 法。4セット で 長休憩。",
    """    <div style="text-align:center;">
      <div id="mode" style="font-size:18px;color:#475569;">準備</div>
      <div class="num" id="display" style="font-size:64px;font-variant-numeric:tabular-nums;">25:00</div>
      <div>セット: <span id="set">0</span> / 4</div>
    </div>
    <div class="bar">
      <button type="button" class="btn primary" id="start">開始</button>
      <button type="button" class="btn ghost" id="reset">リセット</button>
    </div>
""",
    """
const cycle = [25*60, 5*60, 25*60, 5*60, 25*60, 5*60, 25*60, 15*60];
let idx = 0, endAt = 0, timerId = null, sets = 0;
const $d = document.getElementById('display');
const $m = document.getElementById('mode');
const $s = document.getElementById('set');
function nextLabel() {
  if (idx % 2 === 0) return '集中';
  if (idx === 7) return '長休憩 (15分)';
  return '休憩 (5分)';
}
function tick() {
  const remain = Math.max(0, endAt - Date.now());
  $d.textContent = `${String(Math.floor(remain/60000)).padStart(2,'0')}:${String(Math.floor((remain%60000)/1000)).padStart(2,'0')}`;
  if (remain === 0) {
    clearInterval(timerId); timerId = null;
    try { const ctx = new AudioContext(); const o = ctx.createOscillator(); o.frequency.value = 660; o.connect(ctx.destination); o.start(); setTimeout(()=>o.stop(),500); } catch {}
    idx++;
    if (idx >= cycle.length) { idx = 0; sets = 0; $m.textContent = '完了！'; return; }
    if (idx % 2 === 0) sets++;
    $s.textContent = sets;
    $m.textContent = nextLabel();
    endAt = Date.now() + cycle[idx] * 1000;
    timerId = setInterval(tick, 500);
    tick();
  }
}
document.getElementById('start').onclick = () => {
  if (timerId) return;
  $m.textContent = nextLabel();
  endAt = Date.now() + cycle[idx] * 1000;
  timerId = setInterval(tick, 500);
  tick();
};
document.getElementById('reset').onclick = () => {
  if (timerId) clearInterval(timerId);
  timerId = null; idx = 0; sets = 0;
  $d.textContent = '25:00'; $m.textContent = '準備'; $s.textContent = '0';
};
""",
    "",
))


# ---------- 19. 会議費用 計算機 [新規:独自バイラル] ----------
TOOLS.append((
    "meeting-cost", "💰", "この 会議いくら？ 会議費用 計算機",
    "参加人数 × 時給 × 時間 で 会議の コストを 可視化。「無駄な 会議」 撲滅 ツール。",
    """    <label>参加 人数:</label>
    <input id="people" class="in" type="number" value="8" />
    <label>平均 時給 (円) - 年収÷2000 が 目安:</label>
    <input id="wage" class="in" type="number" value="3000" />
    <label>会議 時間 (分):</label>
    <input id="mins" class="in" type="number" value="60" />
    <div class="bar">
      <button type="button" class="btn primary" id="calc">計算</button>
      <button type="button" class="btn ghost" id="live">ライブ 計測</button>
    </div>
    <div class="cards">
      <div class="cell"><div class="num" id="perMin">¥0</div><div class="cap">1分あたり</div></div>
      <div class="cell"><div class="num" id="total" style="color:#c00;">¥0</div><div class="cap">会議 総コスト</div></div>
    </div>
    <p id="msg" class="note" style="font-size:16px;"></p>
    <h2>年収 → 時給 換算 (目安)</h2>
    <p>年収400万円 → 時給2000円 ／ 年収600万円 → 時給3000円 ／ 年収800万円 → 時給4000円 ／ 年収1000万円 → 時給5000円</p>
""",
    """
let liveTimer = null, liveStart = 0;
function calc() {
  const p = parseFloat(document.getElementById('people').value) || 0;
  const w = parseFloat(document.getElementById('wage').value) || 0;
  const m = parseFloat(document.getElementById('mins').value) || 0;
  const perMin = (p * w) / 60;
  const total = perMin * m;
  document.getElementById('perMin').textContent = '¥' + Math.round(perMin).toLocaleString('ja-JP');
  document.getElementById('total').textContent = '¥' + Math.round(total).toLocaleString('ja-JP');
  const msg = document.getElementById('msg');
  if (total < 5000) msg.textContent = '✅ 良心的な 会議コスト。';
  else if (total < 30000) msg.textContent = '💡 これだけの 価値ある 結論を 出せれば OK。';
  else if (total < 100000) msg.textContent = '⚠️ 高額な 会議です。アジェンダ と ゴールを 明確に。';
  else msg.textContent = '🔥 ' + Math.round(total/10000) + '万円 の 会議！絶対 ダラダラ 厳禁。';
}
document.getElementById('calc').onclick = calc;
document.getElementById('live').onclick = (e) => {
  if (liveTimer) {
    clearInterval(liveTimer); liveTimer = null;
    e.target.textContent = 'ライブ 計測';
    return;
  }
  liveStart = Date.now();
  e.target.textContent = '停止 (実 ' + new Date(liveStart).toLocaleTimeString() + ' 〜)';
  liveTimer = setInterval(() => {
    const elapsed = (Date.now() - liveStart) / 60000; // minutes
    document.getElementById('mins').value = elapsed.toFixed(1);
    calc();
  }, 1000);
};
""",
    "<dt>これは どう 使うの？</dt><dd>会議冒頭で 「この会議は1分○○円です」と シェアすると 参加者の 意識が 変わります。ライブ計測モードで リアルタイム表示も 可能。</dd>",
))


# =========================================================================
# D. 日付 / 文章 (高需要) (3)
# =========================================================================

# ---------- 20. ○日後 / ○日前 ----------
TOOLS.append((
    "date-shift", "📆", "○日後 / ○日前 計算",
    "指定 日付の N 日後・前を 計算。締切 や 妊娠 出産予定日 計算に。",
    """    <label>基準日:</label>
    <input id="base" type="date" class="in" />
    <label>日数 (＋未来 / −過去):</label>
    <input id="days" type="number" class="in" value="100" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <h2>結果</h2>
    <div class="num" id="out" style="font-size:28px;"></div>
    <div class="cap" id="dow" style="text-align:center;"></div>
""",
    """
const today = new Date().toISOString().slice(0, 10);
document.getElementById('base').value = today;
document.getElementById('calc').onclick = () => {
  const b = document.getElementById('base').value;
  const d = parseInt(document.getElementById('days').value, 10);
  if (!b || isNaN(d)) return;
  const date = new Date(b);
  date.setDate(date.getDate() + d);
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2,'0');
  const dd = String(date.getDate()).padStart(2,'0');
  const dow = ['日','月','火','水','木','金','土'][date.getDay()];
  document.getElementById('out').textContent = `${yyyy}/${mm}/${dd}`;
  document.getElementById('dow').textContent = `(${dow}曜日)`;
};
""",
    "",
))


# ---------- 21. 目標達成日 逆算 [新規:独自] ----------
TOOLS.append((
    "goal-tracker", "🎯", "目標達成日 逆算 (ダイエット・貯金 等)",
    "現在値 → 目標値 まで 1日あたり 進捗で 何日 / いつ 達成かを 計算。",
    """    <label>現在の 値:</label>
    <input id="cur" class="in" type="number" step="0.1" value="75" />
    <label>目標 値:</label>
    <input id="goal" class="in" type="number" step="0.1" value="65" />
    <label>1日あたり 変化量 (絶対値):</label>
    <input id="pace" class="in" type="number" step="0.01" value="0.1" />
    <label>目標 達成 希望日 (任意):</label>
    <input id="deadline" class="in" type="date" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="days">0</div><div class="cap">必要 日数</div></div>
      <div class="cell"><div class="num" id="date">-</div><div class="cap">達成 予定日</div></div>
    </div>
    <p id="msg" class="note" style="font-size:16px;"></p>
    <h2>例</h2>
    <p>ダイエット: 75→65kg、1日0.1kg減 → 100日 ／ 貯金: 100万→300万円、1日1000円 → 2000日 ／ 学習: 0→1000時間、1日2時間 → 500日</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const cur = parseFloat(document.getElementById('cur').value);
  const goal = parseFloat(document.getElementById('goal').value);
  const pace = Math.abs(parseFloat(document.getElementById('pace').value) || 0);
  if (pace === 0) { document.getElementById('days').textContent = '∞'; return; }
  const diff = Math.abs(cur - goal);
  const days = Math.ceil(diff / pace);
  document.getElementById('days').textContent = days + '日';
  const target = new Date();
  target.setDate(target.getDate() + days);
  document.getElementById('date').textContent =
    `${target.getFullYear()}/${String(target.getMonth()+1).padStart(2,'0')}/${String(target.getDate()).padStart(2,'0')}`;
  const ddl = document.getElementById('deadline').value;
  const msg = document.getElementById('msg');
  if (ddl) {
    const dd = new Date(ddl);
    const dayDiff = Math.ceil((dd - new Date()) / 86400000);
    if (dayDiff >= days) msg.textContent = `✅ 希望日に 間に合います (${dayDiff - days}日 余裕)。`;
    else {
      const needed = (diff / dayDiff).toFixed(3);
      msg.textContent = `⚠️ 希望日に ${days - dayDiff}日 不足。 1日あたり ${needed} が 必要です。`;
    }
  } else msg.textContent = '';
};
""",
    "<dt>どんな 目標に 使えますか？</dt><dd>体重・貯金・学習時間・読書ページ・歩数 など、線形 進捗で 表せる 目標 全般。希望日を 入れると 「ペース 不足/余裕」も 表示します。</dd>",
))


# ---------- 22. 読了時間 予測 [新規] ----------
TOOLS.append((
    "read-time", "📖", "読了時間 予測 (記事・本)",
    "テキストを 貼ると 読了 時間を 推定。ブログ 公開時の 「○分で 読めます」 表示に。",
    """    <textarea id="in" class="in" placeholder="記事や 文章を 貼り付けてください"></textarea>
    <label>読書 速度:</label>
    <select id="speed" class="in">
      <option value="400">ゆっくり (400 字/分)</option>
      <option value="600" selected>普通 (600 字/分)</option>
      <option value="800">速い (800 字/分)</option>
      <option value="1200">速読 (1200 字/分)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">推定</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="chars">0</div><div class="cap">文字数</div></div>
      <div class="cell"><div class="num" id="time">0分</div><div class="cap">読了 時間</div></div>
      <div class="cell"><div class="num" id="pages">0</div><div class="cap">原稿用紙 換算</div></div>
    </div>
    <h2>ブログ用 コピペ</h2>
    <p>📖 この記事は <strong id="snippet">約X分</strong> で 読めます (<span id="snippetChars">0</span>文字)</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const text = document.getElementById('in').value;
  const chars = text.replace(/\\s/g, '').length;
  const speed = parseFloat(document.getElementById('speed').value) || 600;
  const totalSec = Math.ceil((chars / speed) * 60);
  const mm = Math.floor(totalSec / 60);
  const ss = totalSec % 60;
  const t = mm > 0 ? `${mm}分${ss > 0 ? ss + '秒' : ''}` : `${ss}秒`;
  document.getElementById('chars').textContent = chars.toLocaleString('ja-JP') + '文字';
  document.getElementById('time').textContent = t;
  document.getElementById('pages').textContent = (chars / 400).toFixed(1) + '枚';
  document.getElementById('snippet').textContent = '約' + (mm || 1) + '分';
  document.getElementById('snippetChars').textContent = chars.toLocaleString('ja-JP');
};
""",
    "<dt>速度の 目安は？</dt><dd>日本人 成人 平均は 約500〜600 字/分。「速読」 は 訓練者の 数字です。ブログでは 600 字/分 で 表示するのが 一般的。</dd>",
))


# ---------- 23. X (Twitter) 文字数 [新規:高需要] ----------
TOOLS.append((
    "tweet-count", "🐦", "X (Twitter) 文字数 カウンター",
    "X (旧Twitter) / Bluesky / Threads の 投稿 文字数 を リアルタイム カウント。",
    """    <textarea id="in" class="in" placeholder="投稿 内容を 入力" style="min-height:120px;"></textarea>
    <div class="cards">
      <div class="cell"><div class="num" id="x">0 / 280</div><div class="cap">X (Twitter)</div></div>
      <div class="cell"><div class="num" id="x_premium">0 / 25000</div><div class="cap">X Premium</div></div>
      <div class="cell"><div class="num" id="bs">0 / 300</div><div class="cap">Bluesky</div></div>
      <div class="cell"><div class="num" id="th">0 / 500</div><div class="cap">Threads</div></div>
    </div>
    <h2>カウント 内訳</h2>
    <div class="cards">
      <div class="cell"><div class="num" id="full">0</div><div class="cap">全角 文字数</div></div>
      <div class="cell"><div class="num" id="half">0</div><div class="cap">半角 文字数</div></div>
      <div class="cell"><div class="num" id="urls">0</div><div class="cap">URL 数</div></div>
    </div>
    <p class="note">※ X では URL は 何文字でも 23字 換算。日本語等の 全角 文字は X では 1文字 ＝ 2 重み (実質 140文字 上限) で 計算。</p>
""",
    """
const $in = document.getElementById('in');
function isHalf(c) { return c.charCodeAt(0) < 0x100 || (c.charCodeAt(0) >= 0xFF61 && c.charCodeAt(0) <= 0xFF9F); }
function update() {
  const t = $in.value;
  // URL を 23字 に 置換
  const urls = t.match(/https?:\\/\\/[^\\s]+/g) || [];
  const tNoUrl = t.replace(/https?:\\/\\/[^\\s]+/g, 'x'.repeat(23));
  // X: 全角=2, 半角=1, /2 → 140char weighted
  let xWeight = 0;
  for (const c of tNoUrl) xWeight += isHalf(c) ? 1 : 2;
  const xVal = Math.ceil(xWeight / 2);
  const len = t.length;
  document.getElementById('x').textContent = xVal + ' / 140';
  document.getElementById('x_premium').textContent = len + ' / 25000';
  document.getElementById('bs').textContent = len + ' / 300';
  document.getElementById('th').textContent = len + ' / 500';
  document.getElementById('full').textContent = [...t].filter(c => !isHalf(c)).length;
  document.getElementById('half').textContent = [...t].filter(isHalf).length;
  document.getElementById('urls').textContent = urls.length;
  // 残量で 色変え
  const elX = document.getElementById('x');
  elX.style.color = xVal > 140 ? '#c00' : (xVal > 120 ? '#e67e22' : '#1d9bf0');
}
$in.addEventListener('input', update);
update();
""",
    "<dt>X の 文字数 ルールは？</dt><dd>日本語等の 全角 文字は 1文字 = 2 重み。280 (重み 単位) / 2 = 140 字 が 上限です。URL は 何文字でも 23字 として 計算されます (X 仕様)。</dd>",
))


# =========================================================================
# E. その他 (3)
# =========================================================================

# ---------- 24. ランダム / サイコロ / コイン ----------
TOOLS.append((
    "random", "🎲", "ランダム 選択 / サイコロ / コイン",
    "迷ったら 任せる！選択肢から ランダム 抽選、サイコロ、コイントス。",
    """    <h2>ランダム抽選</h2>
    <textarea id="choices" class="in" placeholder="選択肢を 1行 ずつ 入力&#10;例:&#10;ラーメン&#10;カレー&#10;寿司"></textarea>
    <div class="bar"><button type="button" class="btn primary" id="pick">抽選！</button></div>
    <div class="num" id="result" style="font-size:32px;text-align:center;"></div>
    <h2>サイコロ</h2>
    <div class="bar">
      <button type="button" class="btn primary" id="d6">6面 サイコロ</button>
      <button type="button" class="btn ghost" id="d100">100面</button>
    </div>
    <div class="num" id="dice" style="font-size:48px;text-align:center;"></div>
    <h2>コイントス</h2>
    <div class="bar"><button type="button" class="btn primary" id="coin">コイン</button></div>
    <div class="num" id="coinR" style="font-size:32px;text-align:center;"></div>
""",
    """
document.getElementById('pick').onclick = () => {
  const arr = document.getElementById('choices').value.split('\\n').filter(s=>s.trim());
  document.getElementById('result').textContent = arr.length ? arr[Math.floor(Math.random()*arr.length)] : '(選択肢なし)';
};
document.getElementById('d6').onclick = () => document.getElementById('dice').textContent = Math.floor(Math.random()*6)+1;
document.getElementById('d100').onclick = () => document.getElementById('dice').textContent = Math.floor(Math.random()*100)+1;
document.getElementById('coin').onclick = () => document.getElementById('coinR').textContent = Math.random() < 0.5 ? '🪙 表' : '🪙 裏';
""",
    "",
))


# ---------- 25. QR コード 生成 ----------
TOOLS.append((
    "qr-code", "🔲", "QR コード 生成",
    "URL や テキストを QR コード化。スマホで 簡単に 読み取れます。",
    """    <textarea id="in" class="in" placeholder="URL や テキストを 入力"></textarea>
    <div class="bar">
      <button type="button" class="btn primary" id="gen">生成</button>
      <button type="button" class="btn ghost" id="dl">ダウンロード</button>
    </div>
    <div id="qr" style="text-align:center;padding:16px;"></div>
""",
    """
function build(text) {
  if (!text) return;
  const size = 300;
  const url = `https://api.qrserver.com/v1/create-qr-code/?data=${encodeURIComponent(text)}&size=${size}x${size}`;
  document.getElementById('qr').innerHTML = `<img id="qrimg" src="${url}" alt="QRコード">`;
}
document.getElementById('gen').onclick = () => build(document.getElementById('in').value);
document.getElementById('dl').onclick = () => {
  const img = document.getElementById('qrimg');
  if (!img) return;
  const a = document.createElement('a');
  a.href = img.src; a.download = 'qrcode.png'; a.click();
};
""",
    "<dt>QR コードの 中身は どこに 送られますか？</dt><dd>外部API (qrserver.com) に テキストが 送られて 画像生成されます。機密データには 使わないでください。</dd>",
))


# =========================================================================
# F. 営業電話なし 即答 シリーズ (個人情報不要・概算 即時)
# =========================================================================

# ---------- 26. 車 買取 概算 [独自:営業電話なし] ----------
TOOLS.append((
    "car-buyback", "🚗", "車 買取 概算 (営業電話なし)",
    "メーカー・年式・走行距離から 買取概算を 即時表示。一括査定の 電話地獄なし、個人情報も 不要。",
    """    <label>メーカー:</label>
    <select id="maker" class="in">
      <option value="1.15">トヨタ・レクサス (人気・高リセール)</option>
      <option value="1.05" selected>ホンダ・日産・マツダ・スズキ・ダイハツ</option>
      <option value="1.00">スバル・三菱・いすゞ</option>
      <option value="0.85">輸入車 (一般)</option>
      <option value="1.10">輸入車プレミアム (BMW/メルセデス/Audi)</option>
    </select>
    <label>ボディ タイプ・排気量:</label>
    <select id="body" class="in">
      <option value="65">軽自動車</option>
      <option value="90">コンパクト (1.3L以下)</option>
      <option value="130" selected>セダン・ハッチバック (1.5L)</option>
      <option value="180">セダン・ハッチバック (2.0L)</option>
      <option value="240">セダン (2.5L以上)</option>
      <option value="220">SUV (小〜中型)</option>
      <option value="320">SUV (大型・プレミアム)</option>
      <option value="230">ミニバン</option>
      <option value="260">スポーツカー</option>
    </select>
    <label>初度登録 年式 (西暦):</label>
    <input id="year" class="in" type="number" min="1990" max="2026" value="2020" />
    <label>走行距離 (km):</label>
    <input id="km" class="in" type="number" value="60000" />
    <label>状態:</label>
    <select id="cond" class="in">
      <option value="1.15">極上 (無事故・修復歴なし・キズ少)</option>
      <option value="1.00" selected>良好 (普通の中古車)</option>
      <option value="0.80">並 (キズ・凹みあり)</option>
      <option value="0.55">難あり (修復歴 / 事故車)</option>
    </select>
    <label>修復歴:</label>
    <select id="acc" class="in">
      <option value="1.00" selected>なし</option>
      <option value="0.70">あり (フレーム修正等)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">買取 概算を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">最低ライン</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">業者 平均</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">最高ライン</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <h2>計算 内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const maker = parseFloat(document.getElementById('maker').value);
  const bodyBase = parseFloat(document.getElementById('body').value); // 3年落ち基準 万円
  const year = parseInt(document.getElementById('year').value, 10);
  const km = parseFloat(document.getElementById('km').value);
  const cond = parseFloat(document.getElementById('cond').value);
  const acc = parseFloat(document.getElementById('acc').value);
  const now = new Date().getFullYear();
  const age = Math.max(0, now - year);
  // 減価: 3年落ちを基準に 年率 12% 低下、ボトム 5%
  let ageF;
  if (age <= 3) ageF = Math.pow(1.08, 3 - age); // 新しい方が高い
  else ageF = Math.pow(0.88, age - 3);
  ageF = Math.max(0.05, ageF);
  // 走行距離: 年1万km基準、超過分 ×0.95/万km、不足は ×1.03/万km (max 1.15)
  const stdKm = age * 10000;
  const diff = (km - stdKm) / 10000;
  let kmF = diff < 0 ? Math.min(1.15, 1 - diff * 0.03) : Math.max(0.5, 1 - diff * 0.05);
  // 業者買取係数: 流通価格の 約 70%
  const dealerF = 0.70;
  // 結果: 3年落ち基準価格×係数群
  const base = bodyBase * 10000 * maker * ageF * kmF * cond * acc * dealerF;
  const mid = Math.round(base);
  const lo = Math.round(base * 0.80);
  const hi = Math.round(base * 1.25);
  const fmt = v => '¥' + v.toLocaleString('ja-JP');
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(mid);
  document.getElementById('hi').textContent = fmt(hi);
  document.getElementById('detail').innerHTML =
    `基準価格 (3年落ち想定): ¥${(bodyBase*10000).toLocaleString('ja-JP')}<br>` +
    `× メーカー人気係数: ${maker.toFixed(2)}<br>` +
    `× 年式 減価係数 (${age}年経過): ${ageF.toFixed(3)}<br>` +
    `× 走行距離 係数 (${km.toLocaleString('ja-JP')}km, 標準${stdKm.toLocaleString('ja-JP')}km): ${kmF.toFixed(3)}<br>` +
    `× 状態係数: ${cond.toFixed(2)}<br>` +
    `× 修復歴 係数: ${acc.toFixed(2)}<br>` +
    `× 業者買取率 (流通価格の約70%): ${dealerF.toFixed(2)}`;
  const msg = document.getElementById('msg');
  if (mid < 50000) msg.textContent = '⚠️ 0円〜廃車費用が かかる ケースも。廃車買取 専門業者が おすすめ。';
  else if (mid < 200000) msg.textContent = '💡 業者間で 差が 出にくい 帯。複数社 相見積りで 1〜3万円の 差。';
  else if (mid < 1000000) msg.textContent = '✅ 業者間 差が 大きい 帯。3社以上 比較で 10〜30万円 アップも。';
  else msg.textContent = '🔥 高額車両。専門店・オートオークション 代行 含めて 比較推奨。';
};
""",
    "<dt>正確な 査定額に なりますか？</dt><dd>あくまで 概算 です (±15〜25% の 誤差)。実車の 状態・色・グレード・オプション・地域 で 大きく 変わります。実際の 買取は 複数業者で 見積もりを 取ってください。</dd><dt>個人情報が 必要 ない 理由は？</dt><dd>このツールは 内蔵 計算式 だけで 動きます。送信先 サーバーは ありません。一括査定 サイトとは 仕組みが 違います。</dd><dt>次に 何を すれば？</dt><dd>本ツールの 概算を 「最低ライン」 として、複数の 買取店 (ガリバー・ビッグモーター以外も) や ユーカーパック (1社のみ 連絡) の 利用が おすすめ。</dd>",
))


# ---------- 27. 不動産 売却 概算 [独自:営業電話なし] ----------
TOOLS.append((
    "realestate-value", "🏠", "不動産 売却 概算 (営業電話なし)",
    "立地・築年数・面積から マンション/戸建/土地の 売却概算を 即時表示。査定サイトに 登録せずに 相場が 分かります。",
    """    <label>物件 タイプ:</label>
    <select id="ptype" class="in">
      <option value="mansion" selected>マンション (区分所有)</option>
      <option value="house">一戸建て (土地+建物)</option>
      <option value="land">土地のみ</option>
    </select>
    <label>地域 区分:</label>
    <select id="area" class="in">
      <option value="700">都心3区 (千代田・中央・港)</option>
      <option value="450">都心5区+渋谷・新宿</option>
      <option value="300" selected>23区 その他 / 横浜・大阪中心</option>
      <option value="180">政令市 中心部 (名古屋・福岡・札幌等)</option>
      <option value="120">政令市 郊外 / 中核市 中心</option>
      <option value="80">その他 主要市</option>
      <option value="45">地方都市 / 郊外</option>
    </select>
    <label>専有 面積 (㎡):</label>
    <input id="area_m2" class="in" type="number" value="70" />
    <label>築年数:</label>
    <input id="age" class="in" type="number" value="10" />
    <label>最寄駅 徒歩 (分):</label>
    <select id="walk" class="in">
      <option value="1.15">3分以内</option>
      <option value="1.05">4-7分</option>
      <option value="1.00" selected>8-10分</option>
      <option value="0.90">11-15分</option>
      <option value="0.75">16-20分</option>
      <option value="0.60">バス便・21分以上</option>
    </select>
    <label>方角・日当たり:</label>
    <select id="face" class="in">
      <option value="1.05">南向き (好条件)</option>
      <option value="1.00" selected>東・南東・南西</option>
      <option value="0.93">西向き</option>
      <option value="0.85">北向き</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">売却 概算を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">早く 売る 価格</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">標準 (3〜6ヶ月)</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">強気 価格</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <h2>計算 内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const ptype = document.getElementById('ptype').value;
  const pricePerTsubo = parseFloat(document.getElementById('area').value); // 万円/坪
  const m2 = parseFloat(document.getElementById('area_m2').value);
  const age = parseFloat(document.getElementById('age').value) || 0;
  const walkF = parseFloat(document.getElementById('walk').value);
  const faceF = parseFloat(document.getElementById('face').value);
  // 坪→㎡: 1坪 = 3.30579㎡
  const pricePerM2 = pricePerTsubo / 3.30579 * 10000; // 円/㎡
  // 建物 減価
  let ageF;
  if (ptype === 'mansion') {
    // RC: 法定耐用年数47年。価値は 30年で 60%、50年で 30%
    ageF = Math.max(0.30, 1 - age * 0.014);
  } else if (ptype === 'house') {
    // 木造: 22年で建物価値ほぼゼロ。土地分残るので 0.35 をボトム
    ageF = Math.max(0.35, 1 - age * 0.030);
  } else {
    // 土地は 経年減価なし、ただし地価変動は無視
    ageF = 1.00;
  }
  const base = pricePerM2 * m2 * ageF * walkF * faceF;
  const mid = Math.round(base);
  const lo = Math.round(base * 0.85); // 早期売却
  const hi = Math.round(base * 1.12); // 強気価格
  const fmt = v => '¥' + v.toLocaleString('ja-JP');
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(mid);
  document.getElementById('hi').textContent = fmt(hi);
  document.getElementById('detail').innerHTML =
    `地域 坪単価: ${pricePerTsubo} 万円/坪 (≒ ¥${Math.round(pricePerM2).toLocaleString('ja-JP')}/㎡)<br>` +
    `× 面積: ${m2}㎡<br>` +
    `× 建物 減価 (築${age}年): ${ageF.toFixed(3)}<br>` +
    `× 駅徒歩 係数: ${walkF.toFixed(2)}<br>` +
    `× 方角 係数: ${faceF.toFixed(2)}`;
  const msg = document.getElementById('msg');
  if (mid < 5000000) msg.textContent = '💡 地方・古い物件 帯。買い手が 限定的なので 不動産屋 複数社 比較を。';
  else if (mid < 30000000) msg.textContent = '✅ 一般的 価格帯。査定は 3社以上で 比較すると ±10% の 差が 出ます。';
  else if (mid < 100000000) msg.textContent = '🏢 中高額帯。仲介手数料も 大きい (3% + 6万)。専任媒介 vs 一般 媒介の 検討も。';
  else msg.textContent = '🔥 高額物件。富裕層向け 仲介・買取保証付き 仲介の 利用も 視野に。';
};
""",
    "<dt>本当に 営業電話 なし？</dt><dd>はい。このツールは ブラウザ内 計算 のみ。住所も 氏名も 入力 不要、送信先 サーバーも ありません。</dd><dt>なぜ 既存の 査定サイトは 個人情報を 取るの？</dt><dd>不動産業者に 顧客リード (見込み客 情報) を 売る ビジネスモデル だからです。複数業者から 同時に 連絡が 来る 仕組みです。</dd><dt>もっと 正確に 知りたい 場合は？</dt><dd>レインズ・マーケット・インフォメーション (国交省 指定 流通機構の 公開データ) で 実際の 成約価格を 確認できます。本ツールの 概算と 合わせると 精度が 上がります。</dd><dt>マンションと 戸建の 違いは？</dt><dd>マンション (RC造) は 50年でも 30% の 価値が 残るのに対し、木造 戸建は 22〜30年で 建物価値が ほぼゼロに。土地価値が 主体に なります。</dd>",
))


# ---------- 28. 引越し 概算 ----------
TOOLS.append((
    "moving-cost", "🚚", "引越し 費用 概算 (営業電話なし)",
    "世帯人数・距離・時期から 引越し費用の 相場を 即時表示。一括見積もりサイトの 電話地獄を 回避。",
    """    <label>世帯 人数:</label>
    <select id="people" class="in">
      <option value="0">単身 (荷物 少なめ / 1K)</option>
      <option value="1" selected>単身 (荷物 多め / 1LDK)</option>
      <option value="2">2人 家族</option>
      <option value="3">3人 家族</option>
      <option value="4">4人 以上</option>
    </select>
    <label>移動 距離:</label>
    <select id="dist" class="in">
      <option value="0" selected>同一市内 (〜15km)</option>
      <option value="1">同一県内 (〜50km)</option>
      <option value="2">隣接県 (〜200km)</option>
      <option value="3">遠距離 (〜500km)</option>
      <option value="4">超遠距離 (500km以上)</option>
    </select>
    <label>時期:</label>
    <select id="season" class="in">
      <option value="1.0" selected>通常期 (5〜2月)</option>
      <option value="1.5">繁忙期 (3月〜4月上旬)</option>
    </select>
    <label>建物 階数:</label>
    <select id="floor" class="in">
      <option value="1.0" selected>1〜2階 / エレベーターあり</option>
      <option value="1.15">3階以上 (エレベーターなし)</option>
    </select>
    <label>曜日:</label>
    <select id="day" class="in">
      <option value="1.0" selected>平日</option>
      <option value="1.10">土日・祝日</option>
    </select>
    <label>オプション (複数選択 可):</label>
    <div>
      <label><input type="checkbox" id="ac" value="15000"> エアコン取外・取付 (1台)</label><br>
      <label><input type="checkbox" id="trash" value="20000"> 不用品 処分</label><br>
      <label><input type="checkbox" id="pack" value="30000"> おまかせパック (荷造り 代行)</label>
    </div>
    <div class="bar"><button type="button" class="btn primary" id="calc">概算を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">最安</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">標準</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">大手 / 安心枠</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <h2>節約 のコツ</h2>
    <p>① 平日・午後便を 選ぶ (午後便は 20-30%安) ／ ② 3-4月の 繁忙期を 避ける (通常期の 1.5倍) ／ ③ 複数社 見積もり (個人情報なしの 比較は 「アート引越センター 」 等の 直接 サイトで)</p>
""",
    """
// 基本料金マトリックス (円): [人数区分][距離区分]
const BASE = [
  // 同市  同県   隣接県  遠距離  超遠距離
  [25000, 35000, 50000,  70000, 100000], // 単身少
  [40000, 55000, 75000, 100000, 140000], // 単身多
  [60000, 80000, 110000, 150000, 200000], // 2人
  [80000, 110000, 150000, 200000, 280000], // 3人
  [100000, 140000, 190000, 250000, 350000] // 4人+
];
document.getElementById('calc').onclick = () => {
  const p = parseInt(document.getElementById('people').value, 10);
  const d = parseInt(document.getElementById('dist').value, 10);
  const season = parseFloat(document.getElementById('season').value);
  const floor = parseFloat(document.getElementById('floor').value);
  const day = parseFloat(document.getElementById('day').value);
  let opt = 0;
  if (document.getElementById('ac').checked) opt += 15000;
  if (document.getElementById('trash').checked) opt += 20000;
  if (document.getElementById('pack').checked) opt += 30000;
  const base = BASE[p][d];
  const mid = Math.round(base * season * floor * day + opt);
  const lo = Math.round(mid * 0.75); // 単身パック・赤帽 等
  const hi = Math.round(mid * 1.35); // 大手 サカイ・アート 等
  const fmt = v => '¥' + v.toLocaleString('ja-JP');
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(mid);
  document.getElementById('hi').textContent = fmt(hi);
  const msg = document.getElementById('msg');
  if (season > 1.0) msg.textContent = '⚠️ 繁忙期 (3〜4月) です。可能なら 1〜2週間 ズラすだけで 大幅節約。';
  else if (lo < 30000) msg.textContent = '💡 赤帽・単身パック (クロネコ・日通) が 最安。';
  else if (mid < 100000) msg.textContent = '✅ 中堅 業者 (アーク・アリさんマーク) で 十分。';
  else msg.textContent = '🚛 大手3社 (サカイ・アート・日通) で 安心枠。複数 見積で ±15%。';
};
""",
    "<dt>本当の 業者見積もりとの ズレは？</dt><dd>±25% 程度。実際は 荷物量・トラック サイズ・搬出入経路 で 大きく 変わります。本ツールで 「最安〜大手」 の レンジを 知った上で、気に なる 業者 2-3社に 個別 問合せが おすすめ。</dd><dt>個人情報なしで 業者に 連絡したい</dt><dd>サカイ・アート・日通 等の 公式サイトで 直接 見積もり 申込み 可能。「一括」 サイトを 経由しなければ 鬼電話 は 来ません。</dd>",
))


# ---------- 29. 結婚式 概算 ----------
TOOLS.append((
    "wedding-cost", "💍", "結婚式 費用 概算 (営業電話なし)",
    "招待人数・スタイル・衣装から 結婚式の 総額・自己負担 (ご祝儀 差引後) を 即時表示。",
    """    <label>招待 人数:</label>
    <input id="guests" class="in" type="number" value="60" min="2" max="300" />
    <label>スタイル:</label>
    <select id="style" class="in">
      <option value="hotel">ホテル ウエディング</option>
      <option value="hall" selected>専門 式場</option>
      <option value="restaurant">レストラン ウエディング</option>
      <option value="garden">ガーデン / ハウスウエディング</option>
      <option value="overseas">海外 挙式</option>
      <option value="nashi">ナシ婚 / 食事会 のみ</option>
    </select>
    <label>衣装:</label>
    <select id="dress" class="in">
      <option value="300000">洋装 1着 (新婦)</option>
      <option value="500000" selected>洋装 2着 (新婦・新郎)</option>
      <option value="800000">洋装+和装 (3〜4着)</option>
      <option value="1200000">フル (5着以上・新郎挙式衣装)</option>
    </select>
    <label>装花 / 演出 グレード:</label>
    <select id="deco" class="in">
      <option value="0">シンプル</option>
      <option value="300000" selected>標準</option>
      <option value="800000">豪華 (生花たっぷり・映像演出)</option>
    </select>
    <label>料理 ランク (1人あたり):</label>
    <select id="meal" class="in">
      <option value="12000">普及 (\\1.2万)</option>
      <option value="18000" selected>標準 (\\1.8万)</option>
      <option value="25000">高級 (\\2.5万)</option>
    </select>
    <label>引出物 (1人あたり):</label>
    <input id="gift" class="in" type="number" value="6000" />
    <div class="bar"><button type="button" class="btn primary" id="calc">概算を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="total">¥0</div><div class="cap">総額</div></div>
      <div class="cell"><div class="num" id="goshugi" style="color:#1d9bf0;">¥0</div><div class="cap">ご祝儀 (収入)</div></div>
      <div class="cell"><div class="num" id="net" style="color:#c00;">¥0</div><div class="cap">自己 負担額</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <h2>内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
// 固定費 (会場費・サービス料込み)
const FIXED = {
  hotel: 1500000, hall: 1100000, restaurant: 700000,
  garden: 1100000, overseas: 1800000, nashi: 200000
};
// 1人あたり 会場 サービス料 (料理・引出物 除く)
const PER = {
  hotel: 18000, hall: 14000, restaurant: 10000,
  garden: 13000, overseas: 5000, nashi: 3000
};
document.getElementById('calc').onclick = () => {
  const guests = parseInt(document.getElementById('guests').value, 10) || 0;
  const style = document.getElementById('style').value;
  const dress = parseFloat(document.getElementById('dress').value);
  const deco = parseFloat(document.getElementById('deco').value);
  const meal = parseFloat(document.getElementById('meal').value);
  const gift = parseFloat(document.getElementById('gift').value) || 0;
  const fixed = FIXED[style];
  const per = PER[style];
  const guestCost = guests * (per + meal + gift);
  const total = fixed + dress + deco + guestCost;
  // ご祝儀: 一般 35,000円/人 (友人) ・親族は高め (平均値)
  const goshugi = style === 'nashi' ? guests * 10000 : guests * 35000;
  const net = total - goshugi;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('total').textContent = fmt(total);
  document.getElementById('goshugi').textContent = fmt(goshugi);
  document.getElementById('net').textContent = fmt(net);
  document.getElementById('detail').innerHTML =
    `会場 固定費: ${fmt(fixed)}<br>` +
    `衣装代: ${fmt(dress)}<br>` +
    `装花・演出: ${fmt(deco)}<br>` +
    `ゲスト 料金 (${guests}名 × ¥${(per+meal+gift).toLocaleString('ja-JP')}/人): ${fmt(guestCost)}<br>` +
    `└ 内訳: 会場/サービス ¥${per.toLocaleString('ja-JP')} + 料理 ¥${meal.toLocaleString('ja-JP')} + 引出物 ¥${gift.toLocaleString('ja-JP')}`;
  const msg = document.getElementById('msg');
  if (net < 0) msg.textContent = '💚 ご祝儀で 黒字！結婚式は 「持ち出し ゼロ」 が 可能です。';
  else if (net < 1000000) msg.textContent = '✅ 一般的な 自己負担 水準。100万円前後が ボリュームゾーン。';
  else if (net < 2500000) msg.textContent = '💡 一般的 上限。装花・衣装の 見直しで ±50万円 調整可能。';
  else msg.textContent = '🌟 ハイクラス。本当に 価値ある 項目に 絞る or 親 援助の 検討を。';
};
""",
    "<dt>ご祝儀の 平均は？</dt><dd>友人 3万円、上司 5万円、親族 5〜10万円。全体 平均は 1人あたり 約3.5万円 (ゼクシィ 結婚トレンド調査)。本ツールは 35,000円/人で 計算しています。</dd><dt>ブライダルフェア の 営業を 避けたい</dt><dd>気になる 式場が あれば 「相談会」 ではなく 「見学のみ・契約しません」 と 最初に 宣言を。本ツールで 相場を 知ってから 行くと 押し切られにくくなります。</dd>",
))


# ---------- 30. リフォーム 概算 ----------
TOOLS.append((
    "renovation-cost", "🏚", "リフォーム 費用 概算 (営業電話なし)",
    "部位を 選ぶだけで リフォーム費用の 相場を 即時表示。訪問見積もりの 高額提案を 回避。",
    """    <p class="cap">リフォームしたい 部位を 選んで グレードを 指定してください (複数選択可)。</p>
    <table style="width:100%;border-collapse:collapse;font-size:15px;">
      <tr><th style="text-align:left;">部位</th><th>グレード</th><th>選択</th></tr>
      <tr><td>キッチン 交換</td><td><select id="g_kitchen" class="in" style="margin:0;"><option value="600000">普及 (60万)</option><option value="1000000" selected>中級 (100万)</option><option value="1800000">高級 (180万)</option></select></td><td><input type="checkbox" id="c_kitchen"></td></tr>
      <tr><td>ユニット バス</td><td><select id="g_bath" class="in" style="margin:0;"><option value="700000">普及 (70万)</option><option value="1100000" selected>中級 (110万)</option><option value="1800000">高級 (180万)</option></select></td><td><input type="checkbox" id="c_bath"></td></tr>
      <tr><td>トイレ 交換</td><td><select id="g_toilet" class="in" style="margin:0;"><option value="150000">普及 (15万)</option><option value="250000" selected>中級 (25万)</option><option value="450000">高級 (45万)</option></select></td><td><input type="checkbox" id="c_toilet"></td></tr>
      <tr><td>洗面 化粧台</td><td><select id="g_basin" class="in" style="margin:0;"><option value="150000">普及 (15万)</option><option value="250000" selected>中級 (25万)</option><option value="400000">高級 (40万)</option></select></td><td><input type="checkbox" id="c_basin"></td></tr>
      <tr><td>外壁 塗装</td><td><select id="g_wall" class="in" style="margin:0;"><option value="800000">普及 (80万 / シリコン)</option><option value="1200000" selected>中級 (120万 / 高耐久)</option><option value="1800000">高級 (180万 / フッ素 ・ 無機)</option></select></td><td><input type="checkbox" id="c_wall"></td></tr>
      <tr><td>屋根 塗装・葺替</td><td><select id="g_roof" class="in" style="margin:0;"><option value="600000">塗装のみ (60万)</option><option value="1200000" selected>カバー工法 (120万)</option><option value="2000000">葺き替え (200万)</option></select></td><td><input type="checkbox" id="c_roof"></td></tr>
      <tr><td>クロス (壁紙) 張替</td><td><input type="number" id="m2_cross" class="in" style="margin:0;" placeholder="㎡" value="50"> × ¥1,300/㎡</td><td><input type="checkbox" id="c_cross"></td></tr>
      <tr><td>フローリング 張替</td><td><input type="number" id="m2_floor" class="in" style="margin:0;" placeholder="㎡" value="20"> × ¥12,000/㎡</td><td><input type="checkbox" id="c_floor"></td></tr>
    </table>
    <div class="bar"><button type="button" class="btn primary" id="calc">合計を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">最安 (相見積もり)</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">標準</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">大手・訪問業者</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
""",
    """
const ITEMS = ['kitchen','bath','toilet','basin','wall','roof'];
document.getElementById('calc').onclick = () => {
  let total = 0;
  for (const k of ITEMS) {
    if (document.getElementById('c_' + k).checked) {
      total += parseFloat(document.getElementById('g_' + k).value);
    }
  }
  if (document.getElementById('c_cross').checked) {
    total += (parseFloat(document.getElementById('m2_cross').value) || 0) * 1300;
  }
  if (document.getElementById('c_floor').checked) {
    total += (parseFloat(document.getElementById('m2_floor').value) || 0) * 12000;
  }
  const mid = Math.round(total);
  const lo = Math.round(total * 0.78); // 地元工務店 直接
  const hi = Math.round(total * 1.40); // 大手リフォーム会社 / 訪問業者
  const fmt = v => '¥' + v.toLocaleString('ja-JP');
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(mid);
  document.getElementById('hi').textContent = fmt(hi);
  const msg = document.getElementById('msg');
  if (mid === 0) msg.textContent = '⚠️ 部位を 選択してください。';
  else if (mid < 500000) msg.textContent = '💡 小規模 工事は 地元工務店が お得。3社 相見積で 20-30% 差が 出ます。';
  else if (mid < 2000000) msg.textContent = '✅ 中規模 リフォーム。「リフォーム瑕疵保険」 加入業者 推奨。';
  else if (mid < 8000000) msg.textContent = '🔧 大規模 リフォーム。住宅ローン・補助金 (省エネ・耐震) も 検討を。';
  else msg.textContent = '🏗 フル リノベ クラス。建て替え 比較も 視野に。';
};
""",
    "<dt>「大手・訪問業者」 で なぜ 1.4倍？</dt><dd>大手リフォーム会社 や 訪問販売 業者は 広告費・営業費 が 上乗せされ、相場の 1.3〜1.5倍 になる ケースが 多い (実例 多数報告)。地元工務店・職人 直接 依頼が 最安です。</dd><dt>悪質訪問業者 を 避けるには？</dt><dd>「今日 契約すれば 半額」 「無料診断」 系は 要注意。本ツールの 「標準」価格より 大幅に 高い 場合は その場で 契約せず 持ち帰って 比較を。</dd><dt>補助金は？</dt><dd>省エネ (窓・断熱)・耐震・バリアフリー 工事には 国・自治体の 補助金 (10〜100万円) が 出ます。「住宅省エネ 2026キャンペーン」 等 を 検索。</dd>",
))


# ---------- 31. 転職 市場価値 ----------
TOOLS.append((
    "career-value", "💼", "転職 市場価値 (年収相場)",
    "業界・役職・経験・スキルから 市場価値 (適正年収) を 即時表示。エージェントを 通さず 相場感を 把握。",
    """    <label>業界:</label>
    <select id="industry" class="in">
      <option value="650">IT・Web (SaaS・SIer・コンサル系)</option>
      <option value="780">外資 IT・FAANG級</option>
      <option value="700">金融 (銀行・証券・保険・運用)</option>
      <option value="600" selected>メーカー (製造・電機・自動車)</option>
      <option value="480">小売・サービス・飲食</option>
      <option value="550">医療・製薬・MR</option>
      <option value="520">教育・出版・メディア</option>
      <option value="580">公務員・準公務 (インフラ)</option>
      <option value="500">建設・不動産・物流</option>
      <option value="530">その他 一般</option>
    </select>
    <label>役職:</label>
    <select id="position" class="in">
      <option value="0.65">一般社員 (主任未満)</option>
      <option value="0.85" selected>主任・リーダークラス</option>
      <option value="1.00">係長・チームリーダー</option>
      <option value="1.30">課長・マネージャー</option>
      <option value="1.70">部長・シニアマネージャー</option>
      <option value="2.20">執行役員・本部長</option>
    </select>
    <label>経験 年数:</label>
    <input id="exp" class="in" type="number" value="8" />
    <label>現在の 年収 (万円):</label>
    <input id="current" class="in" type="number" value="500" />
    <label>保有スキル (1個 +30〜50万円 加算):</label>
    <div>
      <label><input type="checkbox" id="s1" value="50"> 英語 (ビジネス レベル)</label><br>
      <label><input type="checkbox" id="s2" value="40"> マネジメント 経験 (5人 以上)</label><br>
      <label><input type="checkbox" id="s3" value="50"> AI/機械学習・データサイエンス</label><br>
      <label><input type="checkbox" id="s4" value="40"> プロジェクトマネジメント (PMP等)</label><br>
      <label><input type="checkbox" id="s5" value="40"> 専門資格 (会計士・税理士・弁護士・医師)</label><br>
      <label><input type="checkbox" id="s6" value="30"> 海外 勤務 経験</label>
    </div>
    <div class="bar"><button type="button" class="btn primary" id="calc">市場価値を 算出</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">最低ライン</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">適正</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">上振れ (好条件)</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;font-weight:bold;"></p>
    <p id="msg2" class="cap" style="font-size:14px;"></p>
""",
    """
document.getElementById('calc').onclick = () => {
  const indBase = parseFloat(document.getElementById('industry').value); // 万円
  const posF = parseFloat(document.getElementById('position').value);
  const exp = parseFloat(document.getElementById('exp').value) || 0;
  const current = parseFloat(document.getElementById('current').value) || 0;
  // 経験 係数: 0年 0.7, 5年 1.0, 20年 1.4 (上限)
  const expF = Math.min(1.4, 0.7 + (exp / 5) * 0.3);
  let skillSum = 0;
  for (let i = 1; i <= 6; i++) {
    if (document.getElementById('s' + i).checked) skillSum += parseFloat(document.getElementById('s' + i).value);
  }
  const mid = indBase * posF * expF + skillSum;
  const lo = mid * 0.82;
  const hi = mid * 1.30;
  const fmt = v => '¥' + Math.round(v * 10000).toLocaleString('ja-JP');
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(mid);
  document.getElementById('hi').textContent = fmt(hi);
  const diff = mid - current;
  const msg = document.getElementById('msg');
  const msg2 = document.getElementById('msg2');
  if (Math.abs(diff) < 30) {
    msg.textContent = '✅ 市場価値 ≒ 現年収。 適正 水準で 働けています。';
    msg2.textContent = '転職しても 大きな 年収アップは 難しいかも。現職での 役職アップを 狙うのが 効率的。';
  } else if (diff > 100) {
    msg.style.color = '#16a34a';
    msg.textContent = `🔥 +${Math.round(diff)}万円 の 上振れ 余地！`;
    msg2.textContent = '転職で 大幅 アップが 期待できます。複数 エージェント (リクルート/doda/ビズリーチ) で 求人を 見てみましょう。';
  } else if (diff > 30) {
    msg.style.color = '#1d9bf0';
    msg.textContent = `💡 +${Math.round(diff)}万円 の アップ 余地。`;
    msg2.textContent = '同業他社 への 転職で 100万円前後の アップが 狙えそう。';
  } else if (diff < -100) {
    msg.style.color = '#c00';
    msg.textContent = `🌟 現職が ${Math.round(-diff)}万円 オーバー！`;
    msg2.textContent = '現職は 市場相場より 高給です。安易な 転職は 年収ダウン 要注意。';
  } else {
    msg.style.color = '#e67e22';
    msg.textContent = `現職が やや 高め (${Math.round(-diff)}万円 オーバー)。`;
    msg2.textContent = '転職時は 同 ポジションだと 年収ダウン 可能性。役職アップ で 補える 求人を。';
  }
};
""",
    "<dt>計算 根拠は？</dt><dd>厚生労働省 「賃金構造基本統計調査」 と 主要 転職 メディアの 公開 データを 基に した 業界・役職別の 一般的 相場 です。個別 企業・地域 では 大きく 異なります。</dd><dt>本気で 転職活動 する 場合は？</dt><dd>本ツールの 「適正」 を 持参して エージェント 複数 (リクルートエージェント・doda・ビズリーチ) と 話すと、根拠の ある 年収 交渉が できます。</dd>",
))


# ---------- 32. 退職金 概算 ----------
TOOLS.append((
    "retirement-pay", "🛡", "退職金 概算 (税引後 手取り 込み)",
    "勤続年数・基本給・退職事由から 退職金と 課税後 手取りを 即時表示。人事に 聞きにくい 数字が 自分で 分かります。",
    """    <label>勤続 年数:</label>
    <input id="years" class="in" type="number" value="20" min="1" />
    <label>退職時の 基本給 (月額 円):</label>
    <input id="salary" class="in" type="number" value="350000" />
    <label>退職 事由:</label>
    <select id="reason" class="in">
      <option value="0.75">自己都合</option>
      <option value="1.00" selected>会社都合 (リストラ・倒産)</option>
      <option value="1.05">定年</option>
    </select>
    <label>退職金 制度:</label>
    <select id="plan" class="in">
      <option value="1.00" selected>標準的 大企業 (中労委 統計)</option>
      <option value="0.70">中小企業 (中退共 想定)</option>
      <option value="0.50">退職金 制度 弱い 企業</option>
      <option value="1.30">公務員・大企業 上位</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">退職金を 算出</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="gross">¥0</div><div class="cap">退職金 (額面)</div></div>
      <div class="cell"><div class="num" id="tax" style="color:#c00;">¥0</div><div class="cap">税金 (所得税+住民税)</div></div>
      <div class="cell"><div class="num" id="net" style="color:#16a34a;">¥0</div><div class="cap">手取り</div></div>
    </div>
    <h2>計算 内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
// 中央労働委員会 退職金 統計を 簡易化した 支給月数
const SCHEDULE = [
  [1, 0.5], [3, 2], [5, 3.5], [10, 8.5], [15, 15.0],
  [20, 23.0], [25, 32.0], [30, 41.0], [35, 50.0], [40, 58.0]
];
function months(years) {
  if (years <= 1) return 0.5;
  for (let i = 0; i < SCHEDULE.length - 1; i++) {
    if (years >= SCHEDULE[i][0] && years < SCHEDULE[i+1][0]) {
      const [y1, m1] = SCHEDULE[i];
      const [y2, m2] = SCHEDULE[i+1];
      return m1 + (m2 - m1) * (years - y1) / (y2 - y1);
    }
  }
  return SCHEDULE[SCHEDULE.length-1][1] + (years - 40) * 1.5;
}
function deduction(years) {
  // 退職所得控除
  if (years <= 20) return Math.max(800000, 400000 * years);
  return 8000000 + 700000 * (years - 20);
}
// 簡易 所得税率 (退職所得用)
function incomeTax(taxable) {
  // taxable = (退職金 - 控除) / 2
  const T = [
    [1950000, 0.05, 0],
    [3300000, 0.10, 97500],
    [6950000, 0.20, 427500],
    [9000000, 0.23, 636000],
    [18000000, 0.33, 1536000],
    [40000000, 0.40, 2796000],
    [Infinity, 0.45, 4796000]
  ];
  for (const [cap, rate, sub] of T) {
    if (taxable <= cap) return Math.max(0, taxable * rate - sub);
  }
  return 0;
}
document.getElementById('calc').onclick = () => {
  const years = parseFloat(document.getElementById('years').value);
  const salary = parseFloat(document.getElementById('salary').value);
  const reasonF = parseFloat(document.getElementById('reason').value);
  const planF = parseFloat(document.getElementById('plan').value);
  const mo = months(years);
  const gross = Math.round(salary * mo * reasonF * planF);
  const ded = deduction(years);
  const taxable = Math.max(0, (gross - ded) / 2);
  const incomeT = incomeTax(taxable);
  const resTax = taxable * 0.10; // 住民税 10%
  const tax = Math.round(incomeT + resTax);
  const net = gross - tax;
  const fmt = v => '¥' + v.toLocaleString('ja-JP');
  document.getElementById('gross').textContent = fmt(gross);
  document.getElementById('tax').textContent = fmt(tax);
  document.getElementById('net').textContent = fmt(net);
  document.getElementById('detail').innerHTML =
    `支給月数: ${mo.toFixed(1)}ヶ月分 (勤続${years}年 → 中労委統計 補間)<br>` +
    `× 基本給: ¥${salary.toLocaleString('ja-JP')}<br>` +
    `× 退職事由 係数: ${reasonF.toFixed(2)}<br>` +
    `× 企業 規模 係数: ${planF.toFixed(2)}<br>` +
    `<br>退職所得 控除: ¥${ded.toLocaleString('ja-JP')} (勤続${years}年)<br>` +
    `課税対象 額: ¥${Math.round(taxable).toLocaleString('ja-JP')} (= (退職金 - 控除) / 2)<br>` +
    `所得税 概算: ¥${Math.round(incomeT).toLocaleString('ja-JP')}<br>` +
    `住民税 概算: ¥${Math.round(resTax).toLocaleString('ja-JP')}`;
};
""",
    "<dt>会社の 退職金 規程との 差は？</dt><dd>±30% 程度。実際は 会社の 退職金規程 (就業規則 添付) で 決まります。人事 部門に \"退職金 試算\" を 依頼すれば 正確な額が 出ます。本ツールは 「聞く前の 心の準備」 用。</dd><dt>退職所得 控除 とは？</dt><dd>退職金には 大きな 税優遇 が あり、勤続20年までは 年40万円、20年超は 年70万円 が 非課税です。さらに 残りも 1/2 だけが 課税対象 ('退職所得')。</dd><dt>iDeCo や DC の 取扱い は？</dt><dd>本ツールは 会社の 退職一時金 のみ。確定拠出年金 (DC・iDeCo) は 別途 計算が 必要です。受取り方 (一時金 vs 年金) で 税金が 大きく 変わります。</dd>",
))


# ---------- 33. 弁護士費用 相場 ----------
TOOLS.append((
    "lawyer-fee", "⚖️", "弁護士 費用 相場 (旧日弁連 基準)",
    "案件種別・経済利益から 着手金・報酬金の 相場を 即時表示。法律相談 前に 概算を 把握。",
    """    <label>案件 種別:</label>
    <select id="case" class="in">
      <option value="general" selected>一般 民事 (旧日弁連基準)</option>
      <option value="divorce">離婚 (調停・訴訟)</option>
      <option value="inherit">相続 (遺産分割・遺留分)</option>
      <option value="accident">交通事故 (人身)</option>
      <option value="debt">債務整理 (任意整理・1社)</option>
      <option value="criminal">刑事弁護 (起訴後)</option>
      <option value="labor">労働 (解雇・残業代)</option>
    </select>
    <label>経済 利益 (請求額 / 慰謝料 / 遺産額 等, 円):</label>
    <input id="value" class="in" type="number" value="3000000" />
    <div class="bar"><button type="button" class="btn primary" id="calc">費用を 算出</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="start">¥0</div><div class="cap">着手金</div></div>
      <div class="cell"><div class="num" id="reward" style="color:#1d9bf0;">¥0</div><div class="cap">報酬金 (成功時)</div></div>
      <div class="cell"><div class="num" id="total" style="color:#c00;">¥0</div><div class="cap">合計 目安</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <p class="cap" style="font-size:14px;">※ 別途、実費 (印紙代・交通費等)・日当 が かかります。法律相談 料は 30分 5,500円 が 一般的 (初回 無料 事務所も)。</p>
""",
    """
// 旧日弁連 報酬規程 (経済利益 基準) を 着手金・報酬金 双方に
function baseFee(v) {
  if (v <= 3000000) return v * 0.08;
  if (v <= 30000000) return v * 0.05 + 90000;
  if (v <= 300000000) return v * 0.03 + 690000;
  return v * 0.02 + 3690000;
}
const FIXED = {
  general: { startMin: 100000, rewardMin: 100000, mult: 1.0 },
  divorce: { startMin: 300000, rewardMin: 300000, mult: 1.0 },
  inherit: { startMin: 300000, rewardMin: 300000, mult: 1.0 },
  accident: { startMin: 200000, rewardMin: 200000, mult: 0.85 }, // 弁護士特約 想定
  debt: { startMin: 30000, rewardMin: 0, mult: 0.3, perCreditor: 50000 },
  criminal: { startMin: 300000, rewardMin: 300000, mult: 0.5 },
  labor: { startMin: 200000, rewardMin: 200000, mult: 1.0 }
};
document.getElementById('calc').onclick = () => {
  const cs = document.getElementById('case').value;
  const v = parseFloat(document.getElementById('value').value) || 0;
  const c = FIXED[cs];
  let start, reward;
  if (cs === 'debt') {
    start = c.perCreditor; reward = 0;
  } else if (cs === 'criminal') {
    start = Math.max(c.startMin, 500000);
    reward = Math.max(c.rewardMin, 500000); // 成功 (不起訴・執行猶予) 時
  } else {
    const base = baseFee(v) * c.mult;
    start = Math.max(c.startMin, base);
    reward = Math.max(c.rewardMin, base * 2);
  }
  const total = start + reward;
  const fmt = x => '¥' + Math.round(x).toLocaleString('ja-JP');
  document.getElementById('start').textContent = fmt(start);
  document.getElementById('reward').textContent = fmt(reward);
  document.getElementById('total').textContent = fmt(total);
  const msg = document.getElementById('msg');
  if (cs === 'accident') msg.textContent = '🛡 弁護士費用特約 (自動車保険 付帯) で 自己負担 ゼロ の ケース 多数。まず 保険会社に 確認を。';
  else if (cs === 'debt') msg.textContent = '💳 任意整理は 1社あたり。多重債務 5社なら ×5。法テラス・司法書士 (140万円以下) 比較も。';
  else if (total > 1000000) msg.textContent = '⚠️ 高額 案件。複数 弁護士で 着手金 交渉が 可能 (経済利益 比例なので)。';
  else msg.textContent = '✅ 一般的 水準。初回 30分 無料相談 を 利用して 弁護士を 選びましょう。';
};
""",
    "<dt>「経済利益」 って 何？</dt><dd>離婚なら 慰謝料 請求額、相続なら 取得 想定 遺産額、交通事故なら 損害賠償 請求額。「いくら 取り戻す / 守りたいか」 の 金額です。</dd><dt>旧日弁連 基準 は 強制？</dt><dd>2004年に 弁護士報酬 自由化されたため、強制 ではありません。ただし 多くの 事務所が 旧基準を 参考に しています。「成功報酬 のみ」 「完全 定額」 等の 事務所も 増加中。</dd><dt>法テラス は？</dt><dd>収入・資産が 基準以下なら 法テラス (民事法律扶助) で 着手金 立替・無料相談 利用可。年収 約200〜300万円以下 が 目安。</dd>",
))


# ---------- 34. 慰謝料 相場 ----------
TOOLS.append((
    "compensation", "📜", "慰謝料 相場 (判例ベース)",
    "事案別の 慰謝料 相場を 判例 平均から 即時表示。弁護士相談 前に 概算を 把握。",
    """    <label>事案 種別:</label>
    <select id="case" class="in">
      <option value="divorce" selected>離婚 (DV・モラハラ・不貞 等)</option>
      <option value="affair">不倫 (配偶者の 不貞 → 相手方 請求)</option>
      <option value="accident_pain">交通事故 (傷害)</option>
      <option value="accident_disability">交通事故 (後遺障害)</option>
      <option value="accident_death">交通事故 (死亡)</option>
      <option value="harassment">パワハラ・セクハラ</option>
      <option value="engagement">婚約 不当破棄</option>
    </select>
    <div id="optsDivorce" class="opts">
      <label>婚姻 年数:</label>
      <input id="years_marriage" class="in" type="number" value="10" />
      <label>原因:</label>
      <select id="cause_divorce" class="in">
        <option value="100" selected>不貞のみ</option>
        <option value="150">DV (継続的)</option>
        <option value="120">モラハラ・悪意の遺棄</option>
        <option value="80">性格の不一致 (慰謝料が 認められにくい)</option>
      </select>
    </div>
    <div id="optsAffair" class="opts" style="display:none;">
      <label>婚姻 年数:</label>
      <input id="years_affair" class="in" type="number" value="10" />
      <label>不倫の 結果:</label>
      <select id="result_affair" class="in">
        <option value="1.0" selected>離婚 せず (関係 継続)</option>
        <option value="1.8">離婚に 至った</option>
        <option value="2.2">離婚 + 子供あり</option>
      </select>
    </div>
    <div id="optsAccidentPain" class="opts" style="display:none;">
      <label>入院 月数:</label>
      <input id="hosp" class="in" type="number" value="1" />
      <label>通院 月数:</label>
      <input id="visit" class="in" type="number" value="3" />
    </div>
    <div id="optsAccidentDisability" class="opts" style="display:none;">
      <label>後遺障害 等級:</label>
      <select id="grade" class="in">
        <option value="2800">1級 (要介護)</option>
        <option value="2370">2級</option>
        <option value="1990">3級</option>
        <option value="1670">4級</option>
        <option value="1400">5級</option>
        <option value="1180">6級</option>
        <option value="1000">7級</option>
        <option value="830">8級</option>
        <option value="690">9級</option>
        <option value="550">10級</option>
        <option value="420">11級</option>
        <option value="290">12級</option>
        <option value="180">13級</option>
        <option value="110" selected>14級 (むち打ち 等)</option>
      </select>
    </div>
    <div id="optsAccidentDeath" class="opts" style="display:none;">
      <label>被害者 立場:</label>
      <select id="role" class="in">
        <option value="2800" selected>一家の 大黒柱</option>
        <option value="2500">配偶者・母親</option>
        <option value="2200">独身 ・ 子供・高齢者</option>
      </select>
    </div>
    <div id="optsHarassment" class="opts" style="display:none;">
      <label>程度:</label>
      <select id="degree" class="in">
        <option value="50">単発・軽度</option>
        <option value="150" selected>継続的・診断書あり</option>
        <option value="300">悪質・退職に追込</option>
      </select>
    </div>
    <div id="optsEngagement" class="opts" style="display:none;">
      <label>婚約 期間:</label>
      <input id="years_engage" class="in" type="number" value="2" />
    </div>
    <div class="bar"><button type="button" class="btn primary" id="calc">相場を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">低い ケース</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">中央値</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">高い ケース</div></div>
    </div>
    <p class="note" style="font-size:14px;">※ 「赤い本」(日弁連) 「青本」(自賠責) 「判例タイムズ」 等の 平均的 算定額 を 基にした 概算です。個別 事案で 大きく 上下します。</p>
""",
    """
const SECTIONS = ['Divorce','Affair','AccidentPain','AccidentDisability','AccidentDeath','Harassment','Engagement'];
const KEY = {divorce:'Divorce', affair:'Affair', accident_pain:'AccidentPain', accident_disability:'AccidentDisability', accident_death:'AccidentDeath', harassment:'Harassment', engagement:'Engagement'};
function showOnly(k) {
  SECTIONS.forEach(s => document.getElementById('opts'+s).style.display = (s === k) ? 'block' : 'none');
}
document.getElementById('case').addEventListener('change', e => showOnly(KEY[e.target.value]));
document.getElementById('calc').onclick = () => {
  const cs = document.getElementById('case').value;
  let mid;
  if (cs === 'divorce') {
    const y = parseFloat(document.getElementById('years_marriage').value) || 0;
    const base = parseFloat(document.getElementById('cause_divorce').value); // 万円基準
    const yF = Math.min(2.0, 0.5 + y * 0.05); // 婚姻10年で1.0, 30年で2.0
    mid = base * yF;
  } else if (cs === 'affair') {
    const y = parseFloat(document.getElementById('years_affair').value) || 0;
    const r = parseFloat(document.getElementById('result_affair').value);
    const yF = Math.min(2.0, 0.5 + y * 0.05);
    mid = 100 * yF * r;
  } else if (cs === 'accident_pain') {
    const h = parseFloat(document.getElementById('hosp').value) || 0;
    const v = parseFloat(document.getElementById('visit').value) || 0;
    mid = h * 53 + v * 28; // 赤本 基準 (万円)
  } else if (cs === 'accident_disability') {
    mid = parseFloat(document.getElementById('grade').value);
  } else if (cs === 'accident_death') {
    mid = parseFloat(document.getElementById('role').value);
  } else if (cs === 'harassment') {
    mid = parseFloat(document.getElementById('degree').value);
  } else if (cs === 'engagement') {
    const y = parseFloat(document.getElementById('years_engage').value) || 0;
    mid = Math.min(200, 50 + y * 30);
  }
  const lo = mid * 0.65;
  const hi = mid * 1.55;
  const fmt = x => '¥' + Math.round(x * 10000).toLocaleString('ja-JP');
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(mid);
  document.getElementById('hi').textContent = fmt(hi);
};
showOnly('Divorce');
""",
    "<dt>必ず この 金額が 取れますか？</dt><dd>いいえ。慰謝料は 「証拠」 と 「相手の 支払い能力」 で 大きく 変わります。証拠 (LINE・写真・診断書) が 不十分だと 大幅 減額。逆に 明確な 証拠 + 悪質性 立証で 大幅 増額も。</dd><dt>不倫 慰謝料 は 配偶者と 相手 どっち から 取れる？</dt><dd>両方から 取れます (連帯責任)。ただし 合計額 が 慰謝料 総額。配偶者と 関係修復するなら 相手方のみ 請求が 一般的。</dd><dt>交通事故の 「赤本」 「青本」 とは？</dt><dd>赤本: 弁護士 基準 (高め)、青本: 自賠責 基準 (低め)。差は 2-3倍 にも。弁護士に 依頼すると 「赤本基準」 が 通る 可能性が 上がります。</dd>",
))


# ---------- 35. 金・プラチナ 買取 概算 ----------
TOOLS.append((
    "gold-buyback", "🪙", "金・プラチナ 買取 概算",
    "純度・重量・当日相場から 買取額を 即時表示。店舗で 買い叩かれる 前に 自分で 計算。",
    """    <label>種類・純度:</label>
    <select id="purity" class="in">
      <option value="1.000">金 K24 (純金 99.99%)</option>
      <option value="0.917">金 K22 (91.7%)</option>
      <option value="0.750" selected>金 K18 (75%)</option>
      <option value="0.585">金 K14 (58.5%)</option>
      <option value="0.417">金 K10 (41.7%)</option>
      <option value="0.375">金 K9 (37.5%)</option>
      <option value="pt1.000">プラチナ Pt1000 (100%)</option>
      <option value="pt0.950">プラチナ Pt950 (95%)</option>
      <option value="pt0.900">プラチナ Pt900 (90%)</option>
      <option value="pt0.850">プラチナ Pt850 (85%)</option>
      <option value="silver">銀 SV925 (シルバー)</option>
    </select>
    <label>重量 (g):</label>
    <input id="weight" class="in" type="number" step="0.1" value="10" />
    <label>当日 1g 相場 (円) <a href="https://gold.tanaka.co.jp/" target="_blank" rel="noopener">田中貴金属で 確認</a>:</label>
    <input id="rate" class="in" type="number" value="18000" />
    <label>業者 区分:</label>
    <select id="dealer" class="in">
      <option value="0.85">大手 リユースチェーン (大黒屋・コメ兵 等)</option>
      <option value="0.92" selected>金 専門 買取店</option>
      <option value="0.95">地金 業者 (田中貴金属・三菱マテリアル 直接)</option>
      <option value="0.75">出張買取・宝石店 (低め)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">買取 概算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="raw">¥0</div><div class="cap">地金 純価</div></div>
      <div class="cell"><div class="num" id="buyback" style="color:#16a34a;">¥0</div><div class="cap">業者 買取</div></div>
      <div class="cell"><div class="num" id="diff">¥0</div><div class="cap">買取 手数料</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <p class="cap" style="font-size:14px;">※ 当日 相場は 田中貴金属・三菱マテリアル の 公開価格 を 参照。プラチナは 金より 安い 日が 多い (2024〜)。</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const p = document.getElementById('purity').value;
  const w = parseFloat(document.getElementById('weight').value) || 0;
  const rate = parseFloat(document.getElementById('rate').value) || 0;
  const dealer = parseFloat(document.getElementById('dealer').value);
  let purity = parseFloat(p);
  let kind = '金';
  if (p.startsWith('pt')) { purity = parseFloat(p.slice(2)); kind = 'プラチナ'; }
  if (p === 'silver') { purity = 0.925; kind = '銀'; }
  const raw = w * purity * rate;
  const buyback = raw * dealer;
  const diff = raw - buyback;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('raw').textContent = fmt(raw);
  document.getElementById('buyback').textContent = fmt(buyback);
  document.getElementById('diff').textContent = fmt(diff) + ` (${Math.round((1-dealer)*100)}%)`;
  const msg = document.getElementById('msg');
  if (buyback < 5000) msg.textContent = '💡 少量 (アクセサリー 1点) は 専門店 持ち込みが 効率的。';
  else if (buyback < 100000) msg.textContent = '✅ 中規模。3店 相見積で 5-10% アップが 期待できます。';
  else if (buyback < 1000000) msg.textContent = '🔥 高額。地金業者 (田中貴金属 等) 直接持込で 最高値が 出やすい。';
  else msg.textContent = '🏆 大量保有。地金業者 + 法人窓口 で 交渉を。譲渡所得 (年50万円 控除) の 申告も 検討。';
};
""",
    "<dt>なぜ 業者で 差が 出る？</dt><dd>地金業者 (田中貴金属 等) は 公開価格-2% 程度で 買取。リユースチェーンは 「査定料」 「精錬費」 名目で 10-15% 引きが 多い。出張買取は 「来てもらった 手間賃」 で さらに 安く。</dd><dt>売却に 税金は？</dt><dd>金・プラチナの 売却益は 「譲渡所得」。年50万円までの 控除 + 5年超 保有なら 1/2 課税 で、多くの 個人 売却は 非課税で 済みます (200g/月 超は 業者から 税務署 報告)。</dd><dt>偽物 が 心配</dt><dd>正規の 刻印 (K18・Pt900 等) + 重量で 計算。電子比重計 / 蛍光X線分析 で 検査して もらえる 店舗を 選びましょう。</dd>",
))


# =========================================================================
# G. 公的手続き・税金 シリーズ (面倒・分かりにくい を 解消)
# =========================================================================

# ---------- 36. ふるさと納税 上限額 ----------
TOOLS.append((
    "furusato-limit", "🎁", "ふるさと納税 上限額 (給与所得者)",
    "年収・家族構成・社会保険料から ふるさと納税の 控除上限額を 即時計算。シミュレーター 各社の 簡易版。",
    """    <label>給与 年収 (万円):</label>
    <input id="income" class="in" type="number" value="500" />
    <label>家族 構成:</label>
    <select id="family" class="in">
      <option value="0" selected>独身 / 共働き (配偶者 控除なし)</option>
      <option value="1">配偶者 (扶養) あり</option>
      <option value="2">配偶者 + 子1人 (高校生以上)</option>
      <option value="3">配偶者 + 子2人 (高校生以上)</option>
      <option value="4">配偶者 + 子1人 (中学生以下) ※非控除</option>
    </select>
    <label>社会保険料 年額 (万円・通常は年収の14-15%):</label>
    <input id="social" class="in" type="number" value="75" />
    <div class="bar"><button type="button" class="btn primary" id="calc">上限額を 計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="limit" style="color:#16a34a;">¥0</div><div class="cap">寄付 上限額</div></div>
      <div class="cell"><div class="num" id="goods">¥0</div><div class="cap">返礼品 価値 目安 (30%)</div></div>
      <div class="cell"><div class="num" id="cost">¥2,000</div><div class="cap">実質 自己負担</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <p class="cap">※ 給与所得者の 簡易計算。住宅ローン控除・医療費控除 等で 数値は 変動します。</p>
""",
    """
function calc() {
  const income = (parseFloat(document.getElementById('income').value) || 0) * 10000;
  const family = parseInt(document.getElementById('family').value, 10);
  const social = (parseFloat(document.getElementById('social').value) || 0) * 10000;
  // 給与所得控除 (2024年〜)
  let kyuyo;
  if (income <= 1625000) kyuyo = 550000;
  else if (income <= 1800000) kyuyo = income * 0.4 - 100000;
  else if (income <= 3600000) kyuyo = income * 0.3 + 80000;
  else if (income <= 6600000) kyuyo = income * 0.2 + 440000;
  else if (income <= 8500000) kyuyo = income * 0.1 + 1100000;
  else kyuyo = 1950000;
  const giveIncome = income - kyuyo;
  // 配偶者控除 (住民税): 33万 / 子供控除 (16歳以上): 33万/人
  const family_ded = [0, 330000, 660000, 990000, 330000][family];
  // 基礎控除 (住民税): 43万
  const baseDed = 430000;
  const taxableIncome = Math.max(0, giveIncome - social - family_ded - baseDed);
  // 住民税 所得割 (10%)
  const jumin = taxableIncome * 0.10;
  // 所得税 (累進)
  const taxBaseDed = 480000; // 所得税の基礎控除
  const taxFamilyDed = [0, 380000, 760000, 1140000, 380000][family];
  const taxableForIncomeTax = Math.max(0, giveIncome - social - taxFamilyDed - taxBaseDed);
  function incomeTax(t) {
    if (t <= 1950000) return t * 0.05;
    if (t <= 3300000) return t * 0.10 - 97500;
    if (t <= 6950000) return t * 0.20 - 427500;
    if (t <= 9000000) return t * 0.23 - 636000;
    if (t <= 18000000) return t * 0.33 - 1536000;
    if (t <= 40000000) return t * 0.40 - 2796000;
    return t * 0.45 - 4796000;
  }
  const itax = incomeTax(taxableForIncomeTax);
  const itaxRate = taxableForIncomeTax === 0 ? 0 : itax / taxableForIncomeTax;
  // ふるさと納税 上限額の 計算式 (簡易):
  // 上限 = 住民税所得割 × 0.2 / (1 - 0.1 - 所得税率 × 1.021) + 2000
  const limit = jumin * 0.2 / (1 - 0.1 - itaxRate * 1.021) + 2000;
  const fmt = v => '¥' + Math.round(v / 100) * 100 + ''.toLocaleString('ja-JP');
  document.getElementById('limit').textContent = '¥' + (Math.round(limit / 1000) * 1000).toLocaleString('ja-JP');
  document.getElementById('goods').textContent = '¥' + Math.round(limit * 0.3).toLocaleString('ja-JP');
  const msg = document.getElementById('msg');
  if (limit < 10000) msg.textContent = '💡 年収・控除の 影響で 上限が 低めです。';
  else if (limit < 60000) msg.textContent = '✅ 標準的な 帯。実質負担 2000円で 返礼品 (上限の30%) が もらえます。';
  else if (limit < 150000) msg.textContent = '🎁 上限に 余裕あり。複数 自治体への 分散 寄付が おすすめ。';
  else msg.textContent = '🌟 高額。返礼品 多数 + 来年も 同等の 上限が 期待できます。';
}
document.getElementById('calc').onclick = calc;
calc();
""",
    "<dt>正確に 計算するには？</dt><dd>住宅ローン控除・医療費控除・iDeCo 等の 控除が あると 上限が 下がります。「さとふる」 「ふるなび」 等の 詳細 シミュレーターも 併用してください。</dd><dt>本ツールは 何 基準？</dt><dd>給与所得者の 簡易計算 (国税庁 発表の 速算表)。事業所得・年金 受給者は 別計算 です。</dd>",
))


# ---------- 37. 年収の壁 (103/106/130/150) ----------
TOOLS.append((
    "income-wall", "🚧", "年収の壁 (103・106・130・150万円) 判定",
    "パート・アルバイトの 年収から 「どの壁」を 超えると 何が 起きるかを 一発判定。",
    """    <label>給与 年収 (円):</label>
    <input id="income" class="in" type="number" value="1200000" />
    <label>勤務先の 規模:</label>
    <select id="size" class="in">
      <option value="big">大企業 (従業員 101人以上)</option>
      <option value="small" selected>中小企業 (100人以下)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result"></div>
    <h2>年収の壁 早見表</h2>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr style="background:#f1f5f9;"><th>壁</th><th>内容</th><th>影響</th></tr>
      <tr><td>100万円</td><td>住民税 課税</td><td>住民税 (年 数千円〜) が かかり始める</td></tr>
      <tr><td>103万円</td><td>所得税 課税 + 配偶者控除</td><td>所得税 発生・配偶者 配偶者控除 → 配偶者特別控除に</td></tr>
      <tr><td>106万円</td><td>社会保険 加入 (大企業)</td><td>厚生年金・健保 加入 → 手取り 10-15万円減</td></tr>
      <tr><td>130万円</td><td>社会保険 加入 (全企業 配偶者扶養 外れる)</td><td>国保・国年 自己負担 (年20万円程度)</td></tr>
      <tr><td>150万円</td><td>配偶者特別控除 満額終了</td><td>配偶者特別控除が 段階的に 減少</td></tr>
      <tr><td>201万円</td><td>配偶者特別控除 終了</td><td>配偶者特別控除 ゼロに</td></tr>
    </table>
""",
    """
document.getElementById('calc').onclick = () => {
  const income = parseFloat(document.getElementById('income').value) || 0;
  const big = document.getElementById('size').value === 'big';
  const walls = [];
  if (income > 1000000) walls.push({l: '🟡 100万円突破', d: '住民税が かかります (年 数千円〜1万円程度)'});
  if (income > 1030000) walls.push({l: '🟠 103万円突破', d: '所得税が 発生。配偶者の 配偶者控除 → 配偶者特別控除 に 切替 (満額は 維持)'});
  if (income > 1060000 && big) walls.push({l: '🔴 106万円突破 (大企業)', d: '厚生年金・健保 加入義務。手取り 年10-15万円減 (将来の 年金は 増える)'});
  if (income > 1300000) walls.push({l: '🔴 130万円突破', d: '配偶者の 扶養から 外れる。国保 + 国年 で 年20万円 自己負担'});
  if (income > 1500000) walls.push({l: '🟡 150万円突破', d: '配偶者特別控除が 段階的 減少 開始'});
  if (income > 2010000) walls.push({l: '⚫ 201万円突破', d: '配偶者特別控除 ゼロに'});
  const result = document.getElementById('result');
  if (walls.length === 0) {
    result.innerHTML = '<div class="cell" style="background:#dcfce7;padding:16px;"><div class="num" style="color:#16a34a;">✅ 全ての壁の 下</div><div class="cap">税金・社会保険 ともに 影響なし</div></div>';
    return;
  }
  let html = '<h2>あなたが 突破した 壁</h2><div class="cards">';
  for (const w of walls) {
    html += `<div class="cell" style="text-align:left;"><div style="font-weight:bold;font-size:16px;">${w.l}</div><div class="cap">${w.d}</div></div>`;
  }
  html += '</div>';
  // 損益逆転帯の警告
  if (income > 1060000 && income < 1250000 && big) html += '<p class="note" style="color:#c00;font-weight:bold;">⚠️ 「働き損ゾーン」: 106〜125万円 は 社会保険料で 手取り 減少。125万円 超えれば 逆転します。</p>';
  if (income > 1300000 && income < 1530000) html += '<p class="note" style="color:#c00;font-weight:bold;">⚠️ 「働き損ゾーン」: 130〜153万円 は 国保・国年で 手取り 減少。153万円 超えれば 逆転します。</p>';
  result.innerHTML = html;
};
""",
    "<dt>「働き損ゾーン」 とは？</dt><dd>壁を 超えた 直後は 社会保険料で 手取りが 一時的に 減ります (106万→125万、130万→153万 が この帯)。突破するなら 「125万 / 153万 以上 稼ぐ」 計画が 大事です。</dd><dt>2024年の 制度変更は？</dt><dd>政府が 「年収の壁・支援強化パッケージ」 で 一部 緩和 (社保加入時の 助成金 等)。2026年以降も 制度 検討中。</dd>",
))


# ---------- 38. 手取り計算 (額面→手取り) ----------
TOOLS.append((
    "take-home", "💴", "手取り計算 (年収・月収 → 手取り)",
    "額面 年収から 社会保険料・所得税・住民税を 差し引いた 手取り額を 即時表示。",
    """    <label>給与 年収 (額面・円):</label>
    <input id="income" class="in" type="number" value="5000000" />
    <label>賞与の 占める 割合 (年収内・賞与なしは 0%):</label>
    <select id="bonus" class="in">
      <option value="0">なし (月給 のみ)</option>
      <option value="0.15" selected>標準 (年 約2ヶ月分・15%)</option>
      <option value="0.25">多め (年 約3ヶ月分・25%)</option>
      <option value="0.35">大企業 (年 約4-5ヶ月分・35%)</option>
    </select>
    <label>扶養 家族 (配偶者+16歳以上の子):</label>
    <input id="deps" class="in" type="number" value="0" min="0" />
    <div class="bar"><button type="button" class="btn primary" id="calc">手取りを 計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="net" style="color:#16a34a;">¥0</div><div class="cap">年間 手取り</div></div>
      <div class="cell"><div class="num" id="netMonth">¥0</div><div class="cap">月 手取り (賞与含む 平均)</div></div>
      <div class="cell"><div class="num" id="ratio">0%</div><div class="cap">手取り率</div></div>
    </div>
    <h2>内訳 (年間)</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const income = parseFloat(document.getElementById('income').value) || 0;
  const deps = parseInt(document.getElementById('deps').value, 10) || 0;
  // 社会保険料 (厚生年金 9.15% + 健保 約5% + 雇用保険 0.6%) ≒ 14.75%
  const social = income * 0.1475;
  // 給与所得控除
  let kyuyo;
  if (income <= 1625000) kyuyo = 550000;
  else if (income <= 1800000) kyuyo = income * 0.4 - 100000;
  else if (income <= 3600000) kyuyo = income * 0.3 + 80000;
  else if (income <= 6600000) kyuyo = income * 0.2 + 440000;
  else if (income <= 8500000) kyuyo = income * 0.1 + 1100000;
  else kyuyo = 1950000;
  const giveIncome = income - kyuyo;
  // 所得税 (基礎48万 + 扶養38万/人)
  const taxBase = giveIncome - social - 480000 - deps * 380000;
  const t = Math.max(0, taxBase);
  let itax;
  if (t <= 1950000) itax = t * 0.05;
  else if (t <= 3300000) itax = t * 0.10 - 97500;
  else if (t <= 6950000) itax = t * 0.20 - 427500;
  else if (t <= 9000000) itax = t * 0.23 - 636000;
  else if (t <= 18000000) itax = t * 0.33 - 1536000;
  else if (t <= 40000000) itax = t * 0.40 - 2796000;
  else itax = t * 0.45 - 4796000;
  itax *= 1.021; // 復興特別税
  // 住民税 (基礎43万 + 扶養33万/人 + 一律10% + 均等割 約5000円)
  const jumBase = Math.max(0, giveIncome - social - 430000 - deps * 330000);
  const jumin = jumBase * 0.10 + 5000;
  const net = income - social - itax - jumin;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('net').textContent = fmt(net);
  document.getElementById('netMonth').textContent = fmt(net / 12);
  document.getElementById('ratio').textContent = (net / income * 100).toFixed(1) + '%';
  document.getElementById('detail').innerHTML =
    `額面 年収: ${fmt(income)}<br>` +
    `- 社会保険料 (約14.75%): ${fmt(social)}<br>` +
    `- 所得税 (累進+復興税): ${fmt(itax)}<br>` +
    `- 住民税 (一律10%+均等割): ${fmt(jumin)}<br>` +
    `<strong style="color:#16a34a;">= 年間 手取り: ${fmt(net)}</strong>`;
};
""",
    "<dt>「年収 ÷ 0.8 が 手取り」 って 本当？</dt><dd>ざっくり 正しいです。年収 400-800万円 帯なら 手取りは 額面の 75-80% が 一般的。本ツールで 自分の 年収帯で 正確に 計算できます。</dd><dt>賞与の 計算は？</dt><dd>賞与にも 同じく 社会保険料 (14.75%) + 所得税が かかり、住民税は 月給に 含めて 計算。本ツールは 年収 トータルで 計算しているので 賞与 比率に 関わらず ほぼ 同じ結果。</dd>",
))


# ---------- 39. 副業 確定申告 必要判定 ----------
TOOLS.append((
    "side-tax", "🧾", "副業 確定申告 必要判定 + 税額",
    "副業所得・経費から 確定申告の 要否を 判定し、追加 納税額を 試算。20万円ルール に 対応。",
    """    <label>本業 給与年収 (額面・円):</label>
    <input id="main" class="in" type="number" value="5000000" />
    <label>副業 売上 (年間・円):</label>
    <input id="side" class="in" type="number" value="500000" />
    <label>副業 経費 (年間・円):</label>
    <input id="cost" class="in" type="number" value="100000" />
    <label>副業の 種類:</label>
    <select id="type" class="in">
      <option value="zatsu" selected>雑所得 (アフィリエイト・ライティング 等)</option>
      <option value="jigyo">事業所得 (青色申告 65万控除 利用)</option>
      <option value="kyuyo">給与 (アルバイト・WワークでW2)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const main = parseFloat(document.getElementById('main').value) || 0;
  const side = parseFloat(document.getElementById('side').value) || 0;
  const cost = parseFloat(document.getElementById('cost').value) || 0;
  const type = document.getElementById('type').value;
  const sideProfit = Math.max(0, side - cost);
  // 20万円ルール: 給与所得者の 副業所得 (給与以外) が 20万円超で 申告必要
  let needFile, reason;
  if (type === 'kyuyo' && side > 0) {
    needFile = true; reason = '副業が 給与 (アルバイト) の 場合は 副業の 給与額に 関わらず 確定申告 必要';
  } else if (sideProfit > 200000) {
    needFile = true; reason = '副業 所得 (売上 - 経費) が 20万円を 超えるため 確定申告 必要';
  } else {
    needFile = false; reason = `副業 所得 ${sideProfit.toLocaleString('ja-JP')}円 は 20万円 以下のため 確定申告 不要 (※住民税 申告は 別途 必要な 場合あり)`;
  }
  // 追加 税額の 試算 (簡易): 本業の 限界税率 × 副業所得
  let kyuyo;
  if (main <= 1625000) kyuyo = 550000;
  else if (main <= 1800000) kyuyo = main * 0.4 - 100000;
  else if (main <= 3600000) kyuyo = main * 0.3 + 80000;
  else if (main <= 6600000) kyuyo = main * 0.2 + 440000;
  else if (main <= 8500000) kyuyo = main * 0.1 + 1100000;
  else kyuyo = 1950000;
  const mainTaxable = Math.max(0, main - kyuyo - main * 0.1475 - 480000);
  let marginalRate;
  if (mainTaxable <= 1950000) marginalRate = 0.05;
  else if (mainTaxable <= 3300000) marginalRate = 0.10;
  else if (mainTaxable <= 6950000) marginalRate = 0.20;
  else if (mainTaxable <= 9000000) marginalRate = 0.23;
  else if (mainTaxable <= 18000000) marginalRate = 0.33;
  else if (mainTaxable <= 40000000) marginalRate = 0.40;
  else marginalRate = 0.45;
  const aoiroDed = type === 'jigyo' ? 650000 : 0;
  const sideTaxable = Math.max(0, sideProfit - aoiroDed);
  const addTax = sideTaxable * (marginalRate + 0.10) * 1.021;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  const color = needFile ? '#c00' : '#16a34a';
  document.getElementById('result').innerHTML = `
    <div class="cards">
      <div class="cell" style="background:${needFile ? '#fee2e2' : '#dcfce7'};">
        <div class="num" style="color:${color};">${needFile ? '⚠️ 必要' : '✅ 不要'}</div>
        <div class="cap">確定申告 ${needFile ? '要' : '不要'}</div>
      </div>
      <div class="cell"><div class="num">${fmt(sideProfit)}</div><div class="cap">副業 所得</div></div>
      <div class="cell"><div class="num" style="color:#c00;">${fmt(addTax)}</div><div class="cap">追加 納税額 (概算)</div></div>
    </div>
    <p class="note" style="font-size:15px;">${reason}</p>
    <p class="note" style="font-size:14px;">所得税の 限界税率: ${(marginalRate * 100).toFixed(0)}% (本業 課税所得から 算出)。住民税 10% + 復興税 2.1%。</p>`;
};
""",
    "<dt>20万円 以下でも 住民税の 申告は？</dt><dd>所得税の 確定申告 不要でも、副業所得が あれば 住民税の 申告は 別途必要 です (お住まいの 市区町村)。怠ると 後から 追徴課税の 可能性。</dd><dt>青色申告の メリットは？</dt><dd>事業所得として 開業届+青色申告承認申請を 出すと 65万円控除 + 赤字繰越3年 + 家族給与 等の 特典。副業が 30万円超なら 検討価値あり。</dd>",
))


# ---------- 40. iDeCo 節税額 ----------
TOOLS.append((
    "ideco-tax", "🏦", "iDeCo (個人型確定拠出年金) 節税額",
    "月額 掛金から 所得税・住民税の 節税額を 即時表示。新NISA との 比較に。",
    """    <label>給与 年収 (額面・万円):</label>
    <input id="income" class="in" type="number" value="500" />
    <label>iDeCo 月額 掛金 (円):</label>
    <select id="monthly" class="in">
      <option value="5000">5,000 (最低)</option>
      <option value="12000">12,000 (会社員DB+企業DC加入の上限)</option>
      <option value="20000">20,000 (会社員 企業DCのみの上限)</option>
      <option value="23000" selected>23,000 (会社員 企業年金なし 上限)</option>
      <option value="68000">68,000 (自営業 上限)</option>
    </select>
    <label>加入 年数 (退職金 計算用):</label>
    <input id="years" class="in" type="number" value="20" />
    <div class="bar"><button type="button" class="btn primary" id="calc">節税額を 計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="yearTax" style="color:#16a34a;">¥0</div><div class="cap">年間 節税額</div></div>
      <div class="cell"><div class="num" id="totalTax" style="color:#16a34a;">¥0</div><div class="cap">加入期間 累計 節税額</div></div>
      <div class="cell"><div class="num" id="contribution">¥0</div><div class="cap">累計 掛金 (元本)</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <h2>注意点</h2>
    <p class="cap" style="font-size:14px;">① 原則 60歳まで 引き出せない ／ ② 受取時 (退職一時金・年金) に 課税 (ただし 退職所得控除で 大幅 優遇) ／ ③ 運用管理 手数料 (月170円程度) が かかる</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const income = (parseFloat(document.getElementById('income').value) || 0) * 10000;
  const monthly = parseFloat(document.getElementById('monthly').value) || 0;
  const years = parseFloat(document.getElementById('years').value) || 0;
  const annual = monthly * 12;
  // 簡易: 年収から 限界税率を 推定
  let marginalRate;
  if (income <= 3000000) marginalRate = 0.05;
  else if (income <= 4500000) marginalRate = 0.10;
  else if (income <= 7000000) marginalRate = 0.20;
  else if (income <= 9000000) marginalRate = 0.23;
  else if (income <= 18000000) marginalRate = 0.33;
  else marginalRate = 0.40;
  const yearTax = annual * (marginalRate + 0.10) * 1.021;
  const totalTax = yearTax * years;
  const contribution = annual * years;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('yearTax').textContent = fmt(yearTax);
  document.getElementById('totalTax').textContent = fmt(totalTax);
  document.getElementById('contribution').textContent = fmt(contribution);
  const msg = document.getElementById('msg');
  if (yearTax < 10000) msg.textContent = '💡 節税額は 小さめ。NISA の方が 流動性 高くて 有利な ことも。';
  else if (yearTax < 50000) msg.textContent = '✅ 中所得層の 王道。NISA と 併用が ベスト。';
  else msg.textContent = '🔥 高所得者の 強力な 節税ツール。年間 5万円超の 節税は 大きい。';
};
""",
    "<dt>iDeCo と NISA、どっち 先？</dt><dd>① iDeCo (節税) → ② NISA (非課税運用) の 順が 一般的。ただし iDeCo は 60歳まで 引き出せないため、若い 世代は NISA 優先も 合理的。</dd><dt>受取時の 税金は？</dt><dd>一時金 受取は 「退職所得」 (大幅優遇)、年金 受取は 「雑所得」 (公的年金等 控除)。受取り方で 税金が 数十万円 変わる ことが あります。</dd>",
))


# ---------- 41. 失業保険 受給額 ----------
TOOLS.append((
    "unemployment", "🏃", "失業保険 受給額 (基本手当)",
    "離職前6ヶ月の 給与から 基本手当 日額・総額・所定 給付日数を 算出。",
    """    <label>離職前 6ヶ月の 平均 月給 (額面・円):</label>
    <input id="salary" class="in" type="number" value="280000" />
    <label>離職時の 年齢:</label>
    <select id="age" class="in">
      <option value="29" selected>30歳 未満</option>
      <option value="34">30-34歳</option>
      <option value="44">35-44歳</option>
      <option value="59">45-59歳</option>
      <option value="64">60-64歳</option>
    </select>
    <label>雇用保険 加入 年数:</label>
    <input id="years" class="in" type="number" value="5" />
    <label>離職 理由:</label>
    <select id="reason" class="in">
      <option value="self" selected>自己都合</option>
      <option value="company">会社都合 (倒産・解雇・特定理由離職)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">受給額を 計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="daily">¥0</div><div class="cap">基本手当 日額</div></div>
      <div class="cell"><div class="num" id="days">0</div><div class="cap">所定 給付日数</div></div>
      <div class="cell"><div class="num" id="total" style="color:#16a34a;">¥0</div><div class="cap">総 受給額</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
""",
    """
document.getElementById('calc').onclick = () => {
  const salary = parseFloat(document.getElementById('salary').value) || 0;
  const age = parseInt(document.getElementById('age').value, 10);
  const years = parseFloat(document.getElementById('years').value) || 0;
  const isCompany = document.getElementById('reason').value === 'company';
  const daily_wage = salary * 6 / 180; // 賃金日額 = 6ヶ月給与 / 180
  // 給付率: 賃金日額が 低いほど 高率 (45-80%)
  let rate;
  if (daily_wage <= 5200) rate = 0.80;
  else if (daily_wage <= 12000) rate = 0.50 + (12000 - daily_wage) / 6800 * 0.30;
  else if (daily_wage <= 16000) rate = 0.50;
  else rate = 0.45;
  // 日額 上限 (年齢別、2024年)
  const caps = {29: 7065, 34: 7845, 44: 8635, 59: 8635, 64: 7420};
  let daily = Math.min(daily_wage * rate, caps[age]);
  daily = Math.floor(daily);
  // 所定 給付日数
  let days;
  if (isCompany) {
    // 会社都合
    if (age >= 45 && years >= 20) days = 330;
    else if (age >= 45 && years >= 10) days = 270;
    else if (years >= 20) days = 240;
    else if (years >= 10) days = 210;
    else if (years >= 5) days = 180;
    else if (years >= 1) days = age >= 30 ? 180 : 120;
    else days = 90;
  } else {
    // 自己都合
    if (years >= 20) days = 150;
    else if (years >= 10) days = 120;
    else if (years >= 1) days = 90;
    else days = 0;
  }
  const total = daily * days;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('daily').textContent = fmt(daily);
  document.getElementById('days').textContent = days + '日';
  document.getElementById('total').textContent = fmt(total);
  const msg = document.getElementById('msg');
  if (years < 1) msg.textContent = '⚠️ 加入1年 未満は 受給資格 なし (会社都合 6ヶ月以上は 例外あり)。';
  else if (!isCompany) msg.textContent = '💡 自己都合は 給付開始まで 待機7日+給付制限2ヶ月。会社都合より 受給日数も 少なめ。';
  else msg.textContent = '✅ 会社都合 (特定受給資格者) は 待機7日のみ で 給付開始。給付日数も 手厚い。';
};
""",
    "<dt>自己都合と 会社都合の 差は？</dt><dd>自己都合: 待機7日 + 給付制限 2ヶ月 (2025年〜)、給付日数 90-150日。会社都合: 待機7日のみ、給付日数 90-330日。総額で 50-200万円 の差が 出ることも。</dd><dt>「給付制限」 を 短くする 方法は？</dt><dd>会社都合・特定理由離職 (病気・介護・転居 等) は 制限なし。自己都合でも 「正当な理由」 が 認められると 制限なし に なる ケースあり (ハローワーク 相談)。</dd>",
))


# ---------- 42. 年金 受給額 概算 ----------
TOOLS.append((
    "pension", "👴", "年金 受給額 概算 (国民年金+厚生年金)",
    "加入 状況・平均年収から 65歳以降の 年金 受給額 (月額・年額) を 概算。",
    """    <label>国民年金 加入 年数 (国民年金 + 厚生年金 期間 合計):</label>
    <input id="kokumin" class="in" type="number" value="40" max="40" />
    <label>厚生年金 加入 年数:</label>
    <input id="kosei" class="in" type="number" value="40" />
    <label>厚生年金 期間中の 平均年収 (額面 万円):</label>
    <input id="income" class="in" type="number" value="500" />
    <div class="bar"><button type="button" class="btn primary" id="calc">受給額を 計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="monthly" style="color:#16a34a;">¥0</div><div class="cap">月額 受給</div></div>
      <div class="cell"><div class="num" id="yearly">¥0</div><div class="cap">年額 受給</div></div>
      <div class="cell"><div class="num" id="lifetime">¥0</div><div class="cap">65→85歳 累計 (20年)</div></div>
    </div>
    <h2>内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
    <p class="cap" style="font-size:14px;">※ あくまで 概算。実額は 「ねんきん定期便」 「ねんきんネット」 で 確認できます。</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const kokumin_years = Math.min(40, parseFloat(document.getElementById('kokumin').value) || 0);
  const kosei_years = parseFloat(document.getElementById('kosei').value) || 0;
  const income = (parseFloat(document.getElementById('income').value) || 0) * 10000;
  // 国民年金 (基礎年金): 満額 約 81万円/年 (40年加入で)
  const kokumin = 810000 * (kokumin_years / 40);
  // 厚生年金 (報酬比例): 標準報酬 月額 × 5.481/1000 × 加入月数
  // 標準報酬 月額 ≒ 年収 / 12 (賞与含む 場合 やや 補正)
  const monthlyStandard = Math.min(620000, income / 12);
  const kosei = monthlyStandard * 5.481 / 1000 * kosei_years * 12;
  const total = kokumin + kosei;
  const monthly = total / 12;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('monthly').textContent = fmt(monthly);
  document.getElementById('yearly').textContent = fmt(total);
  document.getElementById('lifetime').textContent = fmt(total * 20);
  document.getElementById('detail').innerHTML =
    `国民年金 (基礎年金): ${fmt(kokumin)} / 年<br>` +
    `└ 満額 81万円 × ${kokumin_years}年 / 40年<br>` +
    `厚生年金 (報酬比例): ${fmt(kosei)} / 年<br>` +
    `└ 標準月額 ${fmt(monthlyStandard)} × 5.481/1000 × ${kosei_years*12}月<br>` +
    `<strong>合計: ${fmt(total)} / 年 (${fmt(monthly)} / 月)</strong>`;
};
""",
    "<dt>「ねんきん定期便」 との 差は？</dt><dd>本ツールは 簡易計算 で 誤差 ±10%。正確には 「ねんきんネット」 で 過去の 実 給与から 計算。50歳超なら 定期便に 65歳 見込額 が 記載されます。</dd><dt>繰下げ受給で 増える？</dt><dd>受給開始を 70歳まで 遅らせると 42% 増、75歳までで 84% 増。長生き 見込みなら 検討価値あり。</dd>",
))


# ---------- 43. 児童手当 ----------
TOOLS.append((
    "child-allowance", "👶", "児童手当 受給額 (2024年制度拡充版)",
    "子供の 年齢・人数から 月額・総額を 計算。2024年10月〜 所得制限撤廃 + 高校生 まで 拡大に 対応。",
    """    <label>第1子の 年齢:</label>
    <input id="age1" class="in" type="number" value="3" min="0" max="18" />
    <label>第2子の 年齢 (いない場合 -1):</label>
    <input id="age2" class="in" type="number" value="-1" min="-1" max="18" />
    <label>第3子の 年齢 (いない場合 -1):</label>
    <input id="age3" class="in" type="number" value="-1" min="-1" max="18" />
    <label>第4子の 年齢 (いない場合 -1):</label>
    <input id="age4" class="in" type="number" value="-1" min="-1" max="18" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="monthly" style="color:#16a34a;">¥0</div><div class="cap">月額 合計</div></div>
      <div class="cell"><div class="num" id="yearly">¥0</div><div class="cap">年額 合計</div></div>
      <div class="cell"><div class="num" id="total">¥0</div><div class="cap">高校卒業まで 累計</div></div>
    </div>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;margin-top:16px;"></div>
    <h2>2024年10月〜 拡充ポイント</h2>
    <p class="cap">① 所得制限 撤廃 (高所得世帯も 全額支給) ／ ② 対象 拡大 (中学生 → 高校生 まで) ／ ③ 第3子以降 月3万円に 増額 (従来 1.5万円)</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const ages = [
    parseInt(document.getElementById('age1').value, 10),
    parseInt(document.getElementById('age2').value, 10),
    parseInt(document.getElementById('age3').value, 10),
    parseInt(document.getElementById('age4').value, 10),
  ].filter(a => a >= 0 && a <= 18);
  // 各子供の 月額:
  //   0-2歳: 1.5万円
  //   3-15歳 (第1-2子): 1万円, (第3子以降): 3万円
  //   16-18歳 (高校生・第1-2子): 1万円, (第3子以降): 3万円
  let monthly = 0;
  let detail = '';
  ages.sort((a, b) => b - a); // 年長順 = 第1子から
  let i = 0;
  for (const age of ages) {
    i++;
    let amt;
    if (age < 3) amt = 15000;
    else if (i >= 3) amt = 30000;
    else amt = 10000;
    monthly += amt;
    detail += `第${i}子 (${age}歳): 月 ¥${amt.toLocaleString('ja-JP')}<br>`;
  }
  const yearly = monthly * 12;
  // 累計 (各子が 高校卒業 18歳まで)
  let total = 0;
  i = 0;
  for (const age of ages) {
    i++;
    let yearsLeft = 19 - age;
    if (yearsLeft <= 0) continue;
    let curAge = age;
    for (let y = 0; y < yearsLeft; y++) {
      let amt = curAge < 3 ? 15000 : (i >= 3 ? 30000 : 10000);
      total += amt * 12;
      curAge++;
    }
  }
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('monthly').textContent = fmt(monthly);
  document.getElementById('yearly').textContent = fmt(yearly);
  document.getElementById('total').textContent = fmt(total);
  document.getElementById('detail').innerHTML = detail;
};
""",
    "<dt>申請しないと もらえない？</dt><dd>はい。出生・転入 から 15日以内に お住まいの 市区町村に 申請が 必要。所得制限 撤廃で 高所得世帯も 申請忘れずに。</dd><dt>支給時期は？</dt><dd>年6回 (偶数月)。各回 2ヶ月分 まとめて 振込まれます (例: 4月15万円 = 4-5月分)。</dd>",
))


# =========================================================================
# H. 法律・労務 シリーズ
# =========================================================================

# ---------- 44. 残業代 未払い 計算 ----------
TOOLS.append((
    "overtime-pay", "⏰", "残業代 未払い 計算機 (割増 込み)",
    "労働時間・基本給から 法定 残業代 (時間外/深夜/休日) を 算出。サービス残業の 損失 見える化。",
    """    <label>月の 基本給 (円):</label>
    <input id="base" class="in" type="number" value="280000" />
    <label>月の 所定 労働時間 (時間):</label>
    <input id="std" class="in" type="number" value="160" />
    <label>時間外 (法定外) 残業時間 / 月:</label>
    <input id="ot" class="in" type="number" value="30" />
    <label>深夜 (22時〜5時) 労働時間 / 月:</label>
    <input id="night" class="in" type="number" value="0" />
    <label>休日 (法定休日) 労働時間 / 月:</label>
    <input id="holiday" class="in" type="number" value="0" />
    <label>未払い 期間 (月):</label>
    <input id="months" class="in" type="number" value="12" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="hourly">¥0</div><div class="cap">時給 (基準)</div></div>
      <div class="cell"><div class="num" id="monthly" style="color:#1d9bf0;">¥0</div><div class="cap">月の 未払い</div></div>
      <div class="cell"><div class="num" id="total" style="color:#c00;">¥0</div><div class="cap">未払い 総額 (請求 可能)</div></div>
    </div>
    <h2>内訳 (月)</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
    <p class="note" style="font-size:14px;">※ 時効: 賃金請求は 3年 (2020年4月〜)。証拠 (タイムカード・PC ログ・メール) を 保管しておきましょう。</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const base = parseFloat(document.getElementById('base').value) || 0;
  const std = parseFloat(document.getElementById('std').value) || 1;
  const ot = parseFloat(document.getElementById('ot').value) || 0;
  const night = parseFloat(document.getElementById('night').value) || 0;
  const holiday = parseFloat(document.getElementById('holiday').value) || 0;
  const months = parseFloat(document.getElementById('months').value) || 1;
  const hourly = base / std;
  // 割増率: 時間外 1.25, 60時間超 1.50, 深夜 +0.25, 休日 1.35
  let ot_pay = 0;
  if (ot <= 60) ot_pay = hourly * 1.25 * ot;
  else ot_pay = hourly * 1.25 * 60 + hourly * 1.50 * (ot - 60);
  const night_pay = hourly * 0.25 * night;
  const holiday_pay = hourly * 1.35 * holiday;
  const monthly = ot_pay + night_pay + holiday_pay;
  const total = monthly * months;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('hourly').textContent = fmt(hourly);
  document.getElementById('monthly').textContent = fmt(monthly);
  document.getElementById('total').textContent = fmt(total);
  document.getElementById('detail').innerHTML =
    `時間外 残業 (×1.25): ${ot}h × ${fmt(hourly * 1.25)} = ${fmt(ot_pay)}<br>` +
    (ot > 60 ? `└ 内 60時間超 (×1.50): ${ot - 60}h<br>` : '') +
    `深夜 加算 (+0.25): ${night}h × ${fmt(hourly * 0.25)} = ${fmt(night_pay)}<br>` +
    `休日 (×1.35): ${holiday}h × ${fmt(hourly * 1.35)} = ${fmt(holiday_pay)}<br>` +
    `<strong>月の 未払い 合計: ${fmt(monthly)}</strong>`;
};
""",
    "<dt>請求できる 期間は？</dt><dd>2020年4月以降の 賃金は 3年 (2020年3月以前は 2年)。たとえば 5年 サービス残業させられても、過去3年分のみ 請求可能。早めに 行動を。</dd><dt>請求の 進め方は？</dt><dd>① 証拠収集 (タイムカード・PC ログ・LINE等) → ② 会社に 内容証明 で 請求 → ③ 労基署 申告 / 弁護士 相談。労基署は 無料、弁護士は 着手金20万〜 + 成功報酬20%程度。</dd>",
))


# ---------- 45. 有給休暇 付与日数 ----------
TOOLS.append((
    "paid-leave", "🏖", "有給休暇 付与日数 (年次有給休暇)",
    "入社日から 現在までの 有給 付与日数 + 残日数を 自動計算。労基法 39条 ベース。",
    """    <label>入社日:</label>
    <input id="hire" class="in" type="date" />
    <label>週の 所定 労働時間:</label>
    <select id="hours" class="in">
      <option value="full" selected>30時間 以上 (フルタイム)</option>
      <option value="4">週 4日 (短時間)</option>
      <option value="3">週 3日</option>
      <option value="2">週 2日</option>
      <option value="1">週 1日</option>
    </select>
    <label>これまでに 取得した 有給 日数:</label>
    <input id="used" class="in" type="number" value="0" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="granted">0</div><div class="cap">累計 付与</div></div>
      <div class="cell"><div class="num" id="used_display">0</div><div class="cap">取得済</div></div>
      <div class="cell"><div class="num" id="remain" style="color:#16a34a;">0</div><div class="cap">残 (上限 40日)</div></div>
    </div>
    <h2>付与 履歴</h2>
    <div id="history" class="cap" style="font-size:14px;line-height:1.8;"></div>
    <p class="cap">※ 有給は 取得から 2年で 時効消滅。最大 40日 (前年 繰越 20+今年 20) まで 保持可能。</p>
""",
    """
const SCHEDULE_FULL = [
  // 勤続年数, 付与日数
  [0.5, 10], [1.5, 11], [2.5, 12], [3.5, 14], [4.5, 16], [5.5, 18], [6.5, 20]
];
const SCHEDULE_PART = {
  4: [[0.5, 7], [1.5, 8], [2.5, 9], [3.5, 10], [4.5, 12], [5.5, 13], [6.5, 15]],
  3: [[0.5, 5], [1.5, 6], [2.5, 6], [3.5, 8], [4.5, 9], [5.5, 10], [6.5, 11]],
  2: [[0.5, 3], [1.5, 4], [2.5, 4], [3.5, 5], [4.5, 6], [5.5, 6], [6.5, 7]],
  1: [[0.5, 1], [1.5, 2], [2.5, 2], [3.5, 2], [4.5, 3], [5.5, 3], [6.5, 3]],
};
document.getElementById('hire').valueAsDate = new Date(Date.now() - 3 * 365 * 24 * 3600 * 1000);
document.getElementById('calc').onclick = () => {
  const hireStr = document.getElementById('hire').value;
  if (!hireStr) return;
  const hire = new Date(hireStr);
  const now = new Date();
  const days = (now - hire) / (1000 * 60 * 60 * 24);
  const yearsServed = days / 365.25;
  const hoursVal = document.getElementById('hours').value;
  const schedule = hoursVal === 'full' ? SCHEDULE_FULL : SCHEDULE_PART[hoursVal];
  let granted = 0;
  let history = '';
  for (const [y, d] of schedule) {
    if (yearsServed >= y) {
      granted += d;
      const grantDate = new Date(hire.getTime() + y * 365.25 * 24 * 3600 * 1000);
      history += `${grantDate.getFullYear()}/${grantDate.getMonth()+1}/${grantDate.getDate()}: +${d}日 (勤続${y}年)<br>`;
    }
  }
  // 7年目以降は 毎年 20日 (フル) または 規定
  if (yearsServed > 6.5) {
    const extraYears = Math.floor(yearsServed - 6.5);
    const extra = hoursVal === 'full' ? 20 : schedule[schedule.length - 1][1];
    granted += extra * extraYears;
    for (let i = 0; i < extraYears; i++) {
      const grantDate = new Date(hire.getTime() + (7.5 + i) * 365.25 * 24 * 3600 * 1000);
      if (grantDate <= now) history += `${grantDate.getFullYear()}/${grantDate.getMonth()+1}/${grantDate.getDate()}: +${extra}日<br>`;
    }
  }
  const used = parseFloat(document.getElementById('used').value) || 0;
  const remain = Math.min(40, granted - used); // 上限 40日 (2年 時効)
  document.getElementById('granted').textContent = granted + '日';
  document.getElementById('used_display').textContent = used + '日';
  document.getElementById('remain').textContent = remain + '日';
  document.getElementById('history').innerHTML = history;
};
""",
    "<dt>年5日 取得 義務は？</dt><dd>2019年4月から 年10日以上 付与される 労働者は 年5日 取得が 義務化 (会社が 取らせる 責任)。違反は 30万円以下 罰金。</dd><dt>退職時に 残ったら？</dt><dd>退職前に 全消化 が ベスト。会社が 拒否したら 違法。買取は 法的義務 なしですが、慣行で 行う 会社も あります。</dd>",
))


# ---------- 46. 解雇予告手当 ----------
TOOLS.append((
    "dismissal-pay", "📋", "解雇予告手当 計算機",
    "解雇予告から 解雇日までの 日数 不足分の 手当 (労基法 20条) を 計算。",
    """    <label>過去 3ヶ月の 給与 合計 (額面・円):</label>
    <input id="totalWage" class="in" type="number" value="900000" />
    <label>過去 3ヶ月の 総日数 (通常 約90日):</label>
    <input id="totalDays" class="in" type="number" value="90" />
    <label>解雇 予告日から 解雇日までの 日数:</label>
    <input id="noticeDays" class="in" type="number" value="0" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="avgWage">¥0</div><div class="cap">平均賃金 (1日)</div></div>
      <div class="cell"><div class="num" id="shortage">0</div><div class="cap">不足 日数</div></div>
      <div class="cell"><div class="num" id="pay" style="color:#16a34a;">¥0</div><div class="cap">解雇予告 手当</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <h2>労基法 20条 のルール</h2>
    <p class="cap">使用者は 労働者を 解雇する 場合、少なくとも 30日 前に 予告 しなければ ならない。30日 前に 予告 しない 場合は 30日分 以上の 平均賃金を 支払う 必要 (予告日数 不足分の 平均賃金を 支払えば 即時 解雇 可能)。</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const totalWage = parseFloat(document.getElementById('totalWage').value) || 0;
  const totalDays = parseFloat(document.getElementById('totalDays').value) || 90;
  const noticeDays = parseFloat(document.getElementById('noticeDays').value) || 0;
  const avg = totalWage / totalDays;
  const shortage = Math.max(0, 30 - noticeDays);
  const pay = avg * shortage;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('avgWage').textContent = fmt(avg);
  document.getElementById('shortage').textContent = shortage + '日';
  document.getElementById('pay').textContent = fmt(pay);
  const msg = document.getElementById('msg');
  if (noticeDays >= 30) msg.textContent = '✅ 30日 以上の 予告 期間が あれば 解雇予告 手当は 不要。';
  else if (noticeDays === 0) msg.textContent = '⚠️ 即時 解雇には 30日分 全額 (' + fmt(avg * 30) + ') の 解雇予告 手当が 必要。';
  else msg.textContent = `📋 ${noticeDays}日 前 予告 + ${shortage}日分 手当 (${fmt(pay)}) で 解雇 適法。`;
};
""",
    "<dt>解雇予告 不要の ケースは？</dt><dd>① 試用期間 14日以内 / ② 日雇い 1ヶ月以内 / ③ 季節雇用 4ヶ月以内 / ④ 天災 等で 事業継続 不可能 / ⑤ 労働者の 責に 帰すべき 重大事由 (横領 等)。これ以外は 必要。</dd><dt>解雇が 無効な ケースは？</dt><dd>「解雇権 濫用法理」 (労契法16条) で 客観的・合理的 理由がない 解雇は 無効。本ツールは あくまで 「適法 解雇の 場合の 手当」 計算。違法 解雇は 別途 損害賠償 請求 可能。</dd>",
))


# ---------- 47. 養育費 相場 (算定表) ----------
TOOLS.append((
    "child-support", "👨‍👩‍👧", "養育費 相場 (家裁 算定表ベース)",
    "離婚後の 養育費 相場を 家庭裁判所の 標準算定方式から 即時表示。",
    """    <label>支払う側 (義務者) の 年収 (給与・万円):</label>
    <input id="payer" class="in" type="number" value="500" />
    <label>受け取る側 (権利者) の 年収 (給与・万円):</label>
    <input id="receiver" class="in" type="number" value="200" />
    <label>子供の 人数:</label>
    <select id="kids" class="in">
      <option value="1" selected>1人</option>
      <option value="2">2人</option>
      <option value="3">3人</option>
    </select>
    <label>子供の 年齢区分 (一番 上):</label>
    <select id="age" class="in">
      <option value="14" selected>0〜14歳</option>
      <option value="20">15歳以上 (高校〜大学)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">相場を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="lo">¥0</div><div class="cap">低い ケース</div></div>
      <div class="cell"><div class="num" id="mid" style="color:#16a34a;">¥0</div><div class="cap">標準</div></div>
      <div class="cell"><div class="num" id="hi">¥0</div><div class="cap">高い ケース</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <p class="cap">※ 2019年 改定の 標準算定方式 (家庭裁判所 公表) を 簡易化。実際の 調停・審判は 詳細な 計算式で 決まります。</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const payer = parseFloat(document.getElementById('payer').value) || 0;
  const receiver = parseFloat(document.getElementById('receiver').value) || 0;
  const kids = parseInt(document.getElementById('kids').value, 10);
  const olderAge = parseInt(document.getElementById('age').value, 10);
  // 標準算定方式の 簡易近似 (給与所得者・月額)
  // 月額 ≒ 義務者 基礎収入 × 子の指数 / (義務者 基礎収入 + 権利者 基礎収入) × 子の指数
  const payerBase = payer * 0.4; // 基礎収入 ≒ 年収 × 40%
  const receiverBase = receiver * 0.4;
  // 子の指数 (0-14: 62, 15以上: 85)
  const idx14 = 62, idx15 = 85;
  let kidIdx;
  if (kids === 1) kidIdx = olderAge < 15 ? idx14 : idx15;
  else if (kids === 2) {
    kidIdx = olderAge < 15 ? idx14 * 2 : (idx15 + idx14);
  } else {
    kidIdx = olderAge < 15 ? idx14 * 3 : (idx15 + idx14 * 2);
  }
  // 親の指数: 大人 100
  const totalLiving = 100 + kidIdx;
  const kidShareOfPayer = payerBase * (kidIdx / totalLiving);
  // 義務者と 権利者で 子供 生活費を 按分
  const baseTotal = payerBase + receiverBase;
  const payerShare = baseTotal === 0 ? 0 : kidShareOfPayer * (payerBase / baseTotal);
  const monthly = payerShare * 10000 / 12; // 万円→円 月額
  const lo = monthly * 0.80;
  const hi = monthly * 1.25;
  const fmt = v => '¥' + Math.round(v / 1000) * 1000 + '/月';
  document.getElementById('lo').textContent = fmt(lo);
  document.getElementById('mid').textContent = fmt(monthly);
  document.getElementById('hi').textContent = fmt(hi);
  const msg = document.getElementById('msg');
  msg.textContent = `月額 約 ${Math.round(monthly / 10000)}万円 が 標準。20歳 までの 累計で 約 ${Math.round(monthly * 12 * (20 - olderAge) / 10000)}万円。`;
};
""",
    "<dt>強制的に 払わせられる？</dt><dd>離婚時に 公正証書 / 調停調書 / 審判 で 取り決めると 強制執行 可能。協議離婚で 口約束 のみ だと 強制力 弱い (改めて 調停 必要)。</dd><dt>払う側の 再婚で 減額される？</dt><dd>再婚相手や 連れ子 を 扶養すると 「事情変更」 で 減額 申立て 可能。一方、受け取る側の 再婚で 養子縁組 が 成立すると 大幅 減額 / 停止 も。</dd>",
))


# =========================================================================
# I. ライフプラン シリーズ
# =========================================================================

# ---------- 48. 住宅 vs 賃貸 損益分岐 ----------
TOOLS.append((
    "buy-vs-rent", "🏘", "持ち家 vs 賃貸 損益分岐 (30年シミュ)",
    "家賃・住宅価格・諸経費から 30年間の 総コストを 比較。「結局 どっち得？」 を 即答。",
    """    <h2>持ち家 (購入する場合)</h2>
    <label>物件 価格 (万円):</label>
    <input id="price" class="in" type="number" value="4000" />
    <label>頭金 (万円):</label>
    <input id="down" class="in" type="number" value="400" />
    <label>住宅ローン 金利 (年率%):</label>
    <input id="rate" class="in" type="number" step="0.05" value="1.0" />
    <label>返済 期間 (年):</label>
    <input id="years" class="in" type="number" value="35" />
    <h2>賃貸 (借りる場合)</h2>
    <label>月の 家賃 (円):</label>
    <input id="rent" class="in" type="number" value="100000" />
    <label>更新料 (家賃 1ヶ月分・2年に1回 想定):</label>
    <input id="renew" class="in" type="number" value="100000" />
    <h2>共通</h2>
    <label>シミュレーション 期間 (年):</label>
    <input id="period" class="in" type="number" value="30" />
    <div class="bar"><button type="button" class="btn primary" id="calc">比較</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="buyTotal" style="color:#1d9bf0;">¥0</div><div class="cap">持ち家 総支出</div></div>
      <div class="cell"><div class="num" id="rentTotal" style="color:#e67e22;">¥0</div><div class="cap">賃貸 総支出</div></div>
      <div class="cell"><div class="num" id="diff" style="color:#16a34a;">¥0</div><div class="cap">差額</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;font-weight:bold;"></p>
    <h2>内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const price = (parseFloat(document.getElementById('price').value) || 0) * 10000;
  const down = (parseFloat(document.getElementById('down').value) || 0) * 10000;
  const rate = (parseFloat(document.getElementById('rate').value) || 0) / 100 / 12;
  const yrs = parseFloat(document.getElementById('years').value) || 0;
  const rent = parseFloat(document.getElementById('rent').value) || 0;
  const renew = parseFloat(document.getElementById('renew').value) || 0;
  const period = parseFloat(document.getElementById('period').value) || 0;
  // 持ち家
  const loan = price - down;
  const n = yrs * 12;
  const monthly = rate === 0 ? loan / n : loan * rate / (1 - Math.pow(1 + rate, -n));
  const periodMonths = Math.min(period * 12, n);
  const loanPaid = monthly * periodMonths + (period > yrs ? 0 : 0);
  // 諸費用: 購入時 6%, 固定資産税 年12万, 修繕積立 年20万 (戸建・マンション 平均)
  const buyCost = price * 0.06 + (120000 + 200000) * period;
  const buyTotal = down + loanPaid + buyCost;
  // 賃貸
  const rentPaid = rent * 12 * period;
  const renewPaid = renew * Math.floor(period / 2);
  const moveCost = 200000; // 入居時の 礼金・敷金 等
  const rentTotal = rentPaid + renewPaid + moveCost;
  const diff = buyTotal - rentTotal;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('buyTotal').textContent = fmt(buyTotal);
  document.getElementById('rentTotal').textContent = fmt(rentTotal);
  document.getElementById('diff').textContent = (diff > 0 ? '+' : '') + fmt(diff);
  const msg = document.getElementById('msg');
  if (diff > 5000000) msg.textContent = `🏘 賃貸が ${fmt(diff)} お得 (期間 ${period}年で)。`;
  else if (diff > 0) msg.textContent = `📊 賃貸が やや 有利 (${fmt(diff)} 安い)。`;
  else if (diff > -5000000) msg.textContent = `📊 持ち家が やや 有利 (${fmt(-diff)} 安い)。`;
  else msg.textContent = `🏠 持ち家が ${fmt(-diff)} お得 (期間 ${period}年で)。さらに 資産も 残る！`;
  document.getElementById('detail').innerHTML =
    `<strong>持ち家</strong><br>` +
    `頭金: ${fmt(down)}<br>` +
    `ローン返済 (${period}年分): ${fmt(loanPaid)}<br>` +
    `諸費用 (購入時+固定資産税+修繕): ${fmt(buyCost)}<br>` +
    `※ ${period}年後の 物件 残価値 (3割想定): ${fmt(price * 0.3)} は 計上していません<br><br>` +
    `<strong>賃貸</strong><br>` +
    `家賃 (${period}年分): ${fmt(rentPaid)}<br>` +
    `更新料: ${fmt(renewPaid)}<br>` +
    `初期費用: ${fmt(moveCost)}`;
};
""",
    "<dt>持ち家の 残価値は？</dt><dd>本ツールは 比較を シンプルに するため 残価値を 計上していません。30年後 物件価値が 元の 30% (約1200万) 残れば、その分 持ち家が 有利に なります。立地 次第。</dd><dt>団信・税制 優遇は？</dt><dd>住宅ローン には 団信 (死亡で 残債ゼロ)・住宅ローン控除 (年最大40万円×13年 = 約500万円) があります。これらを 加味すると 持ち家が より 有利に。</dd>",
))


# ---------- 49. 教育費 総額 ----------
TOOLS.append((
    "education-cost", "🎓", "教育費 総額 (幼〜大学・公立私立 別)",
    "保育園〜大学までの 教育費 総額を 進路 シナリオ別 に 即時表示。",
    """    <p class="cap">お子さん 1人あたりの 教育費 総額を 算出します。文科省「学習費調査」「学生生活調査」 ベース。</p>
    <label>保育園 / 幼稚園:</label>
    <select id="hoiku" class="in">
      <option value="0" selected>公立 (3〜5歳 無償)</option>
      <option value="1500000">私立 幼稚園 (3年)</option>
    </select>
    <label>小学校 (6年):</label>
    <select id="sho" class="in">
      <option value="2110000" selected>公立 小学校</option>
      <option value="10000000">私立 小学校</option>
    </select>
    <label>中学校 (3年):</label>
    <select id="chu" class="in">
      <option value="1620000" selected>公立 中学校</option>
      <option value="4300000">私立 中学校</option>
    </select>
    <label>高校 (3年):</label>
    <select id="ko" class="in">
      <option value="1540000" selected>公立 高校</option>
      <option value="3160000">私立 高校</option>
    </select>
    <label>大学 (4年):</label>
    <select id="dai" class="in">
      <option value="0">進学 しない</option>
      <option value="2440000">国公立 大学 (自宅)</option>
      <option value="4470000" selected>私立文系 (自宅)</option>
      <option value="6240000">私立理系 (自宅)</option>
      <option value="3500000">国公立 (一人暮らし)</option>
      <option value="6500000">私立文系 (一人暮らし)</option>
      <option value="8500000">私立医歯薬 (6年・自宅)</option>
      <option value="20000000">私立医歯薬 (6年・一人暮らし)</option>
    </select>
    <label>習い事・塾 (小〜高・年平均 月額 円):</label>
    <input id="extra" class="in" type="number" value="20000" />
    <div class="bar"><button type="button" class="btn primary" id="calc">総額を 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="total" style="color:#c00;">¥0</div><div class="cap">22歳までの 総額</div></div>
      <div class="cell"><div class="num" id="monthly">¥0</div><div class="cap">月平均 (22年で)</div></div>
    </div>
    <h2>内訳</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const items = ['hoiku', 'sho', 'chu', 'ko', 'dai'];
  const labels = ['保育・幼稚園', '小学校(6年)', '中学校(3年)', '高校(3年)', '大学(4年)'];
  const periods = [3, 6, 3, 3, 4]; // 年数
  let total = 0;
  let detail = '';
  for (let i = 0; i < items.length; i++) {
    const v = parseFloat(document.getElementById(items[i]).value) || 0;
    total += v;
    detail += `${labels[i]}: ¥${v.toLocaleString('ja-JP')}<br>`;
  }
  // 塾・習い事 (小1〜高3 = 12年)
  const extra = parseFloat(document.getElementById('extra').value) || 0;
  const extraTotal = extra * 12 * 12;
  total += extraTotal;
  detail += `習い事・塾 (12年): ¥${extraTotal.toLocaleString('ja-JP')}<br>`;
  document.getElementById('total').textContent = '¥' + total.toLocaleString('ja-JP');
  document.getElementById('monthly').textContent = '¥' + Math.round(total / 22 / 12).toLocaleString('ja-JP') + '/月';
  document.getElementById('detail').innerHTML = detail;
};
""",
    "<dt>「教育費 2000万円」 って 本当？</dt><dd>すべて 公立 + 国公立大 自宅 で 約1000万円。中学から 私立 + 私立大文系で 約1500-1800万円。私立医学部 まで 含むと 3000-4000万円。本ツールで シナリオ別 確認できます。</dd><dt>奨学金は？</dt><dd>日本学生支援機構 (JASSO) で 月3-6万円が 一般的。返済 必要 (利子型・無利子型)。給付型 (返済不要) もあるが 所得制限 厳しい。</dd>",
))


# ---------- 50. 老後資金 必要額 ----------
TOOLS.append((
    "retirement-fund", "🌅", "老後資金 必要額 (2000万円問題)",
    "想定 生活費・年金から 老後 必要 資金を 算出。「2000万円 問題」 の 真相を 自分の 数字で。",
    """    <label>現在の 年齢:</label>
    <input id="cur" class="in" type="number" value="45" />
    <label>引退 予定 年齢:</label>
    <input id="retire" class="in" type="number" value="65" />
    <label>想定 寿命 (女性平均 87・男性平均 81):</label>
    <input id="life" class="in" type="number" value="90" />
    <label>引退後 月の 生活費 (夫婦・円):</label>
    <input id="cost" class="in" type="number" value="270000" />
    <label>年金 月額 (夫婦 合計・概算):</label>
    <input id="pension" class="in" type="number" value="220000" />
    <label>現在の 貯蓄 (円):</label>
    <input id="savings" class="in" type="number" value="5000000" />
    <label>今後 月 積立 額 (円):</label>
    <input id="invest" class="in" type="number" value="50000" />
    <label>運用 利回り (年率%):</label>
    <input id="growth" class="in" type="number" step="0.5" value="3" />
    <div class="bar"><button type="button" class="btn primary" id="calc">シミュレート</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="need" style="color:#c00;">¥0</div><div class="cap">引退時 必要 額</div></div>
      <div class="cell"><div class="num" id="future" style="color:#16a34a;">¥0</div><div class="cap">引退時 予測 資産</div></div>
      <div class="cell"><div class="num" id="gap">¥0</div><div class="cap">過不足</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;font-weight:bold;"></p>
""",
    """
document.getElementById('calc').onclick = () => {
  const cur = parseFloat(document.getElementById('cur').value) || 0;
  const retire = parseFloat(document.getElementById('retire').value) || 0;
  const life = parseFloat(document.getElementById('life').value) || 0;
  const cost = parseFloat(document.getElementById('cost').value) || 0;
  const pension = parseFloat(document.getElementById('pension').value) || 0;
  const savings = parseFloat(document.getElementById('savings').value) || 0;
  const invest = parseFloat(document.getElementById('invest').value) || 0;
  const growth = (parseFloat(document.getElementById('growth').value) || 0) / 100 / 12;
  const yearsToRetire = retire - cur;
  const yearsRetired = life - retire;
  // 引退時 必要額: 月赤字 × 12 × 引退後年数
  const monthlyGap = Math.max(0, cost - pension);
  const need = monthlyGap * 12 * yearsRetired;
  // 引退時 予測 資産 (複利・月次)
  const months = yearsToRetire * 12;
  const FV_savings = growth === 0 ? savings : savings * Math.pow(1 + growth, months);
  const FV_invest = growth === 0 ? invest * months : invest * (Math.pow(1 + growth, months) - 1) / growth;
  const future = FV_savings + FV_invest;
  const gap = future - need;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('need').textContent = fmt(need);
  document.getElementById('future').textContent = fmt(future);
  document.getElementById('gap').textContent = (gap >= 0 ? '+' : '') + fmt(gap);
  const msg = document.getElementById('msg');
  if (gap >= 0) {
    msg.style.color = '#16a34a';
    msg.textContent = `✅ ${fmt(gap)} 黒字。安心。`;
  } else {
    msg.style.color = '#c00';
    const addMonth = (-gap / months) | 0;
    msg.textContent = `⚠️ ${fmt(-gap)} 不足。あと 月 ${fmt(addMonth)} 追加積立で 解決。`;
  }
};
""",
    "<dt>「2000万円問題」 の 真相は？</dt><dd>2019年 金融庁 報告書 で 「夫婦の 老後 30年で 約2000万円 不足」 と され、話題に。これは 「月5万円 赤字 × 30年」 の 単純計算。生活費・年金で 数字は 大きく 変動します。</dd><dt>運用 利回り 3% は 現実的？</dt><dd>NISA で 全世界株式 を 30年 積立てた 過去実績で 平均 5-7%。慎重 見積もりで 3%、強気で 5% が 妥当。</dd>",
))


# =========================================================================
# J. 健康・暮らし シリーズ
# =========================================================================

# ---------- 51. 基礎代謝・PFC ----------
TOOLS.append((
    "metabolism", "🔥", "基礎代謝 + PFC バランス (ダイエット用)",
    "Harris-Benedict 式で 基礎代謝・1日必要カロリー・PFC バランスを 算出。ダイエット 計画に。",
    """    <label>性別:</label>
    <select id="sex" class="in">
      <option value="m" selected>男性</option>
      <option value="f">女性</option>
    </select>
    <label>年齢:</label>
    <input id="age" class="in" type="number" value="30" />
    <label>身長 (cm):</label>
    <input id="height" class="in" type="number" value="170" />
    <label>体重 (kg):</label>
    <input id="weight" class="in" type="number" value="70" />
    <label>活動 レベル:</label>
    <select id="activity" class="in">
      <option value="1.2">座り仕事 中心 (ほぼ運動なし)</option>
      <option value="1.375">軽い 運動 (週1-3 軽い 運動)</option>
      <option value="1.55" selected>中程度 (週3-5 適度な 運動)</option>
      <option value="1.725">活発 (週6-7 激しい 運動)</option>
      <option value="1.9">非常に 活発 (体力 仕事 + 毎日 運動)</option>
    </select>
    <label>目的:</label>
    <select id="goal" class="in">
      <option value="0" selected>現状 維持</option>
      <option value="-500">減量 (月 約2kg減 = -500kcal/日)</option>
      <option value="-300">緩い減量 (月 約1kg減)</option>
      <option value="300">緩い 増量</option>
      <option value="500">バルクアップ (筋肥大)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="bmr">0</div><div class="cap">基礎代謝</div></div>
      <div class="cell"><div class="num" id="tdee">0</div><div class="cap">1日消費 (TDEE)</div></div>
      <div class="cell"><div class="num" id="target" style="color:#16a34a;">0</div><div class="cap">目標 摂取</div></div>
    </div>
    <h2>PFC バランス (推奨)</h2>
    <div class="cards">
      <div class="cell"><div class="num" id="p">0g</div><div class="cap">タンパク質 (P)</div></div>
      <div class="cell"><div class="num" id="f">0g</div><div class="cap">脂質 (F)</div></div>
      <div class="cell"><div class="num" id="c">0g</div><div class="cap">炭水化物 (C)</div></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const sex = document.getElementById('sex').value;
  const age = parseFloat(document.getElementById('age').value) || 0;
  const h = parseFloat(document.getElementById('height').value) || 0;
  const w = parseFloat(document.getElementById('weight').value) || 0;
  const act = parseFloat(document.getElementById('activity').value);
  const goal = parseFloat(document.getElementById('goal').value);
  // Harris-Benedict (改訂版)
  let bmr;
  if (sex === 'm') bmr = 88.362 + 13.397 * w + 4.799 * h - 5.677 * age;
  else bmr = 447.593 + 9.247 * w + 3.098 * h - 4.330 * age;
  const tdee = bmr * act;
  const target = tdee + goal;
  document.getElementById('bmr').textContent = Math.round(bmr) + ' kcal';
  document.getElementById('tdee').textContent = Math.round(tdee) + ' kcal';
  document.getElementById('target').textContent = Math.round(target) + ' kcal';
  // PFC: 減量時は P高め, 増量時は C高め
  let pRatio, fRatio, cRatio;
  if (goal < 0) { pRatio = 0.30; fRatio = 0.25; cRatio = 0.45; } // 減量
  else if (goal > 0) { pRatio = 0.25; fRatio = 0.20; cRatio = 0.55; } // 増量
  else { pRatio = 0.20; fRatio = 0.25; cRatio = 0.55; }
  document.getElementById('p').textContent = Math.round(target * pRatio / 4) + 'g';
  document.getElementById('f').textContent = Math.round(target * fRatio / 9) + 'g';
  document.getElementById('c').textContent = Math.round(target * cRatio / 4) + 'g';
};
""",
    "<dt>PFC は 何の 略？</dt><dd>P=Protein (タンパク質, 4kcal/g)、F=Fat (脂質, 9kcal/g)、C=Carbohydrate (炭水化物, 4kcal/g)。ダイエットは PFC バランス が 成功の カギ。</dd><dt>月 2kg減 は 速い？</dt><dd>体重 70kg なら 月 -2kg (約 -2.8%) が 健康的な 上限。これ以上 だと 筋肉 減少・リバウンド リスク。</dd>",
))


# ---------- 52. 保育料 概算 ----------
TOOLS.append((
    "daycare-cost", "🧒", "保育料 概算 (認可保育所・自治体平均)",
    "世帯年収・子供年齢から 認可保育所の 保育料を 概算 (自治体平均)。",
    """    <label>世帯 年収 (額面 合計・万円):</label>
    <input id="income" class="in" type="number" value="600" />
    <label>子供の 年齢:</label>
    <select id="age" class="in">
      <option value="0" selected>0歳児</option>
      <option value="1">1歳児</option>
      <option value="2">2歳児</option>
      <option value="3">3歳児 (無償化 対象)</option>
      <option value="4">4歳児 (無償化 対象)</option>
      <option value="5">5歳児 (無償化 対象)</option>
    </select>
    <label>保育時間:</label>
    <select id="time" class="in">
      <option value="full" selected>標準時間 (11時間)</option>
      <option value="short">短時間 (8時間)</option>
    </select>
    <label>同時 在園 (兄弟・姉妹) の 数:</label>
    <select id="siblings" class="in">
      <option value="0" selected>なし (本人 のみ)</option>
      <option value="1">兄姉 1人 (本人 半額)</option>
      <option value="2">兄姉 2人 (本人 無料)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">概算 表示</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="monthly" style="color:#16a34a;">¥0</div><div class="cap">月額</div></div>
      <div class="cell"><div class="num" id="yearly">¥0</div><div class="cap">年額</div></div>
    </div>
    <p id="msg" class="note" style="font-size:15px;"></p>
    <p class="cap">※ 自治体差が 非常に 大きい (同じ年収でも 倍以上 違うことも)。お住まいの 市区町村の HP で 確認を。</p>
""",
    """
document.getElementById('calc').onclick = () => {
  const income = parseFloat(document.getElementById('income').value) || 0;
  const age = parseInt(document.getElementById('age').value, 10);
  const fullTime = document.getElementById('time').value === 'full';
  const siblings = parseInt(document.getElementById('siblings').value, 10);
  // 3-5歳 は 無償化
  if (age >= 3) {
    document.getElementById('monthly').textContent = '¥0';
    document.getElementById('yearly').textContent = '¥0';
    document.getElementById('msg').textContent = '✅ 3-5歳 は 幼児教育・保育 無償化 対象。給食費・教材費 等の 実費 (月数千円) は 別途必要。';
    return;
  }
  // 0-2歳児 自治体 平均 (世帯年収 帯別)
  let base;
  if (income < 300) base = 8000;
  else if (income < 470) base = 18000;
  else if (income < 600) base = 35000;
  else if (income < 800) base = 50000;
  else if (income < 1000) base = 65000;
  else if (income < 1200) base = 75000;
  else base = 85000;
  if (!fullTime) base *= 0.95;
  if (siblings === 1) base *= 0.50;
  else if (siblings >= 2) base = 0;
  const monthly = Math.round(base / 100) * 100;
  document.getElementById('monthly').textContent = '¥' + monthly.toLocaleString('ja-JP');
  document.getElementById('yearly').textContent = '¥' + (monthly * 12).toLocaleString('ja-JP');
  const msg = document.getElementById('msg');
  if (monthly < 20000) msg.textContent = '💡 低所得帯 / 兄姉 多数 で 安価。';
  else if (monthly < 50000) msg.textContent = '✅ 標準的な 保育料 水準。';
  else msg.textContent = '🔥 高所得帯。認証保育所・企業内 保育 等の 比較も。';
};
""",
    "<dt>幼児教育 無償化の 対象は？</dt><dd>3-5歳児 (年少〜年長) の 認可保育所・幼稚園・認定こども園 が 月額 上限なし で 無償。0-2歳は 住民税 非課税 世帯のみ 無償。</dd><dt>認証保育所 / 認可外は？</dt><dd>無償化 対象だが 月額 上限あり (3-5歳 月3.7万円、0-2歳 非課税世帯のみ 月4.2万円 まで)。超過分は 自己負担。</dd>",
))


# ---------- 53. 車 維持費 年間 ----------
TOOLS.append((
    "car-cost", "🚙", "車 維持費 年間 (税・保険・車検・ガソリン)",
    "車種・走行距離から 年間 維持費を 一括計算。「車を 持つと いくら？」 の 答えを 即時。",
    """    <label>車種:</label>
    <select id="type" class="in">
      <option value="kei">軽自動車 (660cc以下)</option>
      <option value="compact" selected>コンパクト・1.5Lクラス</option>
      <option value="mid">2.0L クラス</option>
      <option value="large">2.5L 以上・SUV</option>
      <option value="luxury">高級車 (3.0L超)</option>
    </select>
    <label>年間 走行 距離 (km):</label>
    <input id="km" class="in" type="number" value="10000" />
    <label>燃費 (km/L):</label>
    <input id="kmpl" class="in" type="number" step="0.1" value="18" />
    <label>ガソリン 単価 (円/L):</label>
    <input id="gas" class="in" type="number" value="175" />
    <label>駐車場 月額 (持ち家は 0 円):</label>
    <input id="parking" class="in" type="number" value="15000" />
    <label>任意保険 年額 (年齢・等級で 大きく 変動):</label>
    <input id="insurance" class="in" type="number" value="60000" />
    <div class="bar"><button type="button" class="btn primary" id="calc">年間 維持費</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="yearly" style="color:#c00;">¥0</div><div class="cap">年間 合計</div></div>
      <div class="cell"><div class="num" id="monthly">¥0</div><div class="cap">月平均</div></div>
    </div>
    <h2>内訳 (年間)</h2>
    <div id="detail" class="cap" style="font-size:14px;line-height:1.8;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const type = document.getElementById('type').value;
  const km = parseFloat(document.getElementById('km').value) || 0;
  const kmpl = parseFloat(document.getElementById('kmpl').value) || 1;
  const gas = parseFloat(document.getElementById('gas').value) || 0;
  const parking = parseFloat(document.getElementById('parking').value) || 0;
  const insurance = parseFloat(document.getElementById('insurance').value) || 0;
  // 自動車税 (年額)
  const tax = {kei: 10800, compact: 30500, mid: 39500, large: 51000, luxury: 88000}[type];
  // 自賠責 (年換算 = 2年分 / 2)
  const jibai = {kei: 11000, compact: 12500, mid: 12500, large: 12500, luxury: 12500}[type];
  // 車検 (2年に1回・年換算): 法定費用 + 整備
  const shaken_total = {kei: 60000, compact: 80000, mid: 100000, large: 130000, luxury: 180000}[type];
  const shaken = shaken_total / 2;
  // ガソリン代
  const fuel = (km / kmpl) * gas;
  // 駐車場
  const park_yearly = parking * 12;
  // メンテ (タイヤ・オイル・洗車 等)
  const maint = {kei: 30000, compact: 40000, mid: 50000, large: 60000, luxury: 80000}[type];
  const total = tax + jibai + shaken + fuel + park_yearly + insurance + maint;
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('yearly').textContent = fmt(total);
  document.getElementById('monthly').textContent = fmt(total / 12);
  document.getElementById('detail').innerHTML =
    `自動車税: ${fmt(tax)}<br>` +
    `自賠責 保険 (年換算): ${fmt(jibai)}<br>` +
    `車検 (年換算): ${fmt(shaken)}<br>` +
    `任意保険: ${fmt(insurance)}<br>` +
    `ガソリン代 (${km.toLocaleString('ja-JP')}km × ${gas}円÷${kmpl}km/L): ${fmt(fuel)}<br>` +
    `駐車場 (年): ${fmt(park_yearly)}<br>` +
    `メンテナンス (タイヤ・オイル・洗車 等): ${fmt(maint)}<br>` +
    `<strong>合計: ${fmt(total)}/年</strong>`;
};
""",
    "<dt>カーシェア vs 車保有 どっち？</dt><dd>本ツールの 年間合計 / 12 で 月コスト を 出し、カーシェア利用予定 時間 × 料金 (タイムズ 220円/15分) と 比較。月20時間 以下なら カーシェア有利。</dd><dt>EV/HV だと 安い？</dt><dd>HV は ガソリン代 が 30-40% 減。EV は 電気代 < ガソリン代 ですが 車両価格 が 高い + 充電インフラ 課題。本ツールで 燃費 25-40 km/L 設定すると HV シミュ 可能。</dd>",
))


# ---------- 54. 携帯プラン 比較 ----------
TOOLS.append((
    "mobile-plan", "📱", "携帯 月額 最適化 (格安SIM 比較)",
    "通信量・通話量から 最適な 携帯プランを 提案。3大キャリア vs 格安 SIM の 差を 即時表示。",
    """    <label>月の データ 通信量 (GB):</label>
    <select id="data" class="in">
      <option value="1">1GB 以下 (LINE・メール 中心)</option>
      <option value="3" selected>3GB (SNS・地図 程度)</option>
      <option value="10">10GB (動画 そこそこ)</option>
      <option value="20">20GB (動画 たくさん)</option>
      <option value="50">50GB 以上 (テザリング・PC接続)</option>
      <option value="999">無制限</option>
    </select>
    <label>月の 通話 時間 (分):</label>
    <select id="call" class="in">
      <option value="0" selected>ほぼ なし (LINE通話 中心)</option>
      <option value="30">30分 程度</option>
      <option value="60">60分 程度</option>
      <option value="120">120分 程度</option>
      <option value="999">無制限 必須</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="calc">最適 プラン 表示</button></div>
    <div id="result"></div>
    <h2>主要 プラン (2026年6月時点)</h2>
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <tr style="background:#f1f5f9;"><th>プラン</th><th>データ</th><th>通話</th><th>月額</th></tr>
      <tr><td>povo (au)</td><td>使った分 トッピング</td><td>5分通話 別途</td><td>基本0円〜</td></tr>
      <tr><td>ahamo (docomo)</td><td>30GB</td><td>5分以内 込み</td><td>2,970円</td></tr>
      <tr><td>LINEMO (SoftBank)</td><td>20GB / 30GB</td><td>別途</td><td>2,090円 / 2,970円</td></tr>
      <tr><td>楽天モバイル</td><td>無制限</td><td>無料 (Rakuten Link)</td><td>3,278円 (20GB超〜)</td></tr>
      <tr><td>mineo</td><td>5GB</td><td>別途</td><td>1,518円</td></tr>
      <tr><td>IIJmio</td><td>5GB</td><td>別途</td><td>990円</td></tr>
      <tr><td>大手 (docomo eximo)</td><td>無制限</td><td>5分以内 込み</td><td>7,315円</td></tr>
    </table>
""",
    """
document.getElementById('calc').onclick = () => {
  const data = parseFloat(document.getElementById('data').value);
  const call = parseFloat(document.getElementById('call').value);
  const plans = [];
  // 通話 無制限 必須の 場合
  if (call >= 999) {
    plans.push({name: '楽天モバイル (Rakuten Link)', price: data >= 999 ? 3278 : 2178, note: 'データ無制限+通話無料'});
    plans.push({name: '大手キャリア 通話無制限オプション', price: 7000, note: '安心の品質'});
  } else if (data <= 1) {
    plans.push({name: 'povo (基本0円+トッピング)', price: 400, note: '電話番号 維持なら 最安'});
    plans.push({name: 'IIJmio (2GB)', price: 850, note: '5G 対応'});
    plans.push({name: 'mineo マイそく (300kbps)', price: 250, note: '低速 だが 月250円'});
  } else if (data <= 3) {
    plans.push({name: 'IIJmio (5GB)', price: 990, note: '最安レベル'});
    plans.push({name: 'mineo (5GB)', price: 1518, note: 'eo光 とセットで さらに 割引'});
    plans.push({name: 'OCNモバイル (3GB)', price: 990, note: 'NTT系で 安心'});
  } else if (data <= 10) {
    plans.push({name: 'IIJmio (10GB)', price: 1500, note: 'コスパ最強'});
    plans.push({name: 'LINEMO ベストプランV (10GB)', price: 2090, note: 'SoftBank 品質'});
    plans.push({name: 'mineo (10GB)', price: 1958, note: 'パケット繰越 OK'});
  } else if (data <= 20) {
    plans.push({name: 'LINEMO (20GB)', price: 2728, note: 'SoftBank サブブランド'});
    plans.push({name: '楽天モバイル', price: 2178, note: '〜20GBは 2,178円'});
    plans.push({name: 'ahamo (30GB)', price: 2970, note: '5分通話込み'});
  } else if (data <= 50) {
    plans.push({name: 'ahamo (30GB+大盛り80GB)', price: 4950, note: '計100GB'});
    plans.push({name: '楽天モバイル (無制限)', price: 3278, note: '一番 お得'});
    plans.push({name: 'povo (60GB/90日)', price: 2700, note: '実質 月900円相当'});
  } else {
    plans.push({name: '楽天モバイル (無制限)', price: 3278, note: '無制限の 最安'});
    plans.push({name: 'ahamo 大盛り (100GB)', price: 4950, note: 'docomo品質'});
    plans.push({name: '大手 無制限プラン', price: 7315, note: '安定だが 高め'});
  }
  // 通話 30分以上 必要なら 5分通話オプション追加
  if (call >= 30 && call < 999) {
    for (const p of plans) {
      if (!p.note.includes('5分通話込み') && !p.note.includes('Rakuten Link')) {
        p.price += 550;
        p.note += ' + 5分通話 オプション';
      }
    }
  }
  plans.sort((a, b) => a.price - b.price);
  let html = '<h2>あなたに 最適な プラン (安い 順)</h2><div class="cards">';
  for (let i = 0; i < plans.length; i++) {
    const p = plans[i];
    const isBest = i === 0;
    html += `<div class="cell" style="text-align:left;${isBest ? 'background:#dcfce7;' : ''}">` +
      `<div style="font-weight:bold;font-size:16px;">${isBest ? '🥇 ' : ''}${p.name}</div>` +
      `<div class="num" style="color:${isBest ? '#16a34a' : '#1d9bf0'};">¥${p.price.toLocaleString('ja-JP')}/月</div>` +
      `<div class="cap">${p.note}</div></div>`;
  }
  html += '</div>';
  // 大手と 比較
  const bigCarrier = 7315;
  const saving = (bigCarrier - plans[0].price) * 12;
  if (saving > 0) html += `<p class="note" style="font-size:16px;color:#16a34a;font-weight:bold;">💰 大手キャリアから 乗換で 年 ¥${saving.toLocaleString('ja-JP')} 節約！</p>`;
  document.getElementById('result').innerHTML = html;
};
""",
    "<dt>大手キャリアの 違いは？</dt><dd>料金は ほぼ 同じ (eximo・use・ペイトク など 5500-7500円)。サブブランド (ahamo, povo, LINEMO) は 半額以下。MVNO (IIJ, mineo, OCN) は さらに 安いが ピーク時 速度低下 あり。</dd><dt>乗り換え方法は？</dt><dd>MNP (番号 そのまま) で 数日〜即時。Web申込で 大手手数料 (3300円) も 多くは 無料化。違約金は 2022年以降 ほぼ 撤廃。</dd>",
))


# ---------- 55. 健康診断 数値判定 ----------
TOOLS.append((
    "health-check", "🩺", "健康診断 数値 判定 (信号 表示)",
    "血圧・血糖・コレステロール・肝機能 等の 数値を 入力すると 基準値 と 信号 (青/黄/赤) で 判定。",
    """    <p class="cap">気になる 項目だけ 入力。空欄は 判定 しません。</p>
    <h2>血圧 (mmHg)</h2>
    <label>上 (収縮期):</label>
    <input id="bpHigh" class="in" type="number" placeholder="例: 130" />
    <label>下 (拡張期):</label>
    <input id="bpLow" class="in" type="number" placeholder="例: 85" />
    <h2>血糖・糖尿 リスク</h2>
    <label>空腹時 血糖 (mg/dL):</label>
    <input id="glucose" class="in" type="number" placeholder="例: 100" />
    <label>HbA1c (%):</label>
    <input id="hba1c" class="in" type="number" step="0.1" placeholder="例: 5.8" />
    <h2>脂質</h2>
    <label>LDL コレステロール (mg/dL):</label>
    <input id="ldl" class="in" type="number" placeholder="例: 130" />
    <label>HDL コレステロール (mg/dL):</label>
    <input id="hdl" class="in" type="number" placeholder="例: 50" />
    <label>中性脂肪 (mg/dL):</label>
    <input id="tg" class="in" type="number" placeholder="例: 120" />
    <h2>肝機能</h2>
    <label>AST (GOT) U/L:</label>
    <input id="ast" class="in" type="number" placeholder="例: 25" />
    <label>ALT (GPT) U/L:</label>
    <input id="alt" class="in" type="number" placeholder="例: 30" />
    <label>γ-GTP U/L:</label>
    <input id="ggt" class="in" type="number" placeholder="例: 40" />
    <h2>尿酸</h2>
    <label>尿酸値 (mg/dL):</label>
    <input id="ua" class="in" type="number" step="0.1" placeholder="例: 5.5" />
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result"></div>
    <p class="note" style="font-size:14px;">※ 一般的な 基準値 (日本人間ドック学会 等) を 採用。性別・年齢・他疾患 で 適正値は 変わります。気になる 数値は 医師 相談を。</p>
""",
    """
function judge(val, ranges) {
  if (val == null || isNaN(val)) return null;
  for (const r of ranges) {
    if (val >= r.min && val < r.max) return {level: r.level, label: r.label};
  }
  return null;
}
const RULES = {
  bpHigh: [{min: 0, max: 120, level: 'green', label: '正常'}, {min: 120, max: 130, level: 'yellow', label: '正常高値'}, {min: 130, max: 140, level: 'yellow', label: '高値血圧'}, {min: 140, max: 9999, level: 'red', label: '高血圧'}],
  bpLow: [{min: 0, max: 80, level: 'green', label: '正常'}, {min: 80, max: 85, level: 'yellow', label: '正常高値'}, {min: 85, max: 90, level: 'yellow', label: '高値'}, {min: 90, max: 9999, level: 'red', label: '高血圧'}],
  glucose: [{min: 0, max: 100, level: 'green', label: '正常'}, {min: 100, max: 110, level: 'yellow', label: '境界'}, {min: 110, max: 126, level: 'yellow', label: '境界'}, {min: 126, max: 9999, level: 'red', label: '糖尿病 疑い'}],
  hba1c: [{min: 0, max: 5.6, level: 'green', label: '正常'}, {min: 5.6, max: 6.0, level: 'yellow', label: '境界'}, {min: 6.0, max: 6.5, level: 'yellow', label: '境界'}, {min: 6.5, max: 99, level: 'red', label: '糖尿病'}],
  ldl: [{min: 0, max: 120, level: 'green', label: '正常'}, {min: 120, max: 140, level: 'yellow', label: '境界'}, {min: 140, max: 9999, level: 'red', label: '高LDL'}],
  hdl: [{min: 0, max: 40, level: 'red', label: '低HDL'}, {min: 40, max: 9999, level: 'green', label: '正常'}],
  tg: [{min: 0, max: 150, level: 'green', label: '正常'}, {min: 150, max: 300, level: 'yellow', label: '境界〜高値'}, {min: 300, max: 9999, level: 'red', label: '高TG'}],
  ast: [{min: 0, max: 31, level: 'green', label: '正常'}, {min: 31, max: 51, level: 'yellow', label: '軽度高値'}, {min: 51, max: 9999, level: 'red', label: '高値'}],
  alt: [{min: 0, max: 31, level: 'green', label: '正常'}, {min: 31, max: 51, level: 'yellow', label: '軽度高値'}, {min: 51, max: 9999, level: 'red', label: '高値'}],
  ggt: [{min: 0, max: 51, level: 'green', label: '正常'}, {min: 51, max: 101, level: 'yellow', label: '軽度高値'}, {min: 101, max: 9999, level: 'red', label: '高値'}],
  ua: [{min: 0, max: 7.0, level: 'green', label: '正常'}, {min: 7.0, max: 8.0, level: 'yellow', label: '高尿酸'}, {min: 8.0, max: 99, level: 'red', label: '痛風リスク'}],
};
const LABELS = {bpHigh: '血圧 (上)', bpLow: '血圧 (下)', glucose: '空腹時 血糖', hba1c: 'HbA1c', ldl: 'LDL', hdl: 'HDL', tg: '中性脂肪', ast: 'AST', alt: 'ALT', ggt: 'γ-GTP', ua: '尿酸'};
const COLORS = {green: '#16a34a', yellow: '#e67e22', red: '#c00'};
const BGS = {green: '#dcfce7', yellow: '#fef3c7', red: '#fee2e2'};
document.getElementById('calc').onclick = () => {
  let html = '<div class="cards">';
  let any = false, hasRed = false;
  for (const key of Object.keys(RULES)) {
    const v = parseFloat(document.getElementById(key).value);
    if (isNaN(v)) continue;
    const j = judge(v, RULES[key]);
    if (!j) continue;
    any = true;
    if (j.level === 'red') hasRed = true;
    html += `<div class="cell" style="background:${BGS[j.level]};text-align:left;">` +
      `<div style="font-weight:bold;">${LABELS[key]}: ${v}</div>` +
      `<div class="num" style="color:${COLORS[j.level]};">${j.label}</div></div>`;
  }
  html += '</div>';
  if (!any) html = '<p>判定する 数値が ありません。気になる 項目を 入力してください。</p>';
  else if (hasRed) html += '<p class="note" style="color:#c00;font-weight:bold;">⚠️ 赤判定 あり。医師 相談を おすすめします。</p>';
  document.getElementById('result').innerHTML = html;
};
""",
    "<dt>基準値は 何 ベース？</dt><dd>日本人間ドック学会・日本動脈硬化学会・日本高血圧学会 等の 公開基準 (2024時点)。海外と 異なる 場合あり。</dd><dt>「境界」 と 言われたら？</dt><dd>「すぐ 治療」 ではないが 生活習慣 改善 推奨。3-6ヶ月後の 再検査で 数値 変動を 確認。改善しなければ 医師 相談。</dd>",
))


# =========================================================================
# K. バイラル系 (アクセス爆発 狙い)
# =========================================================================

# ---------- 56. MBTI 簡易診断 ----------
TOOLS.append((
    "mbti", "🧠", "MBTI 16タイプ 簡易診断 (8問)",
    "8つの 質問に 答えるだけで 16タイプの 性格を 判定。INTJ・ENFP 等 シェア用 結果も。",
    """    <div id="quiz">
      <p class="lead">直感で 答えてください (各 質問 2択)。</p>
      <div id="questions"></div>
      <div class="bar"><button type="button" class="btn primary" id="judge">診断結果を 表示</button></div>
    </div>
    <div id="result" style="display:none;"></div>
""",
    """
const Q = [
  {q: '休日の 過ごし方は?', a: ['友達と 外出 (E)', '一人で 家 (I)'], dim: 'EI'},
  {q: '初対面の 人と話すと?', a: ['元気に なる (E)', '疲れる (I)'], dim: 'EI'},
  {q: '物事を 判断 する 時に 重視するのは?', a: ['事実・データ (S)', '可能性・直感 (N)'], dim: 'SN'},
  {q: '本を 読むなら?', a: ['実用書・ノンフィクション (S)', '小説・哲学 (N)'], dim: 'SN'},
  {q: '判断の 基準は?', a: ['論理・正しさ (T)', '気持ち・調和 (F)'], dim: 'TF'},
  {q: '友達の 悩みを 聞いた時 まず?', a: ['解決策を 提示 (T)', '共感・寄り添う (F)'], dim: 'TF'},
  {q: '計画は?', a: ['細かく 立てる (J)', '臨機応変・流れで (P)'], dim: 'JP'},
  {q: '締切が ある仕事は?', a: ['早めに 終わらせる (J)', 'ギリギリで 集中 (P)'], dim: 'JP'},
];
const $q = document.getElementById('questions');
Q.forEach((q, i) => {
  const div = document.createElement('div');
  div.style.margin = '20px 0';
  div.innerHTML = `<p style="font-weight:bold;">${i+1}. ${q.q}</p>` +
    q.a.map((a, ai) => `<label style="display:block;margin:6px 0;"><input type="radio" name="q${i}" value="${ai}" ${ai===0?'checked':''}> ${a}</label>`).join('');
  $q.appendChild(div);
});
const TYPES = {
  ISTJ: {name: '管理者', desc: '責任感が 強く、現実的で 信頼される 実務派。秩序と 伝統を 重んじる。', good: 'ESFP, ESTP'},
  ISFJ: {name: '擁護者', desc: '献身的で 思いやりが あり、周囲を 細やかに サポート。', good: 'ESFP, ESTP'},
  INFJ: {name: '提唱者', desc: '理想主義で 洞察力が 鋭く、人を 深く 理解。希少な タイプ。', good: 'ENFP, ENTP'},
  INTJ: {name: '建築家', desc: '戦略的思考の 持ち主。独立心が 強く、目標達成に 向けて 体系的に 動く。', good: 'ENFP, ENTP'},
  ISTP: {name: '巨匠', desc: '冷静で 実用的。問題解決が 得意で、機械や 道具を 使いこなす。', good: 'ESFJ, ENFJ'},
  ISFP: {name: '冒険家', desc: '芸術的感性が 豊か。柔軟で 平和を 愛し、自分の 価値観を 大事にする。', good: 'ESFJ, ENFJ'},
  INFP: {name: '仲介者', desc: '理想主義で 共感力が 高い。クリエイティブで 自分の 信念に 忠実。', good: 'ENFJ, ENTJ'},
  INTP: {name: '論理学者', desc: '理論を 好み、独創的。深く 考え、新しい アイデアを 生み出す。', good: 'ENFJ, ENTJ'},
  ESTP: {name: '起業家', desc: 'エネルギッシュで 行動派。今を 楽しみ、リスクを 恐れない。', good: 'ISFJ, ISTJ'},
  ESFP: {name: 'エンターテイナー', desc: '陽気で 人懐っこい。場を 盛り上げる 太陽のような 存在。', good: 'ISFJ, ISTJ'},
  ENFP: {name: '広報運動家', desc: '熱意と 創造性に 満ち、人を 鼓舞する。可能性の 探求者。', good: 'INFJ, INTJ'},
  ENTP: {name: '討論者', desc: '機知に 富み、議論好き。新しい アイデアと 挑戦を 求める。', good: 'INFJ, INTJ'},
  ESTJ: {name: '幹部', desc: '組織を まとめる 統率者。実務的で 効率を 重視する リーダー。', good: 'ISFP, ISTP'},
  ESFJ: {name: '領事', desc: '面倒見が 良く、社交的。周囲との 調和を 大切に する。', good: 'ISFP, ISTP'},
  ENFJ: {name: '主人公', desc: 'カリスマ性が あり、人を 励まし 導く 天性の リーダー。', good: 'INFP, INTP'},
  ENTJ: {name: '指揮官', desc: '大胆で 戦略的。目標達成に 向けて 周囲を 引っ張る タイプ。', good: 'INFP, INTP'},
};
document.getElementById('judge').onclick = () => {
  const scores = {EI: [0,0], SN: [0,0], TF: [0,0], JP: [0,0]};
  for (let i = 0; i < Q.length; i++) {
    const val = parseInt(document.querySelector(`input[name="q${i}"]:checked`).value, 10);
    scores[Q[i].dim][val]++;
  }
  const type =
    (scores.EI[0] > scores.EI[1] ? 'E' : 'I') +
    (scores.SN[0] > scores.SN[1] ? 'S' : 'N') +
    (scores.TF[0] > scores.TF[1] ? 'T' : 'F') +
    (scores.JP[0] > scores.JP[1] ? 'J' : 'P');
  const t = TYPES[type];
  document.getElementById('quiz').style.display = 'none';
  const $r = document.getElementById('result');
  $r.style.display = 'block';
  $r.innerHTML = `
    <div class="cell" style="text-align:center;padding:24px;background:#dcfce7;">
      <div style="font-size:48px;font-weight:bold;color:#16a34a;">${type}</div>
      <div style="font-size:24px;margin-top:8px;">${t.name}</div>
      <div class="cap" style="font-size:16px;margin-top:12px;line-height:1.6;">${t.desc}</div>
      <div class="cap" style="margin-top:16px;">💕 相性が 良い タイプ: ${t.good}</div>
    </div>
    <div class="bar" style="margin-top:16px;">
      <button type="button" class="btn primary" id="share">📋 結果を コピー</button>
      <button type="button" class="btn ghost" id="retry">もう一度</button>
    </div>`;
  document.getElementById('share').onclick = () => {
    const txt = `私の MBTI 診断結果は ${type} (${t.name}) でした! ${t.desc}`;
    navigator.clipboard.writeText(txt);
    document.getElementById('share').textContent = '✅ コピー しました';
  };
  document.getElementById('retry').onclick = () => location.reload();
};
""",
    "<dt>本物の MBTI と 違う？</dt><dd>本格的な 検査 (16Personalities 等) は 60-100問。本ツールは 8問の 簡易版なので 結果は ざっくり目安。詳細は 公式 検査を。</dd><dt>16タイプの 出現率は？</dt><dd>日本人 では ISTJ・ISFJ が 多めとされる。INFJ は 1-2%程度の 希少タイプ。</dd>",
))


# ---------- 57. 人生 残り時間 ----------
TOOLS.append((
    "life-time", "⏳", "人生の 残り時間 リアルタイム カウント",
    "生年月日 + 性別から 平均寿命までの 残り時間を 秒単位で カウント。今 この 瞬間を 大事に 思える ツール。",
    """    <label>生年月日:</label>
    <input id="birth" class="in" type="date" />
    <label>性別 (平均寿命 異なる):</label>
    <select id="sex" class="in">
      <option value="81">男性 (平均 81歳)</option>
      <option value="87" selected>女性 (平均 87歳)</option>
    </select>
    <div class="bar"><button type="button" class="btn primary" id="start">カウント 開始</button></div>
    <div id="result" style="display:none;text-align:center;margin-top:20px;">
      <div style="font-size:18px;color:#475569;">人生 残り (リアルタイム)</div>
      <div id="big" style="font-size:48px;font-weight:bold;color:#c00;font-variant-numeric:tabular-nums;margin:10px 0;">--</div>
      <div class="cards">
        <div class="cell"><div class="num" id="years">0</div><div class="cap">年</div></div>
        <div class="cell"><div class="num" id="days">0</div><div class="cap">日</div></div>
        <div class="cell"><div class="num" id="hours">0</div><div class="cap">時間</div></div>
      </div>
      <p id="lived" class="cap" style="margin-top:16px;font-size:15px;"></p>
      <p id="msg" class="note" style="font-size:16px;font-weight:bold;"></p>
      <div class="bar"><button type="button" class="btn primary" id="share">📋 結果を シェア</button></div>
    </div>
""",
    """
let timer = null, endTime = 0, birthTime = 0, lifeYears = 0;
document.getElementById('start').onclick = () => {
  const b = document.getElementById('birth').value;
  if (!b) { alert('生年月日を 入力してください'); return; }
  birthTime = new Date(b).getTime();
  lifeYears = parseFloat(document.getElementById('sex').value);
  endTime = birthTime + lifeYears * 365.25 * 24 * 3600 * 1000;
  document.getElementById('result').style.display = 'block';
  if (timer) clearInterval(timer);
  tick();
  timer = setInterval(tick, 1000);
};
function tick() {
  const now = Date.now();
  const remain = Math.max(0, endTime - now);
  const sec = Math.floor(remain / 1000);
  const years = Math.floor(sec / (365.25 * 24 * 3600));
  const days = Math.floor((sec % (365.25 * 24 * 3600)) / (24 * 3600));
  const hours = Math.floor((sec % (24 * 3600)) / 3600);
  const mins = Math.floor((sec % 3600) / 60);
  const secs = sec % 60;
  document.getElementById('big').textContent = `${years}年 ${days}日 ${String(hours).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
  document.getElementById('years').textContent = years + '年';
  document.getElementById('days').textContent = Math.floor(remain / (24 * 3600 * 1000)).toLocaleString('ja-JP') + '日';
  document.getElementById('hours').textContent = Math.floor(remain / (3600 * 1000)).toLocaleString('ja-JP') + '時間';
  const lived = (now - birthTime) / (1000 * 3600 * 24 * 365.25);
  document.getElementById('lived').textContent = `あなたは これまで ${lived.toFixed(2)}年 (${Math.floor((now - birthTime) / (1000 * 3600 * 24)).toLocaleString('ja-JP')}日) 生きてきました。`;
  const ratio = (now - birthTime) / (endTime - birthTime);
  const msg = document.getElementById('msg');
  if (ratio < 0.25) msg.textContent = '🌱 人生 序盤。可能性は 無限大。';
  else if (ratio < 0.5) msg.textContent = '🌳 人生 1/4 通過。今日が 一番 若い 日。';
  else if (ratio < 0.75) msg.textContent = '🌞 人生 折り返し 付近。後悔の 少ない 選択を。';
  else msg.textContent = '🌅 人生 後半戦。残り時間を 大事に。';
}
document.getElementById('share') && (document.getElementById('share').onclick = () => {
  const days = Math.floor((endTime - Date.now()) / (24 * 3600 * 1000));
  navigator.clipboard.writeText(`私の 人生 残り時間は あと ${days.toLocaleString('ja-JP')}日 でした。今日を 大事に 生きよう。`);
  alert('シェア テキスト コピー しました!');
});
""",
    "<dt>平均寿命の 根拠は？</dt><dd>厚労省 「簡易生命表 (2023)」 より 男性 81.05歳・女性 87.09歳。本ツールは 概算のため あなた個人の 健康状態を 反映していません。</dd><dt>SNSで シェアしたい</dt><dd>「シェア」 ボタンで テキスト コピー → X (Twitter) ・ Instagram の ストーリー に 貼り付け 可能。</dd>",
))


# ---------- 58. 同年代 年収 偏差値 ----------
TOOLS.append((
    "income-rank", "📊", "同年代 年収 偏差値・上位 何%",
    "年齢・年収を 入力するだけで 「あなたは 同年代の 上位 ◯%」 と 即時表示。賃金構造基本統計調査ベース。",
    """    <label>年齢:</label>
    <input id="age" class="in" type="number" value="35" />
    <label>性別 (賃金統計で 異なる):</label>
    <select id="sex" class="in">
      <option value="m" selected>男性</option>
      <option value="f">女性</option>
    </select>
    <label>年収 (額面・万円):</label>
    <input id="income" class="in" type="number" value="500" />
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result" style="display:none;">
      <div class="cards">
        <div class="cell" style="background:#fef3c7;"><div class="num" id="rank" style="color:#c00;font-size:36px;">上位 ?%</div><div class="cap">同年代 順位</div></div>
        <div class="cell"><div class="num" id="dev">0</div><div class="cap">年収 偏差値</div></div>
      </div>
      <div class="cards" style="margin-top:8px;">
        <div class="cell"><div class="num" id="median">¥0</div><div class="cap">同年代 中央値</div></div>
        <div class="cell"><div class="num" id="avg">¥0</div><div class="cap">同年代 平均</div></div>
        <div class="cell"><div class="num" id="diff" style="color:#16a34a;">¥0</div><div class="cap">差分</div></div>
      </div>
      <p id="msg" class="note" style="font-size:16px;font-weight:bold;"></p>
      <div class="bar"><button type="button" class="btn primary" id="share">📋 結果を シェア</button></div>
    </div>
""",
    """
// 男女・年齢別 中央値 (万円) - 賃金構造基本統計調査 (2023) を 概算
const MEDIAN_M = {20: 270, 25: 360, 30: 430, 35: 490, 40: 540, 45: 580, 50: 600, 55: 620, 60: 480};
const MEDIAN_F = {20: 250, 25: 320, 30: 360, 35: 380, 40: 390, 45: 400, 50: 410, 55: 400, 60: 320};
function lookup(table, age) {
  const keys = Object.keys(table).map(Number).sort((a,b)=>a-b);
  if (age <= keys[0]) return table[keys[0]];
  if (age >= keys[keys.length-1]) return table[keys[keys.length-1]];
  for (let i = 0; i < keys.length - 1; i++) {
    if (age >= keys[i] && age < keys[i+1]) {
      const r = (age - keys[i]) / (keys[i+1] - keys[i]);
      return table[keys[i]] + (table[keys[i+1]] - table[keys[i]]) * r;
    }
  }
  return 0;
}
function erf(x) { const a=0.3275911,p=[0.254829592,-0.284496736,1.421413741,-1.453152027,1.061405429]; const s=Math.sign(x); x=Math.abs(x); const t=1/(1+a*x); const y=1-(((((p[4]*t+p[3])*t)+p[2])*t+p[1])*t+p[0])*t*Math.exp(-x*x); return s*y; }
document.getElementById('calc').onclick = () => {
  const age = parseFloat(document.getElementById('age').value) || 0;
  const sex = document.getElementById('sex').value;
  const income = parseFloat(document.getElementById('income').value) || 0;
  const median = lookup(sex === 'm' ? MEDIAN_M : MEDIAN_F, age);
  const avg = median * 1.15; // 平均は 中央値より 高め (高所得者で 引っ張られる)
  const sd = median * 0.40; // 標準偏差 概算
  const z = (income - median) / sd;
  const dev = 50 + 10 * z;
  const rank = (1 - 0.5 * (1 + erf(z / Math.SQRT2))) * 100;
  const fmt = v => '¥' + (Math.round(v) * 10000).toLocaleString('ja-JP');
  document.getElementById('rank').textContent = `上位 ${rank.toFixed(1)}%`;
  document.getElementById('dev').textContent = dev.toFixed(1);
  document.getElementById('median').textContent = fmt(median);
  document.getElementById('avg').textContent = fmt(avg);
  const diff = income - median;
  document.getElementById('diff').textContent = (diff >= 0 ? '+' : '') + fmt(diff);
  const msg = document.getElementById('msg');
  if (rank < 1) msg.textContent = '🏆 同年代 トップ 1%。 圧倒的 ハイレイヤー。';
  else if (rank < 5) msg.textContent = '🌟 上位 5%。 業界の リーダー クラス。';
  else if (rank < 20) msg.textContent = '🚀 上位 20%。 高収入 ゾーン。';
  else if (rank < 40) msg.textContent = '✅ 上位 40%。 平均より 上、堅実。';
  else if (rank < 60) msg.textContent = '📊 標準帯。 ザ・日本人 サラリーマン。';
  else if (rank < 80) msg.textContent = '💪 中の下。 副業・転職で アップ 余地大。';
  else msg.textContent = '🌱 まだまだ これから。 スキル投資で 年100万円 アップ も。';
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`私の 年収は 同年代の 上位 ${rank.toFixed(1)}%、偏差値 ${dev.toFixed(1)} でした。中央値との 差 ${(diff > 0 ? '+' : '')}${diff}万円。`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "<dt>データ源は？</dt><dd>厚労省 「賃金構造基本統計調査 (令和5年)」 の 年齢階級別 年収を 概算化。実額は 業種・地域・企業規模で 大きく 変動します。</dd><dt>中央値 と 平均値 の 違い？</dt><dd>中央値: 並べた 真ん中の 値、平均: 全員の 平均。日本では 高所得者が 平均を 引き上げるため、平均より 中央値が 「実感に 近い」 数値。</dd>",
))


# ---------- 59. 同年代 貯金 偏差値 ----------
TOOLS.append((
    "savings-rank", "💰", "同年代 貯金額 偏差値・上位 何%",
    "年齢・貯金額から 同年代での 順位を 算出。金融庁 「家計の金融行動」 ベース。",
    """    <label>年齢:</label>
    <input id="age" class="in" type="number" value="35" />
    <label>世帯 区分:</label>
    <select id="house" class="in">
      <option value="single" selected>単身世帯</option>
      <option value="family">2人以上 世帯</option>
    </select>
    <label>貯金額 (預貯金 + 株式 + 投資信託 等の 金融資産 合計・万円):</label>
    <input id="savings" class="in" type="number" value="500" />
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result" style="display:none;">
      <div class="cards">
        <div class="cell" style="background:#dcfce7;"><div class="num" id="rank" style="color:#16a34a;font-size:36px;">上位 ?%</div><div class="cap">同年代 順位</div></div>
        <div class="cell"><div class="num" id="dev">0</div><div class="cap">偏差値</div></div>
      </div>
      <div class="cards" style="margin-top:8px;">
        <div class="cell"><div class="num" id="median">¥0</div><div class="cap">同年代 中央値</div></div>
        <div class="cell"><div class="num" id="avg">¥0</div><div class="cap">同年代 平均</div></div>
      </div>
      <p id="msg" class="note" style="font-size:16px;font-weight:bold;"></p>
      <p class="cap">※ 金融広報中央委員会 「家計の金融行動に関する世論調査 (2023)」 を 簡略化。</p>
      <div class="bar"><button type="button" class="btn primary" id="share">📋 結果を シェア</button></div>
    </div>
""",
    """
// 年齢別 金融資産 中央値・平均 (万円) - 金融広報中央委員会
const SINGLE_MED = {25: 50, 35: 150, 45: 250, 55: 400, 65: 600};
const SINGLE_AVG = {25: 250, 35: 600, 45: 1050, 55: 1450, 65: 1900};
const FAM_MED = {25: 80, 35: 250, 45: 400, 55: 650, 65: 1000};
const FAM_AVG = {25: 350, 35: 750, 45: 1200, 55: 1700, 65: 2200};
function lookup(table, age) {
  const keys = Object.keys(table).map(Number).sort((a,b)=>a-b);
  if (age <= keys[0]) return table[keys[0]];
  if (age >= keys[keys.length-1]) return table[keys[keys.length-1]];
  for (let i = 0; i < keys.length - 1; i++) {
    if (age >= keys[i] && age < keys[i+1]) {
      const r = (age - keys[i]) / (keys[i+1] - keys[i]);
      return table[keys[i]] + (table[keys[i+1]] - table[keys[i]]) * r;
    }
  }
  return 0;
}
function erf(x) { const a=0.3275911,p=[0.254829592,-0.284496736,1.421413741,-1.453152027,1.061405429]; const s=Math.sign(x); x=Math.abs(x); const t=1/(1+a*x); const y=1-(((((p[4]*t+p[3])*t)+p[2])*t+p[1])*t+p[0])*t*Math.exp(-x*x); return s*y; }
document.getElementById('calc').onclick = () => {
  const age = parseFloat(document.getElementById('age').value) || 0;
  const isFamily = document.getElementById('house').value === 'family';
  const savings = parseFloat(document.getElementById('savings').value) || 0;
  const med = lookup(isFamily ? FAM_MED : SINGLE_MED, age);
  const avg = lookup(isFamily ? FAM_AVG : SINGLE_AVG, age);
  // 対数正規分布で 近似 (貯金は 対数で 正規に近い)
  const lnSavings = Math.log(Math.max(1, savings));
  const lnMed = Math.log(Math.max(1, med));
  const lnSd = Math.log(avg / med) * 1.5; // 経験的に
  const z = (lnSavings - lnMed) / lnSd;
  const dev = 50 + 10 * z;
  const rank = (1 - 0.5 * (1 + erf(z / Math.SQRT2))) * 100;
  const fmt = v => '¥' + (Math.round(v) * 10000).toLocaleString('ja-JP');
  document.getElementById('rank').textContent = `上位 ${rank.toFixed(1)}%`;
  document.getElementById('dev').textContent = dev.toFixed(1);
  document.getElementById('median').textContent = fmt(med);
  document.getElementById('avg').textContent = fmt(avg);
  const msg = document.getElementById('msg');
  if (rank < 5) msg.textContent = '🏆 同年代 トップ 5%。 早期FIRE 視野 圏内。';
  else if (rank < 20) msg.textContent = '🚀 上位 20%。 堅実な 蓄財ぶり。';
  else if (rank < 40) msg.textContent = '✅ 上位 40%。 平均より 上。';
  else if (rank < 70) msg.textContent = '📊 標準帯。 NISA・iDeCo 活用で 順位アップ可能。';
  else msg.textContent = '🌱 まだ 少ない。 月3万円 つみたて で 10年で 中央値 突破できます。';
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`私の 貯金額は 同年代の 上位 ${rank.toFixed(1)}%、偏差値 ${dev.toFixed(1)} でした!`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "<dt>「貯金ゼロ」 でも 多い？</dt><dd>金融庁 調査では 「金融資産 ゼロ」 が 単身 30代で 約34%、40代で 約27%。日本は 二極化 が 進んでいます。少額でも 始めるのが 重要。</dd><dt>不動産・年金は？</dt><dd>本ツールは 「金融資産」 (預貯金・株・投資信託・保険) のみ。持ち家・年金は 含めません (流動性 が 違うため)。</dd>",
))


# ---------- 60. 生まれてから 何日 ----------
TOOLS.append((
    "days-alive", "🎂", "生まれてから 何日? 次の キリ番 まで",
    "あなたは これまで 何日 生きてきた？10000日・15000日 など キリ番 まで 何日？シェア用 ツール。",
    """    <label>生年月日:</label>
    <input id="birth" class="in" type="date" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div id="result" style="display:none;">
      <div style="text-align:center;margin:20px 0;">
        <div style="color:#475569;">あなたは これまで</div>
        <div id="bigDays" style="font-size:64px;font-weight:bold;color:#16a34a;">0</div>
        <div style="color:#475569;">日 生きてきました</div>
      </div>
      <div class="cards">
        <div class="cell"><div class="num" id="hours">0</div><div class="cap">時間</div></div>
        <div class="cell"><div class="num" id="mins">0</div><div class="cap">分</div></div>
        <div class="cell"><div class="num" id="weeks">0</div><div class="cap">週</div></div>
      </div>
      <h2>次の キリ番 記念日</h2>
      <div id="milestones" class="cap" style="font-size:14px;line-height:2;"></div>
      <div class="bar"><button type="button" class="btn primary" id="share">📋 シェア</button></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const b = document.getElementById('birth').value;
  if (!b) return;
  const birth = new Date(b);
  const now = new Date();
  const days = Math.floor((now - birth) / (1000 * 60 * 60 * 24));
  const hours = Math.floor((now - birth) / (1000 * 60 * 60));
  const mins = Math.floor((now - birth) / (1000 * 60));
  const weeks = Math.floor(days / 7);
  document.getElementById('bigDays').textContent = days.toLocaleString('ja-JP');
  document.getElementById('hours').textContent = hours.toLocaleString('ja-JP');
  document.getElementById('mins').textContent = mins.toLocaleString('ja-JP');
  document.getElementById('weeks').textContent = weeks.toLocaleString('ja-JP');
  // 次の キリ番
  const milestones = [];
  for (const m of [1000, 5000, 10000, 15000, 20000, 25000, 30000, 36500]) {
    if (days < m) {
      const target = new Date(birth.getTime() + m * 24 * 60 * 60 * 1000);
      const remaining = m - days;
      milestones.push(`<strong>${m.toLocaleString('ja-JP')}日 目 (${m === 36500 ? '100歳' : ''})</strong>: あと ${remaining.toLocaleString('ja-JP')}日 (${target.getFullYear()}/${target.getMonth()+1}/${target.getDate()})`);
      if (milestones.length >= 4) break;
    }
  }
  document.getElementById('milestones').innerHTML = milestones.join('<br>');
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`私は 今日で 生まれてから ${days.toLocaleString('ja-JP')}日目! 時間にして ${hours.toLocaleString('ja-JP')}時間 ${mins.toLocaleString('ja-JP')}分 生きてきました。`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "<dt>キリ番 記念日って？</dt><dd>10000日 = 約27.4歳、15000日 = 約41歳、20000日 = 約54.8歳、25000日 = 約68.5歳。年単位 とは 違う 「日」 で 区切る 記念日が SNSで 流行中。</dd>",
))


# ---------- 61. 生涯年収 ----------
TOOLS.append((
    "lifetime-income", "💵", "生涯年収 シミュレータ",
    "現在の 年齢・年収・想定 昇給率から 退職までの 生涯年収を 計算。「人生で あといくら 稼ぐ？」",
    """    <label>現在の 年齢:</label>
    <input id="age" class="in" type="number" value="30" />
    <label>現在の 年収 (額面・万円):</label>
    <input id="income" class="in" type="number" value="500" />
    <label>想定 年間 昇給率 (%):</label>
    <input id="raise" class="in" type="number" step="0.1" value="2" />
    <label>退職 予定 年齢:</label>
    <input id="retire" class="in" type="number" value="65" />
    <div class="bar"><button type="button" class="btn primary" id="calc">計算</button></div>
    <div id="result" style="display:none;">
      <div style="text-align:center;margin:20px 0;">
        <div style="color:#475569;">残り キャリアで 稼ぐ 額</div>
        <div id="big" style="font-size:48px;font-weight:bold;color:#16a34a;">¥0</div>
      </div>
      <div class="cards">
        <div class="cell"><div class="num" id="ended">¥0</div><div class="cap">退職時 年収</div></div>
        <div class="cell"><div class="num" id="netLife">¥0</div><div class="cap">手取り 累計 (約77%)</div></div>
        <div class="cell"><div class="num" id="years">0</div><div class="cap">残り キャリア</div></div>
      </div>
      <p id="msg" class="note" style="font-size:15px;"></p>
      <div class="bar"><button type="button" class="btn primary" id="share">📋 シェア</button></div>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const age = parseFloat(document.getElementById('age').value) || 0;
  const income = parseFloat(document.getElementById('income').value) || 0;
  const raise = (parseFloat(document.getElementById('raise').value) || 0) / 100;
  const retire = parseFloat(document.getElementById('retire').value) || 0;
  const years = Math.max(0, retire - age);
  let total = 0, cur = income;
  for (let i = 0; i < years; i++) {
    total += cur;
    cur *= (1 + raise);
  }
  const fmt = v => '¥' + Math.round(v * 10000).toLocaleString('ja-JP');
  document.getElementById('big').textContent = fmt(total);
  document.getElementById('ended').textContent = fmt(cur / (1 + raise));
  document.getElementById('netLife').textContent = fmt(total * 0.77);
  document.getElementById('years').textContent = years + '年';
  const msg = document.getElementById('msg');
  if (total > 30000) msg.textContent = '🏆 生涯 3億円超! トップ層。';
  else if (total > 20000) msg.textContent = '🌟 2億円超。 一般的に 「高所得」 と 言われる ライン。';
  else if (total > 10000) msg.textContent = '✅ 1億円超。 日本人 サラリーマン 平均 〜 やや 上。';
  else msg.textContent = '💡 副業・スキルアップで 大幅 増加 余地あり。';
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`私の 生涯年収 (残り キャリア) は ${Math.round(total)}万円 でした!`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "<dt>「生涯年収 3億円」 って 本当？</dt><dd>男性 大学卒・大企業の 平均が 約2.6-3億円 と 言われます (退職金 込み)。中小・女性・高卒は ここから 0.5-1.5億円 減。本ツールで 自分の 数字で 算出してみてください。</dd>",
))


# ---------- 62. 動物占い ----------
TOOLS.append((
    "animal-uranai", "🐾", "動物占い (生年月日 12タイプ)",
    "生年月日から 12種類の 動物に 分類。人気の 動物占いで あなたの 性格と 相性が 一目瞭然。",
    """    <label>生年月日:</label>
    <input id="birth" class="in" type="date" />
    <div class="bar"><button type="button" class="btn primary" id="calc">占う</button></div>
    <div id="result" style="display:none;"></div>
""",
    """
const ANIMALS = [
  {name: 'チータ', icon: '🐆', desc: '時代を 先取りする 早熟タイプ。スピード感 と 直感力 が 武器。', good: 'たぬき, ゾウ'},
  {name: 'たぬき', icon: '🦝', desc: '愛され キャラ。協調性が 高く、人間関係の 達人。', good: 'チータ, 黒ひょう'},
  {name: '猿', icon: '🐵', desc: '頭の 回転が 速く、要領が 良い 賢者。盛り上げ役 にも 最適。', good: 'コアラ, 子守熊'},
  {name: 'コアラ', icon: '🐨', desc: 'マイペースで 独自の 美意識。芸術 センスが 光る。', good: '猿, トラ'},
  {name: '黒ひょう', icon: '🐆', desc: 'スタイリッシュで 流行に 敏感。社交家で 表現力 抜群。', good: 'たぬき, ライオン'},
  {name: 'ライオン', icon: '🦁', desc: '王者の 風格。プライド 高く、人を 引っ張る 自然な リーダー。', good: '黒ひょう, ペガサス'},
  {name: '虎', icon: '🐯', desc: 'バランス感覚に 優れ、何事にも 真面目に 取り組む 堅実派。', good: 'コアラ, ひつじ'},
  {name: 'たぬきB', icon: '🦝', desc: '計画的で 着実。目標達成への 努力を 惜しまない。', good: 'チータ, ゾウ'},
  {name: 'こじか', icon: '🦌', desc: '純粋で 警戒心が 強め。信頼すると 一途に 尽くす。', good: 'ペガサス, ライオン'},
  {name: 'ゾウ', icon: '🐘', desc: '努力家で 持続力 ある 大器晩成型。一度 決めたら 最後まで。', good: 'チータ, たぬきB'},
  {name: 'ひつじ', icon: '🐑', desc: '優しく 平和主義。みんなと 仲良くするのが 何より 大事。', good: '虎, 狼'},
  {name: 'ペガサス', icon: '🦄', desc: '自由 奔放な 天才肌。独創性と インスピレーションの 持ち主。', good: 'ライオン, こじか'},
];
document.getElementById('calc').onclick = () => {
  const b = document.getElementById('birth').value;
  if (!b) { alert('生年月日を 入力してください'); return; }
  const d = new Date(b);
  // 簡易: 月+日から 12種類に 分類
  const idx = (d.getMonth() + d.getDate() + d.getFullYear()) % 12;
  const a = ANIMALS[idx];
  document.getElementById('result').innerHTML = `
    <div class="cell" style="background:#fef3c7;text-align:center;padding:24px;">
      <div style="font-size:80px;">${a.icon}</div>
      <div style="font-size:32px;font-weight:bold;color:#c00;">${a.name}</div>
      <div class="cap" style="font-size:16px;margin-top:12px;line-height:1.7;">${a.desc}</div>
      <div class="cap" style="margin-top:16px;">💕 相性が 良い 動物: ${a.good}</div>
    </div>
    <div class="bar"><button type="button" class="btn primary" id="share">📋 結果を シェア</button></div>`;
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`私の 動物占いは 「${a.name}」 ${a.icon} でした! ${a.desc}`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "<dt>本物の 動物占いと 違う？</dt><dd>本ツールは 12種類の 簡易版。公式の 動物占い (個性學) は 60種類で 生年月日 から 詳細に 判定。本格的 診断は 公式書籍 を どうぞ。</dd>",
))


# ---------- 63. 名前 相性診断 ----------
TOOLS.append((
    "name-match", "💕", "名前 相性 診断 (2人の 名前を 入力)",
    "2人の 名前から 相性%を 即時表示。古典的 ながら 永遠の 人気テーマ。",
    """    <label>あなたの 名前:</label>
    <input id="name1" class="in" type="text" placeholder="例: 太郎" />
    <label>相手の 名前:</label>
    <input id="name2" class="in" type="text" placeholder="例: 花子" />
    <div class="bar"><button type="button" class="btn primary" id="calc">相性 診断</button></div>
    <div id="result" style="display:none;text-align:center;margin-top:20px;"></div>
""",
    """
document.getElementById('calc').onclick = () => {
  const n1 = document.getElementById('name1').value.trim();
  const n2 = document.getElementById('name2').value.trim();
  if (!n1 || !n2) { alert('両方 入力してください'); return; }
  // 文字コード合計から 相性% を 計算 (両方の 名前で 安定した 結果)
  let sum = 0;
  for (const c of n1 + n2) sum += c.charCodeAt(0);
  // 名前順を 入れ替えても 同じ結果に
  let sum2 = 0;
  for (const c of n2 + n1) sum2 += c.charCodeAt(0);
  const seed = (sum + sum2) % 100;
  const pct = 40 + (seed % 61); // 40-100%
  let comment, emoji;
  if (pct >= 90) { comment = '運命の 相手! 結婚 視野に。'; emoji = '💍'; }
  else if (pct >= 75) { comment = 'とても 相性 抜群! 長く 続く カップル。'; emoji = '💕'; }
  else if (pct >= 60) { comment = '良い 関係。 お互い 尊重 すれば◎'; emoji = '😊'; }
  else if (pct >= 50) { comment = '普通の 相性。 努力次第で 良くなる。'; emoji = '🌱'; }
  else { comment = '相性は あまり 良くないかも。 でも 気持ちが あれば 関係ない!'; emoji = '🤔'; }
  document.getElementById('result').innerHTML = `
    <div class="cell" style="background:#fce7f3;padding:24px;">
      <div style="font-size:18px;margin-bottom:8px;">${n1} さん & ${n2} さん</div>
      <div style="font-size:60px;">${emoji}</div>
      <div style="font-size:72px;font-weight:bold;color:#c00;">${pct}%</div>
      <div class="cap" style="font-size:16px;margin-top:12px;">${comment}</div>
    </div>
    <div class="bar" style="margin-top:16px;"><button type="button" class="btn primary" id="share">📋 結果を シェア</button></div>`;
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`${n1} さんと ${n2} さんの 相性は ${pct}%! ${comment}`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "",
))


# ---------- 64. 画像 圧縮 ----------
TOOLS.append((
    "image-compress", "🖼", "画像 圧縮 (ブラウザ内・送信なし)",
    "JPEG・PNG 画像を 品質指定で 圧縮。メール添付・SNS投稿 用に サイズダウン。",
    """    <label>画像を 選択 (複数 可):</label>
    <input type="file" id="files" accept="image/*" multiple class="in" />
    <label>品質 (低いほど 軽量・100%が 最高画質):</label>
    <input type="range" id="quality" min="10" max="100" value="70" class="in" oninput="document.getElementById('qval').textContent = this.value + '%'" />
    <div id="qval" class="num">70%</div>
    <label>最大 サイズ (px・長辺・元のままなら 0):</label>
    <input id="maxSize" class="in" type="number" value="1920" />
    <div class="bar"><button type="button" class="btn primary" id="compress">圧縮</button></div>
    <div id="results"></div>
""",
    """
document.getElementById('compress').onclick = async () => {
  const files = document.getElementById('files').files;
  if (!files || files.length === 0) { alert('画像を 選択してください'); return; }
  const q = parseInt(document.getElementById('quality').value, 10) / 100;
  const maxSize = parseInt(document.getElementById('maxSize').value, 10);
  const $r = document.getElementById('results');
  $r.innerHTML = '';
  for (const f of files) {
    const img = new Image();
    img.src = URL.createObjectURL(f);
    await new Promise(r => img.onload = r);
    let w = img.width, h = img.height;
    if (maxSize > 0 && Math.max(w, h) > maxSize) {
      const ratio = maxSize / Math.max(w, h);
      w = Math.round(w * ratio);
      h = Math.round(h * ratio);
    }
    const canvas = document.createElement('canvas');
    canvas.width = w; canvas.height = h;
    canvas.getContext('2d').drawImage(img, 0, 0, w, h);
    const blob = await new Promise(r => canvas.toBlob(r, 'image/jpeg', q));
    const url = URL.createObjectURL(blob);
    const reduce = (1 - blob.size / f.size) * 100;
    const div = document.createElement('div');
    div.className = 'cell';
    div.style.textAlign = 'left';
    div.style.margin = '8px 0';
    div.innerHTML = `
      <div style="font-weight:bold;">${f.name}</div>
      <div class="cap">元: ${(f.size/1024).toFixed(1)} KB → 圧縮後: ${(blob.size/1024).toFixed(1)} KB (${reduce.toFixed(1)}% 削減)</div>
      <div class="cap">${w} × ${h} px</div>
      <a href="${url}" download="${f.name.replace(/\\.[^.]+$/, '')}_compressed.jpg" class="btn primary" style="display:inline-block;margin-top:8px;">ダウンロード</a>
    `;
    $r.appendChild(div);
  }
};
""",
    "<dt>本当に サーバーに 送信されない？</dt><dd>はい。Canvas API + Blob で ブラウザ 内 だけで 処理しています。ネット切断 状態でも 動作します。</dd><dt>PNG だと 圧縮 効かない？</dt><dd>本ツールは PNG → JPEG 変換 で 圧縮します (写真は JPEG が 効率的)。透過 (alpha) が ある PNG は 透過部分が 黒に なります。</dd>",
))


# ---------- 65. 画像 リサイズ ----------
TOOLS.append((
    "image-resize", "📐", "画像 リサイズ (px / % 指定)",
    "画像を 指定 サイズ や 割合に 一括 リサイズ。SNS用・ブログ用に 整える。",
    """    <label>画像を 選択 (複数 可):</label>
    <input type="file" id="files" accept="image/*" multiple class="in" />
    <label>リサイズ 方法:</label>
    <select id="mode" class="in">
      <option value="long" selected>長辺 指定 (px)</option>
      <option value="width">幅 指定 (px)</option>
      <option value="height">高さ 指定 (px)</option>
      <option value="percent">割合 (%)</option>
    </select>
    <label>値:</label>
    <input id="val" class="in" type="number" value="800" />
    <h2>SNS用 プリセット</h2>
    <div class="bar">
      <button type="button" class="btn ghost" onclick="document.getElementById('mode').value='long';document.getElementById('val').value=1080;">📷 Instagram (1080)</button>
      <button type="button" class="btn ghost" onclick="document.getElementById('mode').value='long';document.getElementById('val').value=1200;">🐦 X / Twitter (1200)</button>
      <button type="button" class="btn ghost" onclick="document.getElementById('mode').value='long';document.getElementById('val').value=1280;">▶️ YouTube サムネ (1280)</button>
    </div>
    <div class="bar"><button type="button" class="btn primary" id="resize">リサイズ</button></div>
    <div id="results"></div>
""",
    """
document.getElementById('resize').onclick = async () => {
  const files = document.getElementById('files').files;
  if (!files || files.length === 0) { alert('画像を 選択してください'); return; }
  const mode = document.getElementById('mode').value;
  const val = parseFloat(document.getElementById('val').value);
  const $r = document.getElementById('results');
  $r.innerHTML = '';
  for (const f of files) {
    const img = new Image();
    img.src = URL.createObjectURL(f);
    await new Promise(r => img.onload = r);
    let w, h;
    if (mode === 'percent') {
      w = Math.round(img.width * val / 100);
      h = Math.round(img.height * val / 100);
    } else if (mode === 'width') {
      w = val; h = Math.round(img.height * val / img.width);
    } else if (mode === 'height') {
      h = val; w = Math.round(img.width * val / img.height);
    } else { // long
      if (img.width > img.height) { w = val; h = Math.round(img.height * val / img.width); }
      else { h = val; w = Math.round(img.width * val / img.height); }
    }
    const canvas = document.createElement('canvas');
    canvas.width = w; canvas.height = h;
    canvas.getContext('2d').drawImage(img, 0, 0, w, h);
    const blob = await new Promise(r => canvas.toBlob(r, f.type, 0.92));
    const url = URL.createObjectURL(blob);
    const div = document.createElement('div');
    div.className = 'cell';
    div.style.textAlign = 'left';
    div.style.margin = '8px 0';
    div.innerHTML = `
      <div style="font-weight:bold;">${f.name}</div>
      <div class="cap">${img.width}×${img.height} → ${w}×${h} px (${(blob.size/1024).toFixed(1)} KB)</div>
      <a href="${url}" download="${f.name.replace(/\\.[^.]+$/, '')}_resized.${f.type === 'image/png' ? 'png' : 'jpg'}" class="btn primary" style="display:inline-block;margin-top:8px;">ダウンロード</a>
    `;
    $r.appendChild(div);
  }
};
""",
    "",
))


# ---------- 66. キラキラネーム判定 ----------
TOOLS.append((
    "kirakira-name", "✨", "キラキラネーム 度 判定",
    "お子さん (or 自分) の 名前を 入れると 「キラキラネーム 度」 を 判定。読みやすさ・当て字度 など。",
    """    <label>判定する 名前 (漢字):</label>
    <input id="kanji" class="in" type="text" placeholder="例: 心愛" />
    <label>その 読み方:</label>
    <input id="yomi" class="in" type="text" placeholder="例: ここあ" />
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result" style="display:none;"></div>
""",
    """
const COMMON_KANJI = '太郎次郎花子美咲健太翔太大輝陽菜結愛大和優子直美和子真理子明美隆夫義雄正一一郎勝美愛子';
const KIRAKIRA_HINTS = ['愛', '夢', '羅', '苺', '姫', '皇', '王', '光', '輝', '煌', '麗'];
const KIRAKIRA_YOMI = ['らぶ', 'らぶり', 'てぃあら', 'きてぃ', 'りずむ', 'ぴあの', 'ぴゅあ', 'らいき', 'まよ', 'るりこ', 'ぷりん', 'りこ', 'てぃあ', 'はーと', 'ぱーる', 'ぱりす', 'ぽっぷ', 'ぱふぇ'];
document.getElementById('calc').onclick = () => {
  const kanji = document.getElementById('kanji').value.trim();
  const yomi = document.getElementById('yomi').value.trim().toLowerCase();
  if (!kanji || !yomi) { alert('両方 入力してください'); return; }
  let score = 0;
  let reasons = [];
  // 当て字・難読 判定: 文字数の 不一致 (漢字 1文字 = ひらがな 2-3 が 標準)
  const expectedYomi = kanji.length * 2;
  if (yomi.length > kanji.length * 4) { score += 30; reasons.push('読みが 漢字に 対して 長すぎる (当て字 疑い)'); }
  if (yomi.length < kanji.length) { score += 20; reasons.push('読みが 漢字に 対して 短すぎる (省略 ・ 強引)'); }
  // キラキラ ヒント漢字
  for (const k of KIRAKIRA_HINTS) {
    if (kanji.includes(k)) { score += 10; reasons.push(`「${k}」 は 派手な 印象の 漢字`); }
  }
  // カタカナ・外来語 系 ヨミ
  for (const y of KIRAKIRA_YOMI) {
    if (yomi.includes(y)) { score += 25; reasons.push(`「${y}」 は 外来語 系の 読み`); }
  }
  // 「と」「な」 など よくある 男女兼用 漢字 (キラキラ性 低)
  if (COMMON_KANJI.includes(kanji)) score -= 20;
  // 結果
  score = Math.max(0, Math.min(100, score));
  let level, emoji, color;
  if (score < 20) { level = '正統派'; emoji = '🎌'; color = '#16a34a'; }
  else if (score < 40) { level = '個性派'; emoji = '🌸'; color = '#1d9bf0'; }
  else if (score < 60) { level = '読みにくい かも'; emoji = '🤔'; color = '#e67e22'; }
  else if (score < 80) { level = 'キラキラ ネーム'; emoji = '✨'; color = '#c00'; }
  else { level = '超 キラキラ ネーム'; emoji = '🌟'; color = '#c00'; }
  document.getElementById('result').innerHTML = `
    <div class="cell" style="background:#fef3c7;text-align:center;padding:24px;">
      <div style="font-size:28px;">${kanji} (${yomi})</div>
      <div style="font-size:72px;">${emoji}</div>
      <div style="font-size:36px;font-weight:bold;color:${color};">${level}</div>
      <div class="num" style="margin-top:8px;">スコア: ${score}/100</div>
      <div class="cap" style="margin-top:16px;text-align:left;">${reasons.length ? '判定 理由:<br>' + reasons.map(r => '• ' + r).join('<br>') : '一般的な 範囲内です'}</div>
    </div>`;
  document.getElementById('result').style.display = 'block';
};
""",
    "<dt>キラキラネームの 定義は？</dt><dd>明確な 定義は ありません。本ツールは ① 当て字度 ② 派手な 漢字 ③ 外来語的 読み の 3軸で 判定。世代差も 大きい (祖父母 世代から 見ると 「心」「愛」 入りの 名前は キラキラ)。</dd><dt>キラキラネーム は ダメ？</dt><dd>個性的で 良い 面も。一方で 「読みにくい」 「就活で 不利」 等の 報告も。バランスが 大事。</dd>",
))


# ---------- 67. 適職診断 (10問) ----------
TOOLS.append((
    "career-test", "🧭", "適職診断 (10問・5カテゴリ)",
    "10問の 質問で あなたに 向いている 職業 カテゴリを 判定。",
    """    <div id="quiz">
      <div id="qs"></div>
      <div class="bar"><button type="button" class="btn primary" id="judge">診断 結果</button></div>
    </div>
    <div id="result" style="display:none;"></div>
""",
    """
const Q = [
  {q: '人と話すのが 好き?', cat: 'sales'},
  {q: '数字や データを 扱うのが 得意?', cat: 'analysis'},
  {q: '新しいものを 作る のが 楽しい?', cat: 'creative'},
  {q: '誰かを 助ける ことに 喜びを 感じる?', cat: 'care'},
  {q: '計画的に 物事を 進めたい?', cat: 'admin'},
  {q: '初対面の 人と すぐ 仲良くなれる?', cat: 'sales'},
  {q: 'パズル・ロジック ゲームが 好き?', cat: 'analysis'},
  {q: '絵や 音楽・文章で 表現するのが 好き?', cat: 'creative'},
  {q: '困っている 人を 見ると 放っておけない?', cat: 'care'},
  {q: '締め切りを 守る 自信が ある?', cat: 'admin'},
];
const CATS = {
  sales: {name: '営業・接客 タイプ', icon: '🤝', jobs: '営業, 接客, 広報, コンサル, カスタマーサクセス'},
  analysis: {name: '分析・技術 タイプ', icon: '🔬', jobs: 'エンジニア, データサイエンティスト, 研究員, 会計士, アナリスト'},
  creative: {name: 'クリエイティブ タイプ', icon: '🎨', jobs: 'デザイナー, ライター, 動画クリエイター, 企画, アーティスト'},
  care: {name: 'サポート・対人援助 タイプ', icon: '🌷', jobs: '看護師, 介護士, 教師, カウンセラー, 保育士'},
  admin: {name: '管理・運営 タイプ', icon: '📋', jobs: '事務, 経理, 総務, プロジェクトマネージャー, 公務員'},
};
const $qs = document.getElementById('qs');
Q.forEach((q, i) => {
  const div = document.createElement('div');
  div.style.margin = '15px 0';
  div.innerHTML = `<p style="font-weight:bold;">${i+1}. ${q.q}</p>` +
    [['とても 思う', 2], ['まあ 思う', 1], ['どちらでも', 0], ['あまり', -1], ['思わない', -2]].map(([l, v]) =>
      `<label style="margin-right:12px;"><input type="radio" name="q${i}" value="${v}" ${v===0?'checked':''}> ${l}</label>`
    ).join('');
  $qs.appendChild(div);
});
document.getElementById('judge').onclick = () => {
  const scores = {sales:0, analysis:0, creative:0, care:0, admin:0};
  for (let i = 0; i < Q.length; i++) {
    const v = parseInt(document.querySelector(`input[name="q${i}"]:checked`).value, 10);
    scores[Q[i].cat] += v;
  }
  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const top = sorted[0][0];
  const second = sorted[1][0];
  const t = CATS[top], s = CATS[second];
  document.getElementById('quiz').style.display = 'none';
  document.getElementById('result').innerHTML = `
    <div class="cell" style="background:#dcfce7;text-align:center;padding:24px;">
      <div style="font-size:64px;">${t.icon}</div>
      <div style="font-size:24px;font-weight:bold;color:#16a34a;">${t.name}</div>
      <div class="cap" style="margin-top:12px;">向いている 職業: ${t.jobs}</div>
    </div>
    <div class="cell" style="text-align:center;padding:16px;margin-top:8px;">
      <div style="font-size:14px;">第2 候補: ${s.icon} ${s.name}</div>
      <div class="cap">${s.jobs}</div>
    </div>
    <div class="bar"><button type="button" class="btn primary" id="share">📋 結果 シェア</button></div>`;
  document.getElementById('result').style.display = 'block';
  document.getElementById('share').onclick = () => {
    navigator.clipboard.writeText(`私の 適職診断は 「${t.name}」 ${t.icon}! 向いている 職業: ${t.jobs}`);
    alert('シェア テキスト コピー しました!');
  };
};
""",
    "",
))


# ---------- 68. ブラック企業度 ----------
TOOLS.append((
    "black-company", "🏴", "ブラック企業度 チェック (10項目)",
    "勤務先の 状況を 10項目 チェックすると 「ブラック企業度」 を 100点 満点で 判定。",
    """    <p class="lead">該当する 項目に チェック。匿名・送信なし。</p>
    <div id="items">
      <label class="ch"><input type="checkbox" value="15"> 月の 残業 60時間 超</label>
      <label class="ch"><input type="checkbox" value="20"> サービス残業 が 当たり前</label>
      <label class="ch"><input type="checkbox" value="15"> 有給休暇を 取らせて くれない / 取りにくい 雰囲気</label>
      <label class="ch"><input type="checkbox" value="10"> 給料が 業界 平均より 明らかに 低い</label>
      <label class="ch"><input type="checkbox" value="10"> 退職者が 多い (3年で 半数以上 辞めている)</label>
      <label class="ch"><input type="checkbox" value="10"> パワハラ・暴言が 日常的</label>
      <label class="ch"><input type="checkbox" value="10"> 残業代が 全部 出ない (固定残業含む) / 一部 カット</label>
      <label class="ch"><input type="checkbox" value="5"> 休日 出勤が 月に 2回以上 ある (代休なし)</label>
      <label class="ch"><input type="checkbox" value="5"> 体調 不良でも 休めない</label>
      <label class="ch"><input type="checkbox" value="10"> 「家族」 「絆」 を 強調する 経営者・社訓</label>
    </div>
    <div class="bar"><button type="button" class="btn primary" id="calc">判定</button></div>
    <div id="result" style="display:none;text-align:center;margin-top:20px;"></div>
""",
    """
document.querySelectorAll('.ch').forEach(l => l.style.display = 'block');
document.getElementById('calc').onclick = () => {
  let score = 0;
  document.querySelectorAll('#items input:checked').forEach(c => score += parseInt(c.value, 10));
  let level, emoji, color, advice;
  if (score === 0) { level = 'ホワイト 企業'; emoji = '🤍'; color = '#16a34a'; advice = '大切に しましょう!'; }
  else if (score < 20) { level = '健全'; emoji = '✅'; color = '#16a34a'; advice = '一般的な 範囲内。'; }
  else if (score < 40) { level = 'グレー'; emoji = '⚠️'; color = '#e67e22'; advice = '改善 余地あり。労組や 人事に 相談を。'; }
  else if (score < 70) { level = 'ブラック'; emoji = '🏴'; color = '#c00'; advice = '転職 活動を 視野に。労基署 相談も。'; }
  else { level = '超 ブラック'; emoji = '💀'; color = '#c00'; advice = '危険レベル。 健康を 守る 行動を 早めに。労基署 / 弁護士 相談を 強く 推奨。'; }
  document.getElementById('result').innerHTML = `
    <div class="cell" style="background:#fee2e2;padding:24px;">
      <div style="font-size:80px;">${emoji}</div>
      <div style="font-size:36px;font-weight:bold;color:${color};">${level}</div>
      <div style="font-size:24px;margin:12px 0;">スコア: ${score} / 110</div>
      <div class="cap" style="font-size:16px;">${advice}</div>
    </div>
    <h2>相談 窓口</h2>
    <p class="cap" style="font-size:14px;text-align:left;">
      🆘 労働基準監督署: 0120-XXX-XXX (地域別)<br>
      🆘 総合労働相談コーナー: 無料・匿名 相談 可<br>
      🆘 厚労省 「労働条件 相談ほっとライン」: 0120-811-610 (平日 17-22時・土日祝 9-21時)<br>
      🆘 法テラス: 0570-078374 (無料 法律相談)
    </p>`;
  document.getElementById('result').style.display = 'block';
};
""",
    "",
))


# ---------- 69. FIRE 達成 年数 ----------
TOOLS.append((
    "fire-years", "🔥", "FIRE 達成 年数 (経済的自立 シミュ)",
    "年収・支出・投資利回りから 「働かなくても 生きていける」 状態 (FIRE) までの 年数を 算出。",
    """    <label>現在の 年収 手取り (万円):</label>
    <input id="income" class="in" type="number" value="400" />
    <label>年間 支出 (生活費 合計・万円):</label>
    <input id="expense" class="in" type="number" value="240" />
    <label>現在の 資産 (万円):</label>
    <input id="assets" class="in" type="number" value="200" />
    <label>運用 利回り (年率 %):</label>
    <input id="rate" class="in" type="number" step="0.5" value="5" />
    <div class="bar"><button type="button" class="btn primary" id="calc">FIRE 計算</button></div>
    <div id="result" style="display:none;">
      <div class="cards">
        <div class="cell"><div class="num" id="goal">¥0</div><div class="cap">FIRE 必要 資産</div></div>
        <div class="cell" style="background:#dcfce7;"><div class="num" id="years" style="color:#c00;font-size:48px;">?</div><div class="cap">達成までの 年数</div></div>
      </div>
      <p id="msg" class="note" style="font-size:15px;"></p>
      <h2>4% ルール とは</h2>
      <p class="cap" style="font-size:14px;">米国 トリニティ 大学の 研究より、年4% 取り崩しても 30年以上 資産が 維持できる ことが 統計的に 示されました。FIRE は 「年間 生活費 × 25倍」 の 資産 ・ それを 年4% で 取り崩す のが 基本式。</p>
    </div>
""",
    """
document.getElementById('calc').onclick = () => {
  const income = parseFloat(document.getElementById('income').value) || 0;
  const expense = parseFloat(document.getElementById('expense').value) || 0;
  const assets = parseFloat(document.getElementById('assets').value) || 0;
  const rate = (parseFloat(document.getElementById('rate').value) || 0) / 100;
  // FIRE 目標: 年間 支出 × 25倍 (4%ルール)
  const goal = expense * 25;
  const annualSave = income - expense;
  if (annualSave <= 0) {
    document.getElementById('years').textContent = '∞';
    document.getElementById('goal').textContent = '¥' + (goal * 10000).toLocaleString('ja-JP');
    document.getElementById('msg').textContent = '⚠️ 年間 貯蓄が ゼロ または マイナス。 支出 削減 か 収入アップが 必要。';
    document.getElementById('result').style.display = 'block';
    return;
  }
  // 複利 計算: 何年で 目標達成 か
  let years = 0;
  let cur = assets;
  while (cur < goal && years < 80) {
    cur = cur * (1 + rate) + annualSave;
    years++;
  }
  const fmt = v => '¥' + Math.round(v * 10000).toLocaleString('ja-JP');
  document.getElementById('goal').textContent = fmt(goal);
  document.getElementById('years').textContent = years < 80 ? years + '年' : '困難';
  const msg = document.getElementById('msg');
  if (years <= 15) msg.textContent = '🔥 ハイペース! 早期 FIRE 視野。';
  else if (years <= 25) msg.textContent = '✅ 標準的な FIRE ペース。';
  else if (years <= 40) msg.textContent = '📊 通常 リタイア 年齢で 達成。';
  else msg.textContent = '💡 支出 削減 or 利回り アップで 大幅 短縮 可能。';
  document.getElementById('result').style.display = 'block';
};
""",
    "<dt>FIRE って 何？</dt><dd>Financial Independence, Retire Early (経済的自立・早期退職)。米国で 流行し 日本にも 浸透。「働かなくても 資産運用 だけで 生活費を 賄える」 状態。</dd><dt>4%ルール は 日本でも 通用する？</dt><dd>米国 株式 中心の 統計なので 完全 適用は 難しい。日本だけ だと インフレや 為替で 3% 程度が 安全圏と される ことも。本ツールは 簡易計算。</dd>",
))


# ---------- 70. タクシー料金 概算 ----------
TOOLS.append((
    "taxi-fare", "🚕", "タクシー料金 概算 (主要都市)",
    "距離 (km) と 都市から タクシー料金を 即時 概算。深夜・休日 加算 対応。",
    """    <label>都市:</label>
    <select id="city" class="in">
      <option value="tokyo" selected>東京 23区・三鷹・武蔵野</option>
      <option value="osaka">大阪・神戸・京都 (関西)</option>
      <option value="nagoya">名古屋・福岡・札幌 (主要)</option>
      <option value="other">その他 地方</option>
    </select>
    <label>距離 (km):</label>
    <input id="km" class="in" type="number" step="0.1" value="3.0" />
    <label>時間帯:</label>
    <select id="time" class="in">
      <option value="day" selected>日中 (5時〜22時)</option>
      <option value="night">深夜・早朝 (22時〜5時・2割増)</option>
    </select>
    <label>渋滞・信号 待ち (分):</label>
    <input id="wait" class="in" type="number" value="2" />
    <div class="bar"><button type="button" class="btn primary" id="calc">料金 概算</button></div>
    <div class="cards">
      <div class="cell"><div class="num" id="fare" style="color:#16a34a;">¥0</div><div class="cap">概算 料金</div></div>
      <div class="cell"><div class="num" id="electronic">¥0</div><div class="cap">迎車 含む</div></div>
    </div>
    <h2>運賃 体系 (主要 都市・2024)</h2>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr style="background:#f1f5f9;"><th>都市</th><th>初乗り</th><th>加算</th></tr>
      <tr><td>東京</td><td>500円 (1.096km)</td><td>100円 / 255m</td></tr>
      <tr><td>関西</td><td>600円 (1.3km)</td><td>100円 / 246m</td></tr>
      <tr><td>名古屋ほか</td><td>500円 (1km)</td><td>90円 / 233m</td></tr>
      <tr><td>地方</td><td>500-700円</td><td>地域差大</td></tr>
    </table>
""",
    """
const RATES = {
  tokyo:   {init: 500, initKm: 1.096, addYen: 100, addM: 255},
  osaka:   {init: 600, initKm: 1.3,   addYen: 100, addM: 246},
  nagoya:  {init: 500, initKm: 1.0,   addYen: 90,  addM: 233},
  other:   {init: 600, initKm: 1.5,   addYen: 90,  addM: 270},
};
document.getElementById('calc').onclick = () => {
  const city = document.getElementById('city').value;
  const km = parseFloat(document.getElementById('km').value) || 0;
  const isNight = document.getElementById('time').value === 'night';
  const wait = parseFloat(document.getElementById('wait').value) || 0;
  const r = RATES[city];
  let fare = r.init;
  if (km > r.initKm) {
    const extraM = (km - r.initKm) * 1000;
    const extraCount = Math.ceil(extraM / r.addM);
    fare += extraCount * r.addYen;
  }
  // 時間距離併用: 時速10km未満 (渋滞時) で 加算
  // 簡易: 渋滞分 = 1.5分 ごとに +100円
  fare += Math.floor(wait / 1.5) * 100;
  if (isNight) fare = Math.ceil(fare * 1.2);
  const fmt = v => '¥' + Math.round(v).toLocaleString('ja-JP');
  document.getElementById('fare').textContent = fmt(fare);
  document.getElementById('electronic').textContent = fmt(fare + 420); // 迎車料金 平均
};
""",
    "<dt>本当の 料金と 違う？</dt><dd>初乗り・加算は ほぼ 正確ですが、ルート (距離) は タクシーアプリで 確認したほうが 正確。本ツールは 「直線距離」 ではなく 「走行距離」 を 入れて ください。</dd><dt>GO・S.RIDE 等の アプリ?</dt><dd>料金は メーター 通り (差なし)。クーポン・配車料金 (300-500円) が プラスに なる ことが あります。</dd>",
))


def main():
    import json
    # 関連ツール 用 JSON データ
    all_tools_json = json.dumps([
        {"slug": t[0], "icon": t[1], "title": t[2], "desc": t[3]}
        for t in TOOLS
    ], ensure_ascii=False)

    for slug, icon, title, desc, body, script, faq in TOOLS:
        d = BASE / slug
        d.mkdir(exist_ok=True)
        extra = ""
        if faq:
            extra = f"<h2>よくある質問</h2><dl class=\"faq\">{faq}</dl>"
        full = PAGE_TPL.format(
            slug=slug, title=title, desc=desc, icon=icon,
            body=body, extra=extra,
            script=f"<script>\n{script}\n</script>" if script else "",
        )
        # プレースホルダ 置換
        full = full.replace("SITE_URL", SITE_URL)
        full = full.replace("GA4_ID", GA4_ID)
        full = full.replace("ADSENSE_CLIENT", ADSENSE_CLIENT)
        full = full.replace("ALL_TOOLS_JSON", all_tools_json)
        (d / "index.html").write_text(full, encoding="utf-8")

    # robots.txt
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (BASE / "robots.txt").write_text(robots, encoding="utf-8")

    # sitemap.xml
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [
        ("", "1.0", "weekly"),  # トップ
    ]
    for t in TOOLS:
        urls.append((t[0] + "/", "0.8", "monthly"))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path, priority, freq in urls:
        sitemap += f"  <url>\n    <loc>{SITE_URL}/{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n"
    sitemap += "</urlset>\n"
    (BASE / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    # favicon.svg (シンプルな絵文字 アイコン)
    favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#2b7de9"/><text x="32" y="46" font-size="40" text-anchor="middle" fill="white">🛠</text></svg>"""
    (BASE / "favicon.svg").write_text(favicon, encoding="utf-8")

    # _headers (Cloudflare Pages 用 セキュリティ・キャッシュヘッダ)
    headers = """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/style.css
  Cache-Control: public, max-age=86400

/sitemap.xml
  Cache-Control: public, max-age=3600
"""
    (BASE / "_headers").write_text(headers, encoding="utf-8")

    out = f"生成: {len(TOOLS)} ツール + robots.txt + sitemap.xml + favicon.svg + _headers\n"
    for t in TOOLS:
        out += f"  - {t[0]}/\n"
    (BASE / "_generate.log").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
