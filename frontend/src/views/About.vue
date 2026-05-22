<template>
  <section class="about content">
    <header class="page-header">
      <h1 class="title is-4">About IKEMEN MAILER</h1>
    </header>

    <div class="about-grid">
      <article class="box about-card">
        <h2 class="about-label">Product</h2>
        <p class="about-value">IKEMEN MAILER</p>
        <p class="about-meta">
          Self-hosted newsletter &amp; mailing-list platform for IKEMEN-LTD.
        </p>
      </article>

      <article class="box about-card">
        <h2 class="about-label">Version</h2>
        <p class="about-value">{{ serverConfig.version || '—' }}</p>
        <p class="about-meta">
          Build channel: stable
        </p>
      </article>

      <article class="box about-card">
        <h2 class="about-label">License</h2>
        <p class="about-value">AGPL-3.0</p>
        <p class="about-meta">
          Network-use disclosure required. See source link below.
        </p>
      </article>
    </div>

    <article class="box about-attribution">
      <h2 class="about-attribution-title">Open-source attribution</h2>
      <p>
        IKEMEN MAILER is built on top of
        <a href="https://github.com/knadh/listmonk" target="_blank" rel="noopener noreferrer">listmonk</a>
        (Copyright &copy; Kailash Nadh), distributed under the
        <a href="https://www.gnu.org/licenses/agpl-3.0.en.html" target="_blank" rel="noopener noreferrer">GNU Affero General Public License v3.0</a>.
      </p>
      <p>
        In accordance with AGPL &sect;13, the complete corresponding source code for this running instance,
        including all IKEMEN MAILER modifications, is available at:
      </p>
      <p>
        <a href="https://github.com/IKEMENLTD/ikemen-mailer" target="_blank" rel="noopener noreferrer" class="about-source">
          github.com/IKEMENLTD/ikemen-mailer
        </a>
      </p>
      <p class="about-upstream-doc">
        Upstream documentation: <a href="https://listmonk.app/docs/" target="_blank" rel="noopener noreferrer">listmonk.app/docs</a>
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
