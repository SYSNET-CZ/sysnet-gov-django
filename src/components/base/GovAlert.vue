<script setup lang="ts">
interface Props {
  variant?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
}
withDefaults(defineProps<Props>(), {
  variant: 'info'
});
</script>

<template>
  <div 
    class="p-4 border-l-8 flex gap-4"
    :class="{
      'bg-blue-50 border-gov-blue-primary text-gov-blue-dark': variant === 'info',
      'bg-green-50 border-gov-success text-green-900': variant === 'success',
      'bg-yellow-50 border-gov-warning text-yellow-900': variant === 'warning',
      'bg-red-50 border-gov-error text-red-900': variant === 'error',
    }"
  >
    <div class="flex-1">
      <h4 v-if="title" class="font-bold mb-1">{{ title }}</h4>
      <div class="text-sm">
        <slot />
      </div>
    </div>
  </div>
</template>
