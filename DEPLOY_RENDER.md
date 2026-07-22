# IKEMEN MAILER — Render 本番デプロイ手順（無料枠）

listmonk フォークを Render に無料デプロイし、Amazon SES で配信するための手順。
リポジトリに同梱済み:

- `render.yaml` … Blueprint（無料PostgreSQL + 無料Docker Webサービス + env配線を一括定義）
- `Dockerfile.render` … ソースから単一バイナリをビルド（Go + Vue + email-builder を `make dist`）
- `render-entrypoint.sh` … `$PORT`バインド + 初回スキーマ作成 + 移行 + 起動

---

## 1. Blueprint でデプロイ（ワンクリック）

1. https://render.com にログイン（GitHubアカウントで可）
2. **New → Blueprint**
3. `IKEMENLTD/ikemen-mailer` を選択（初回は GitHub 連携の承認が必要）
4. Render が `render.yaml` を読み込み、**PostgreSQL + Webサービス**を自動作成
5. **Apply** → ビルド開始（初回は Go+yarn の2重ビルドで数分〜十数分）

## 2. 管理者パスワードを取得

Render Dashboard → **ikemen-mailer** サービス → **Environment** →
`LISTMONK_ADMIN_PASSWORD` の値（Renderが自動生成）を確認・コピー。

→ 発行された URL `https://ikemen-mailer.onrender.com`（名前は変わる場合あり）に
アクセスし、`admin` / そのパスワードでログイン。

> **無料枠の注意**: 15分アクセスが無いと Web サービスがスリープし、次アクセスで
> コールドスタート（30秒〜）。無料 PostgreSQL は**90日で期限切れ**（以後は有料 or 作り直し）。
> 本番で定期配信を回すなら、Web を Starter($7/月)に上げてスリープを無効化するのが安全。

---

## 3. Amazon SES 設定（配信の要）

listmonk の SMTP はデプロイ後に**管理画面で設定**する（env ではない）。

### 3-1. SES 側（AWSコンソール）
1. リージョン選択（例: `ap-northeast-1` 東京）
2. **Verified identities** でドメイン(または送信元アドレス)を検証（SPF/DKIM のDNSレコード追加）
3. **SMTP settings → Create SMTP credentials** で **SMTPユーザー名/パスワード**を発行
   （※ IAMアクセスキーとは別物。必ず SMTP credentials を使う）
4. サンドボックス解除: **Request production access**（未解除だと検証済みアドレスにしか送れない）

### 3-2. IKEMEN MAILER 側（管理画面 → Settings → SMTP）
| 項目 | 値 |
|---|---|
| Host | `email-smtp.ap-northeast-1.amazonaws.com`（リージョンに合わせる） |
| Port | `587` |
| Auth protocol | `STARTTLS`（login） |
| Username | SES の SMTP ユーザー名 |
| Password | SES の SMTP パスワード |
| Max connections | 10 程度から |

### 3-3. 送信元アドレス
**Settings → General → "Default from email"** を SES で検証済みの identity に合わせる
（例: `news@yourdomain.jp`）。送信テスト: 購読者1件 → キャンペーン → **Send test**。

---

## トラブルシューティング

- **ビルド失敗**: Render の Logs を確認。Goバージョン(`golang:1.26.1-bookworm`)や
  frontend の eslint(`prebuild`)で落ちることがある。ログを貼ってくれれば修正する。
- **DB接続エラー**: `LISTMONK_db__ssl_mode=require`（Render Postgres はSSL必須）を確認。
- **502 / 起動しない**: Logs に `Starting IKEMEN MAILER on 0.0.0.0:<PORT>` が出ているか。
- **メールが届かない**: SESサンドボックス未解除 / 送信元未検証 / SMTP認証情報の取り違え が定番。
