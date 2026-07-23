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

## 7. 引き継ぎ（次の人がやること）

> 現在の状態（2026-07-23）: **本番稼働・完全日本語化・実機検証済み**。管理画面/公開ページとも Hakobu ブランド＋日本語で動作。**唯一「実際のメール送信（SES）」だけ未設定**。下記を上から順にやれば配信開始できる。

### ステップ A — Amazon SES 設定【実配信の要・最優先】
実際にメールを送るにはこれが必須（未設定だとキャンペーンを送っても届かない）。

1. **AWS SES を開く**（AWSアカウントが必要）。リージョンは **`ap-northeast-1`（東京）** 推奨。
2. **送信元の検証**: SES → 「Verified identities」→ Create identity
   - ドメインで検証（推奨）: 自社ドメインを入力 → 表示される **DKIM/SPF の DNS レコードをドメインの DNS に追加** → 検証完了を待つ。
   - or 単一メールアドレスで検証（手軽）: アドレスを入力 → 届いた確認メールのリンクをクリック。
3. **サンドボックス解除**: SES → 「Account dashboard」→ **Request production access**。
   - ⚠未解除だと「検証済みの宛先」にしか送れない（本番配信は不可）。申請は数時間〜1日。
4. **SMTP 認証情報を作成**: SES → 「SMTP settings」→ **Create SMTP credentials**
   - 発行される **SMTP ユーザー名 / パスワードを保存**（※ IAM のアクセスキーとは別物。必ず SMTP credentials）。
5. **Hakobu 管理画面に入力**: `/admin/login`（admin / PWは §3）→ **設定 → SMTP**（タブ）→ 有効化して:
   - Host: `email-smtp.ap-northeast-1.amazonaws.com`（リージョンに合わせる）
   - Port: `587` ／ 認証: `STARTTLS`（LOGIN）
   - Username / Password: 手順4の SMTP 認証情報
   - 保存。
6. **送信元アドレスを実値に**: 設定 → 汎用 → 「メールの`送り主`をデフォルトにする」を **SES で検証済みのアドレス**へ。
   - 現在は `Hakobu <noreply@mail.yoursite.com>`（プレースホルダ）。例: `Hakobu <news@自社ドメイン>`。
7. **送信テスト**: 購読者を1件作成 → キャンペーン作成 → 「テストメッセージを送信」で自分宛に届くか確認 → OKなら本配信可。

### ステップ B — Render 有料化【本番運用なら推奨】
無料枠のままだと (1) 15分アクセスが無いとスリープ（次アクセス〜50秒待ち）、(2) **無料 PostgreSQL は約90日（〜2026-08-21頃）で削除**される。

1. Render Dashboard → **ikemen-mailer** → Settings → Instance Type → **Starter（$7/月）**（スリープ無効化）。
2. Render Dashboard → **ikemen-mailer-db** → 有料プランにアップグレード（無料PGの期限切れ＝データ消失を回避）。
3. Starter にしたら `.github/workflows/keepalive.yml`（10分ping）は不要 → 削除してよい。

### ステップ C — 任意の仕上げ
- jp.json の言い回しのネイティブ校正（値は日本語だが一部機械翻訳調）。
- モバイル実機でのレイアウト確認。
- 独自ドメイン割り当て（Render Settings → Custom Domain。例 `mail.自社ドメイン`）→ その場合 `app.root_url` と SES 送信元もそのドメインに合わせる。

### デプロイの反映方法（コード変更時）
public repo 接続のため push だけでは反映されない。**Render Dashboard → Manual Deploy → Deploy latest commit** を押す（§2）。DBは消えない（FORCE_REINSTALL は削除済み）。

## 8. 補助スクリプト（scratchpad、参考）
- ロゴ生成: `branding_src/gen_assets.py`
- ラベル/英語監査: `branding_src/label_audit.txt`, `branding_src/jp_english_scan.txt`
