<script setup lang="ts">
import { computed } from 'vue';
import * as lucideIcons from 'lucide-vue-next';

interface Props {
  name: string;
  size?: number | string;
  color?: string;
  strokeWidth?: number;
}
const props = withDefaults(defineProps<Props>(), {
  size: 20,
  strokeWidth: 2
});

const iconComponent = computed(() => {
  // Převedení kebab-case nebo snake_case na PascalCase pro Lucide
  const pascalName = props.name
    .split(/[-_]/)
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join('');
  
  return (lucideIcons as any)[pascalName] || (lucideIcons as any)[props.name];
});
</script>

<template>
  <span class="inline-flex items-center justify-center shrink-0" aria-hidden="true">
    <component 
      :is="iconComponent" 
      v-if="iconComponent"
      :size="size" 
      :color="color" 
      :stroke-width="strokeWidth" 
    />
    <slot v-else>
      <!-- Fallback pro případ, že ikona neexistuje nebo chceme vlastní SVG -->
      <span class="text-[10px] border border-dashed p-0.5">?</span>
    </slot>
  </span>
</template>
