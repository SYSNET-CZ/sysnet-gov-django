<script setup lang="ts">
defineProps<{ title?: string }>();
</script>

<template>
  <div class="bg-white border-2 border-gov-border shadow-sm overflow-hidden">
    <div v-if="title || $slots.header" class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
      <slot name="header">
        <h3 class="font-bold text-lg text-gov-text">{{ title }}</h3>
      </slot>
    </div>
    <div class="p-6">
      <slot />
    </div>
    <div v-if="$slots.footer" class="px-6 py-3 bg-gray-50/30 border-t border-gray-100">
      <slot name="footer" />
    </div>
  </div>
</template>
