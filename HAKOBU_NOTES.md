# Hakobu — カスタマイズ & 運用ノート

listmonk（`knadh/listmonk`）をフォークした自社メール配信ツール **Hakobu** の、リブランド・日本語化・本番デプロイ・修正の記録。上流とマージする際やトラブル時はまずここを読む。

---

## 1. 概要
- **正体**: listmonk フォーク（Go + Vue 2 + PostgreSQL、単一バイナリ）。
- **ブランド**: 「Hakobu」（箱＝立方体ロゴ ＋ 運ぶ＝配信 の二重意味）。旧称「IKEMEN MAILER」は全廃。
- **言語**: 日本語専用（`app.lang=jp`。listmonk の日本語コードは `ja` ではなく **`jp`**）。
- **本番URL**: https://ikemen-mailer.onrender.com
  - ※サービス/リポジトリ識別子は `ikemen-mailer` のまま（変更すると本番URL・Render・GitHub連携が壊れるため）。表向きのブランドのみ Hakobu。

## 2. 本番デプロイ（Render 無料枠）
- `render.yaml`（Blueprint）… 無料 PostgreSQL + 無料 Docker Web サービス + env 配線。
- `Dockerfile.render`（`make dist` でソースから単一バイナリをビルド）+ `render-entrypoint.sh`（`$PORT` バインド → `--install --idempotent` → `--upgrade` → 起動）。
- **public repo 接続**のため push では自動デプロイされない → Render Dashboard → Manual Deploy → **Deploy latest commit** で手動反映。
- 手順詳細は `DEPLOY_RENDER.md`。

### ⚠ 運用上の重大な落とし穴
1. **`LISTMONK_ADMIN_PASSWORD` は初回インストール（空DB）時しか admin PW を設定しない。** 後から env を変えても既存 admin には無反映。誤設定で締め出されたら `render-entrypoint.sh` の `FORCE_REINSTALL=1` ゲート（空DBを再 `--install`）で復旧。**復旧後は必ず env から `FORCE_REINSTALL` を削除**。
2. **Render の env 削除は「Save only」では永続しないことがある** → 「**Save and deploy**」で確実に反映。削除後は必ず再読込＋確認。
3. 無料枠: 15分アクセスが無いとスリープ。→ `.github/workflows/keepalive.yml` が10分ごとに ping（GitHub Actionsのジッターで稀に超過）。無料 PostgreSQL は**約90日で期限切れ** → 本番運用は Render Starter（$7/月）昇格推奨。
4. このマシンからは**外部 PostgreSQL 5432 がネットワーク遮断**でDB直結不可（TCPは通るがSSLRequest応答なし）。DB操作は管理画面 or API 経由で。

## 3. 管理者ログイン
- URL: `/admin/login` ／ user: `admin` ／ PW: Render Dashboard → ikemen-mailer → Environment の `LISTMONK_ADMIN_PASSWORD`。
- API 操作は nonce(CSRF) 必須: GET `/admin/login` で nonce 取得 → POST `/admin/login`（username/password/nonce）→ `session` cookie。成功=302。

## 4. ブランディング（ロゴ・ファビコン・名称）
- 新ロゴ（青い立方体 #004AAD ＋吹き出し）を `logo.svg` / `logo-mark.svg` / `logo.png` / `favicon.png` に反映。
  - 管理: `frontend/src/assets/`、公開: `static/public/static/`、`frontend/public/static/favicon.png`。
  - 生成スクリプト: `branding_src/gen_assets.py`（元画像 `branding_src/logo-source.png`）。ロゴを差し替える時はこれを再実行。
- ワードマーク「Hako(濃紺)bu(#004AAD)」。
- 表示文字列 "IKEMEN MAILER" → "Hakobu" 全置換（識別子/URLの小文字 `ikemen-mailer` と listmonk 帰属は温存）。
- サイト名/送信元は稼働DBに API で設定: `app.site_name=Hakobu`、`app.from_email=Hakobu <...>`。

## 5. 日本語化・UX（実機シミュレーション＋監査で修正）
- `app.lang=jp`、`index.html` / 公開テンプレ（home/index）の `<html lang="ja">`。
- i18n（`i18n/jp.json`）: 未翻訳・誤訳を全て修正。**残英語=0件**。主な修正:
  - 誤訳バグ: `globals.terms.year`「都市」→「年」、`globals.buttons.new`「新」→「新規」。
  - 未翻訳: analytics/settings 系、`settings.general.siteName`「ウエブサイト」誤字 等。
  - **用語統一**: 「加入／加入者／サブスクリプション」→「**購読／購読者**」（購読解除）に統一。
- 日付を日本語自然表記に:
  - `utils.js` niceDate → 「2026年7月23日(木)」。
  - `constants.js` timestamp・`Dashboard.vue` グラフ軸・`App.vue` 更新日 の英語月(`DD MMM`等)を数字表記に。
  - `formatDateTime`（Campaign/CampaignAnalytics/Maintenance）は `YYYY-MM-DD` で問題なし。
- Vue ハードコード英語の日本語化: About.vue 全体 / App.vue（レガシー警告・skip-link・View・toast）/ 404.vue（メッセージ＋「ダッシュボードに戻る」導線）/ 各種 label・placeholder・aria・toast。
- 8ビューの空状態に初回誘導文（CTA）、削除確認に対象名を明示。
- **英語 listmonk.app ドキュメントリンクを除去**（日本語ユーザーが読めないため）。※About.vue の AGPL 帰属リンクのみ法的義務で保持。
- シードリスト名を日本語化（「デフォルトリスト」「オプトインリスト」）。

## 6. 検証済みの動作（実機）
- ログイン、ダッシュボード、リスト、購読者、キャンペーン編集、設定 … 全画面 日本語＋Hakobu。
- **公開購読フロー**: 公開フォームから送信 → 購読者登録成功を実機確認。
- 公開ページ（トップ/購読フォーム/アーカイブ）… 日本語＋Hakobu＋`lang="ja"`。

## 7. 残タスク
- **Amazon SES 設定**（実配信の要）: 管理画面 Settings → SMTP に SES の SMTP 認証情報。`app.from_email` を SES 検証済みドメインへ。詳細は `DEPLOY_RENDER.md` §3。
- 本番運用なら Render Starter 昇格（スリープ無効化・PG 永続化）。
- jp.json のネイティブ言い回し校正（値は日本語だが一部機械翻訳調）。

## 8. 補助スクリプト（scratchpad、参考）
- ロゴ生成: `branding_src/gen_assets.py`
- ラベル/英語監査: `branding_src/label_audit.txt`, `branding_src/jp_english_scan.txt`
