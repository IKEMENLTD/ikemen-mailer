# IKEMEN MAILER — Railway 本番デプロイ手順

listmonk フォーク（Go + PostgreSQL + SMTP）を Railway に本番デプロイし、Amazon SES で
配信するための手順。リポジトリには以下を同梱済み:

- `Dockerfile.railway` … ソースからビルド（Goバックエンド + Vueフロント + email-builder を単一バイナリにパック）
- `railway-entrypoint.sh` … `$PORT` バインド + 初回スキーマ作成(`--install --idempotent`) + 移行(`--upgrade`) + 起動
- `railway.toml` … Railway に `Dockerfile.railway` でビルドさせる指定

---

## 1. Railway プロジェクト作成

1. https://railway.app → **New Project** → **Deploy from GitHub repo** → `IKEMENLTD/ikemen-mailer` を選択
2. Railway が `railway.toml` を読んで `Dockerfile.railway` で自動ビルド開始（初回は数分。Go+yarn の2重ビルドで重め）

## 2. PostgreSQL を追加

1. 同じプロジェクト内で **New → Database → Add PostgreSQL**
2. これで `Postgres` サービスが生え、`PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE` が使えるようになる

## 3. アプリの環境変数（Variables）を設定

`ikemen-mailer` サービス → **Variables** に以下を登録。DB系は Postgres サービスの参照(`${{Postgres.*}}`)で繋ぐ:

| Key | Value |
|---|---|
| `LISTMONK_db__host` | `${{Postgres.PGHOST}}` |
| `LISTMONK_db__port` | `${{Postgres.PGPORT}}` |
| `LISTMONK_db__user` | `${{Postgres.PGUSER}}` |
| `LISTMONK_db__password` | `${{Postgres.PGPASSWORD}}` |
| `LISTMONK_db__database` | `${{Postgres.PGDATABASE}}` |
| `LISTMONK_db__ssl_mode` | `disable` |
| `LISTMONK_db__max_open` | `25` |
| `LISTMONK_db__max_idle` | `25` |
| `LISTMONK_db__max_lifetime` | `300s` |
| `TZ` | `Asia/Tokyo` |
| `LISTMONK_ADMIN_USER` | `admin` |
| `LISTMONK_ADMIN_PASSWORD` | （強いパスワードを設定） |

> `LISTMONK_app__address` は entrypoint が `$PORT` から自動生成するので**設定不要**。
> `LISTMONK_ADMIN_USER/PASSWORD` は初回インストール時にスーパー管理者を自動作成する。

## 4. 公開 URL を発行

`ikemen-mailer` サービス → **Settings → Networking → Generate Domain**。
Railway が `$PORT` を注入し entrypoint がそこにバインドするので、ポート指定は基本自動。
（自動検出されない場合は target port に `$PORT` の値を指定）

→ `https://<yourapp>.up.railway.app` にアクセスし、上で設定した admin / パスワードでログイン。

---

## 5. Amazon SES 設定（配信の要）

listmonk の SMTP はデプロイ後に**管理画面で設定**する（env ではない）。

### 5-1. SES 側の準備（AWSコンソール）
1. リージョン選択（例: `ap-northeast-1` 東京）
2. **Verified identities** でドメイン(または送信元アドレス)を検証（SPF/DKIM のDNSレコードを追加）
3. **SMTP settings → Create SMTP credentials** で **SMTPユーザー名/パスワード**を発行
   （※ IAMのアクセスキーとは別物。必ず SMTP credentials を使う）
4. サンドボックス解除: **Request production access**（未解除だと検証済みアドレスにしか送れない）

### 5-2. IKEMEN MAILER 側（管理画面 → Settings → SMTP）
| 項目 | 値 |
|---|---|
| Host | `email-smtp.ap-northeast-1.amazonaws.com`（リージョンに合わせる） |
| Port | `587` |
| Auth protocol | `STARTTLS`（login） |
| Username | SES の SMTP ユーザー名 |
| Password | SES の SMTP パスワード |
| Max connections | 10 程度から |

### 5-3. 送信元アドレス
**Settings → General → "Default from email"** を SES で検証済みの identity に合わせる
（例: `news@yourdomain.jp`）。ドメイン未検証のアドレスは SES が拒否する。

送信テスト: 購読者を1件作成 → キャンペーン作成 → **Send test** で自分宛に届くか確認。

---

## トラブルシューティング

- **ビルド失敗**: Railway の Build Logs を確認。Go バージョン(`golang:1.26.1-bookworm`)/yarn ビルドの
  eslint(`prebuild`)で落ちることがある。ログを貼ってくれれば修正する。
- **DB接続エラー**: `LISTMONK_db__ssl_mode=disable` と Postgres 参照(`${{Postgres.*}}`)を再確認。
- **メールが届かない**: SES サンドボックス未解除 / 送信元未検証 / SMTP認証情報の取り違え(IAMキーを使っている)が定番。
- **502/起動しない**: entrypoint が `$PORT` にバインドできているか（Deploy Logs の `Starting IKEMEN MAILER on 0.0.0.0:xxxx`）。
