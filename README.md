# Hakobu

**Hakobu** is the self-hosted newsletter & mailing-list platform for IKEMEN-LTD and its client portfolio. It is built as a downstream of the open-source [listmonk](https://listmonk.app) project (AGPL-3.0), with a refreshed design system, brand identity, and operational tooling tuned for in-house and managed-service use.

> Built on top of [listmonk](https://github.com/knadh/listmonk) by Kailash Nadh — AGPL-3.0 licensed. All upstream copyrights and license obligations are preserved.

---

## What's different from upstream listmonk

| Area | listmonk (upstream) | **Hakobu** |
| --- | --- | --- |
| Brand | listmonk | Hakobu |
| Design system | Bulma defaults + custom CSS | Refined design tokens (color · type · spacing · shadow · radius), premium SaaS aesthetic |
| Color palette | `#0055d4` flat blue | Indigo 600 (`#4F46E5`) + Slate 900 text + Amber 500 accent |
| Sidebar | Right-border active indicator | Soft pill background + subtle gradient rail |
| Dashboard tiles | Hard-shadow boxes | Layered elevation cards with refined hover |
| Login / Public pages | Plain Bulma forms | Centered glass card on subtle gradient backdrop |
| Iconography | Material Design Icons (kept) + emoji decorations | Material Design Icons only — no emoji decorations (SVG-first house rule) |
| Footer | "Powered by listmonk" | "Hakobu · Powered by listmonk" (AGPL attribution preserved) |

The Go backend, schema, queries, i18n, and admin API surface remain compatible with upstream — making upstream security patches and feature merges straightforward.

---

## Installation

### Docker

```bash
# Download the compose file.
curl -LO https://raw.githubusercontent.com/IKEMENLTD/ikemen-mailer/master/docker-compose.yml

# Start the services.
docker compose up -d
```

Visit `http://localhost:9000`.

See the [upstream installation docs](https://listmonk.app/docs/installation) for environment variables, SMTP setup, and reverse-proxy templates — these apply unchanged.

### Binary

- Build from source: `make dist` (requires Go 1.21+ and Node 18+ with Yarn)
- Generate config: `./ikemen-mailer --new-config`
- Install schema: `./ikemen-mailer --install` (or `--upgrade` for existing DBs)
- Run: `./ikemen-mailer` and visit `http://localhost:9000`

---

## Development

Same dev loop as upstream listmonk:

```bash
make deps           # install Go + frontend dependencies
make build          # build backend binary
make build-frontend # build admin UI
make run            # run backend
make run-frontend   # run vite dev server (hot reload)
```

- Backend: **Go** (`/cmd`, `/internal`, `/models`, `/queries`)
- Frontend admin: **Vue 2 + Buefy + Bulma + SCSS** (`/frontend`)
- Public pages: Go HTML templates (`/static/public/templates`) + `static/public/static/style.css`
- Design tokens: `frontend/src/assets/style.scss` (top of file — `$ikemen-*` variables)

---

## Branding & assets

- Wordmark: `frontend/src/assets/logo.svg` and `static/public/static/logo.svg`
- Square mark: `frontend/src/assets/logo-mark.svg` and `static/public/static/logo-mark.svg`
- Favicon: `frontend/src/assets/favicon.png` and `static/public/static/favicon.png`

### Design tokens

All tokens are exported as CSS custom properties under `:root` with the **`--ik-*`** prefix. The same names appear in both `frontend/src/assets/style.scss` (admin) and `static/public/static/style.css` (public pages) — keep the two `:root` blocks in sync when tokens evolve.

| Category | Tokens |
| --- | --- |
| Brand | `--ik-primary` `#4F46E5`, `--ik-primary-deep` `#3730A3`, `--ik-primary-soft` `#EEF2FF`, `--ik-primary-rgb` `79, 70, 229`, `--ik-accent` `#F59E0B`, `--ik-accent-soft` `#FEF3C7` |
| Semantic | `--ik-success` `#059669` + `-soft`, `--ik-danger` `#DC2626` + `-soft`, `--ik-warning` `#D97706` + `-soft`, `--ik-info` `#2563EB` + `-soft` |
| Ink ramp | `--ik-ink-900` `#0F172A` (body), `--ik-ink-700` `#334155` (secondary), `--ik-ink-500` `#64748B` (muted / placeholder — 4.76:1 on white), `--ik-ink-400` `#94A3B8` (**decorative only — 2.54:1 on white, NOT for text**), `--ik-ink-300` `#CBD5E1` (disabled) |
| Surfaces | `--ik-surface` `#FFFFFF`, `--ik-bg` `#F8FAFC`, `--ik-bg-deep` `#EEF2F7`, `--ik-line` `#E2E8F0`, `--ik-line-soft` `#F1F5F9`, `--ik-overlay` `rgba(15,23,42,.45)` |
| Elevation | `--ik-shadow-xs/sm/md/lg/xl`, `--ik-shadow-focus`, `--ik-shadow-primary-sm/md` |
| Radius | `--ik-radius-xs` 4, `-sm` 6, `-md` 8, `-lg` 12, `-xl` 16, `-pill` 999 |
| Spacing (4px base) | `--ik-space-1..10` → 4, 8, 12, 16, 20, 24, 32, 40, 56, 80 px |
| Typography (size) | `--ik-text-xs` 12, `-sm` 14, `-base` 15 (body), `-md` 16 (controls/CTA), `-lg` 18, `-xl` 24, `-2xl` 32, `-3xl` 36; line-height: `--ik-leading-tight/snug/base` |
| Typography (weight) | `--ik-weight-regular` 400, `--ik-weight-medium` 500, `--ik-weight-semibold` 600, `--ik-weight-bold` 700 |
| Typography (tracking) | `--ik-tracking-tight` -0.02em, `-snug` -0.01em, `-normal` 0, `-wide` 0.04em, `-wider` 0.08em |
| Motion | `--ik-ease` cubic-bezier(0.4,0,0.2,1), `--ik-dur-fast` 120ms, `--ik-dur` 200ms, `--ik-dur-slow` 320ms |
| Z-index | `--ik-z-base` 1, `-sticky` 100, `-sidebar` 200, `-navbar` 300, `-overlay` 800, `-modal` 900, `-toast` 1000 |

The SCSS-side variables share the same names with a `$ikemen-*` prefix (e.g. `$ikemen-primary` ⇄ `--ik-primary`), preserved as a thin alias so existing listmonk SCSS code keeps compiling against the new palette.

> **Note on theming surface:** Admin (Vue) components in `style.scss` consume the SCSS scalars (`$ikemen-*`) at compile time, not the CSS variables. The `:root` block exposing `--ik-*` exists so consumer code (custom dashboards, `custom.css` overrides, JS that reads `getComputedStyle`) can read the same tokens. Runtime theme switching of the admin shell via `--ik-*` overrides is therefore limited — change SCSS scalars and rebuild for theme variations.

### Component scope

The Hakobu design layer wraps all admin overrides in a single `body.ikemen-skin { … }` block (bottom of `style.scss`, after the comment marker `Hakobu — Premium overrides v2`). The body class is set in `frontend/index.html` on the `<body>` element. This raises the override layer's specificity to `(0,2,X)` against upstream listmonk's `(0,1,X)` rules — overrides win independent of source order, so future rebases against upstream listmonk are safe.

---

## License

Hakobu is distributed under the **GNU Affero General Public License v3.0** (AGPL-3.0), inherited from upstream listmonk.

- Upstream: <https://github.com/knadh/listmonk> — Copyright © Kailash Nadh
- Source-availability obligations: if you run a modified Hakobu as a network service, you must offer the source code to its users. The full source for this fork is hosted at <https://github.com/IKEMENLTD/ikemen-mailer>.

See [LICENSE](./LICENSE) for the full text.
