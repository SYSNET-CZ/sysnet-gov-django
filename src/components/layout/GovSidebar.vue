<script setup lang="ts">
interface NavItem {
  label: string;
  href: string;
  active?: boolean;
  icon?: any;
}
defineProps<{ items: NavItem[] }>();
</script>

<template>
  <aside class="w-64 bg-gov-bg-gray border-r-2 border-gov-border h-full flex flex-col">
    <nav class="flex-1 p-4 flex flex-col gap-1">
      <a
        v-for="item in items"
        :key="item.label"
        :href="item.href"
        class="flex items-center gap-3 px-4 py-3 font-medium transition-colors border-l-4"
        :class="item.active 
          ? 'bg-white border-gov-blue-primary text-gov-blue-primary shadow-sm' 
          : 'border-transparent text-gray-600 hover:bg-gray-100'
        "
      >
        <component v-if="item.icon" :is="item.icon" class="w-5 h-5" />
        {{ item.label }}
      </a>
    </nav>
    <div class="p-4 border-t border-gray-200 text-xs text-gray-400">
      SYSNET Gov UI Framework v0.1.0
    </div>
  </aside>
</template>
