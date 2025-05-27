<template>

  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router';


</script>

<style>
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

@media (min-width: 768px) {
  .container {
    padding: 0 var(--spacing-lg);
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 var(--spacing-xl);
  }
}
</style>