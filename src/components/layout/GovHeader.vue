<script setup lang="ts">
defineProps<{
  title: string;
  version?: string;
}>();
</script>

<template>
  <header class="bg-white border-b-2 border-gov-blue-primary/10 px-8 py-4 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 bg-gov-blue-primary flex items-center justify-center text-white font-serif text-2xl">
        🦁
      </div>
      <div>
        <h1 class="text-xl font-bold leading-tight">{{ title }}</h1>
        <p v-if="version" class="text-xs text-gray-500">Verze {{ version }}</p>
      </div>
    </div>
    <nav class="flex gap-6 items-center">
      <slot name="nav" />
      <div class="h-8 w-[1px] bg-gray-200 mx-2"></div>
      <button class="text-gray-600">👤 Účet</button>
    </nav>
  </header>
</template>
