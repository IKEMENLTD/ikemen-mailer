<template>
  <section class="page-404">
    <h1 class="title">
      404
    </h1>
    <p class="subtitle">
      お探しのページが見つかりませんでした。
    </p>
    <router-link class="button is-primary" :to="{ name: 'dashboard' }">
      ダッシュボードに戻る
    </router-link>
  </section>
</template>

<script>
import Vue from 'vue';

export default Vue.extend({
});
</script>
