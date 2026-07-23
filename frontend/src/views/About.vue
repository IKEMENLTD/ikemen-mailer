<template>
  <section class="about content">
    <header class="page-header">
      <h1 class="title is-4">Hakobu について</h1>
    </header>

    <div class="about-grid">
      <article class="box about-card">
        <h2 class="about-label">製品</h2>
        <p class="about-value">Hakobu</p>
        <p class="about-meta">
          IKEMEN-LTD 向けの自社ホスト型メール配信・メーリングリスト基盤です。
        </p>
      </article>

      <article class="box about-card">
        <h2 class="about-label">バージョン</h2>
        <p class="about-value">{{ serverConfig.version || '—' }}</p>
        <p class="about-meta">
          リリースチャネル: stable（安定版）
        </p>
      </article>

      <article class="box about-card">
        <h2 class="about-label">ライセンス</h2>
        <p class="about-value">AGPL-3.0</p>
        <p class="about-meta">
          ネットワーク利用時のソース開示が必要です。下記のソースリンクをご覧ください。
        </p>
      </article>
    </div>

    <article class="box about-attribution">
      <h2 class="about-attribution-title">オープンソースの帰属表示</h2>
      <p>
        Hakobu は
        <a href="https://github.com/knadh/listmonk" target="_blank" rel="noopener noreferrer">listmonk</a>
        （Copyright &copy; Kailash Nadh）をベースに構築されており、
        <a href="https://www.gnu.org/licenses/agpl-3.0.en.html" target="_blank" rel="noopener noreferrer">GNU Affero General Public License v3.0</a>
        の下で配布されています。
      </p>
      <p>
        AGPL &sect;13 に従い、稼働中のこのインスタンスに対応する完全なソースコード（Hakobu による
        すべての改変を含む）は、以下で公開しています。
      </p>
      <p>
        <a href="https://github.com/IKEMENLTD/ikemen-mailer" target="_blank" rel="noopener noreferrer" class="about-source">
          github.com/IKEMENLTD/ikemen-mailer
        </a>
      </p>
      <p class="about-upstream-doc">
        上流のドキュメント: <a href="https://listmonk.app/docs/" target="_blank" rel="noopener noreferrer">listmonk.app/docs</a>
      </p>
    </article>
  </section>
</template>

<script>
import Vue from 'vue';
import { mapState } from 'vuex';

export default Vue.extend({
  computed: {
    ...mapState(['serverConfig']),
  },
});
</script>

<style lang="scss" scoped>
/* `:root` from `assets/style.scss` is guaranteed to load before this scoped
   block, so we consume `var(--ik-*)` without hex fallbacks — no token
   duplication, single source of truth. */
.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--ik-space-4);
  margin-bottom: var(--ik-space-6);
}
.about-card {
  padding: var(--ik-space-5) var(--ik-space-6);
}
.about-label {
  text-transform: uppercase;
  letter-spacing: var(--ik-tracking-wider);
  font-weight: var(--ik-weight-semibold);
  color: var(--ik-ink-500);
  font-size: var(--ik-text-xs);
  margin-bottom: var(--ik-space-2);
}
.about-value {
  font-weight: var(--ik-weight-semibold);
  font-size: var(--ik-text-lg);
  color: var(--ik-ink-900);
  margin: 0 0 var(--ik-space-2);
  line-height: var(--ik-leading-tight);
}
.about-meta {
  margin: 0;
  font-size: var(--ik-text-sm);
  color: var(--ik-ink-500);
}
.about-upstream-doc {
  margin: 0;
  font-size: var(--ik-text-sm);
  color: var(--ik-ink-500);
}
.about-attribution {
  padding: var(--ik-space-6) var(--ik-space-7);
}
.about-attribution-title {
  margin-bottom: var(--ik-space-3);
  font-weight: var(--ik-weight-semibold);
}
.about-attribution p {
  margin: 0 0 var(--ik-space-2);
  line-height: var(--ik-leading-base);
}
.about-source {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: var(--ik-text-sm);
}
</style>
