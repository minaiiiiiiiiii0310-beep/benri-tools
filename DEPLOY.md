# ツールサイト デプロイ & 収益化 設定ガイド

このガイドに沿って作業すれば、サイトが公開され、アクセスが計測され、広告収益が発生します。

## 🎯 目標 ROI

- **デプロイから 3ヶ月**: 月間 5,000-10,000 PV (主にバイラル系記事)
- **6ヶ月目**: 月間 30,000-50,000 PV、AdSense 月収 5,000-15,000円
- **12ヶ月目**: 月間 100,000 PV、AdSense + アフィリで 月 30,000-80,000円

## Step 1: Cloudflare Pages でデプロイ (無料・5分)

### 1-A. GitHub にリポジトリ作成
```bash
cd C:/Users/81806/ニュースサイト/tools-site
git init
git add .
git commit -m "Initial commit: 80 tools"
gh repo create benri-tools --public --source=. --push
```

### 1-B. Cloudflare Pages でデプロイ
1. https://dash.cloudflare.com/ にログイン
2. Workers & Pages → Create application → Pages → Connect to Git
3. リポジトリ `benri-tools` を選択
4. Build settings:
   - Framework preset: **None** (静的サイト)
   - Build command: 空欄 OR `python _generate.py`
   - Build output directory: `/` (ルート)
5. Save and Deploy

→ `https://benri-tools.pages.dev` が公開されます。

### 1-C. カスタムドメイン (推奨・年1,500円程度)
1. お名前.com・ムームードメイン等で `.com` か `.jp` を取得 (例: `benri-tools.com`)
2. Cloudflare Pages → Custom domains → ドメインを追加
3. DNS 設定指示通りに

## Step 2: Google Analytics 4 設定 (無料・10分)

1. https://analytics.google.com/ にアクセス
2. 「測定を開始」→ アカウント名 → プロパティ名「便利ツール」
3. データストリーム → ウェブ → URL: `https://benri-tools.com`
4. **測定ID `G-XXXXXXXXXX` をコピー**
5. `_generate.py` の `GA4_ID` を実IDに置換
6. `python _generate.py` 再実行 → git commit & push → 自動デプロイ
7. `index.html` の `G-XXXXXXXXXX` も置換 (2箇所)

```python
# _generate.py の冒頭
GA4_ID = "G-ABCD12345"  # ← 実IDに
SITE_URL = "https://benri-tools.com"  # ← 実URLに
```

## Step 3: Google Search Console 登録 (無料・5分)

1. https://search.google.com/search-console/
2. プロパティを追加 → URLプレフィックス → `https://benri-tools.com/`
3. 所有権確認 (HTML タグ or DNS)
4. **サイトマップ送信**: `sitemap.xml` を URL欄に入力 → 送信
5. クローラーが3-7日でインデックス開始

## Step 4: Google AdSense 申請 (無料・審査1-4週間)

**重要**: AdSense は審査があります。以下の条件を満たしてから申請してください:

- ✅ 独自ドメイン (`.pages.dev` でなく自前ドメイン)
- ✅ ある程度のコンテンツ (80ツール + about + privacy → 既に満たす)
- ✅ プライバシーポリシー (既に作成済み)
- ✅ お問い合わせページ (既に作成済み)
- ✅ 最低 1-2 週間 公開している実績

### 申請手順
1. https://www.google.com/adsense/ にログイン
2. 「お申し込みはこちら」→ サイトURL入力
3. 審査用コード `<script>` を `<head>` に貼る (既に PAGE_TPL に組み込み済み・`ca-pub-` を実IDに)
4. 審査結果待ち (1-4週間)
5. 承認後、`_generate.py` の `ADSENSE_CLIENT` を実IDに置換 → 再生成 → push

## Step 5: アフィリエイト追加 (任意・収益アップ)

### Amazon アソシエイト (個人推奨)
1. https://affiliate.amazon.co.jp/ で登録
2. 各ツールの「次の行動」セクションに関連商品リンク
3. 例:
   - 健康診断ツール → 血圧計・体重計
   - FIRE ツール → 投資本「ジェイソン流お金の増やし方」
   - 副業ツール → 副業本

### A8.net (高単価)
1. https://www.a8.net/ で登録
2. 金融・保険・転職系プログラムと提携
3. 該当ツールにバナー設置

## 🚀 アクセス爆発 戦略 (Step 6)

### バイラル系を SNS に流す
- **MBTI 診断** → X で「MBTI診断」ハッシュタグ投稿
- **動物占い** → Instagram ストーリーズ
- **同年代年収偏差値** → TikTok 動画化
- **人生残り時間** → YouTube ショート

### SEO 強化
- 各ツールの記事化 (500-1000字の解説を追加)
- 内部リンク強化 (関連ツール → 既に実装済み)
- ロングテール キーワード対策

## 📊 KPI モニタリング (毎週)

GA4 で以下を確認:
- **ユーザー数** (週次推移)
- **ページビュー数**
- **平均エンゲージメント時間** (1分以上が目標)
- **離脱率** (50%以下が目標)
- **流入チャネル** (オーガニック検索 / 直接 / SNS)
- **人気ページ TOP10** (どのツールが伸びているか)

Search Console で以下を確認:
- **インデックス状況** (80ページが「有効」になるまで)
- **表示回数 / クリック数 / CTR**
- **検索クエリ** (ユーザーが何で検索して来ているか)

## 🔧 PDCA (改善サイクル)

1. **週1**: GA4 / Search Console チェック
2. **月1**: 伸びていないツールを記事化・SNS拡散
3. **月1**: 新ツール追加 (1-3個)
4. **3ヶ月毎**: AdSense 配置 A/B テスト

## ⚠️ 注意事項

- **AdSense 自己クリック厳禁** (アカウント停止)
- **個人情報を扱わない方針を維持** (プライバシー差別化)
- **薬機法・景品表示法** (健康・投資ツールの表現に注意)
