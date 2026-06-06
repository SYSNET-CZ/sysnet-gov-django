<template>
  <nav class="gov-breadcrumbs" aria-label="Drobečková navigace">
    <ol class="gov-breadcrumbs__list">
      <li v-for="(item, index) in items" :key="index" class="gov-breadcrumbs__item">
        <span v-if="index === items.length - 1" class="gov-breadcrumbs__link gov-breadcrumbs__link--current" aria-current="page">
          {{ item.label }}
        </span>
        <a v-else :href="item.url" class="gov-breadcrumbs__link">
          {{ item.label }}
        </a>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  items: Array<{ label: string; url?: string }>
}>()
</script>
