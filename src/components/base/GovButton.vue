<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  type?: 'button' | 'submit';
  disabled?: boolean;
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  type: 'button',
  disabled: false,
});
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center px-6 py-2 border-2 font-bold transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
    :class="{
      'bg-gov-blue-primary border-gov-blue-primary text-white hover:bg-gov-blue-hover': variant === 'primary',
      'bg-white border-gov-blue-primary text-gov-blue-primary hover:bg-gov-blue-primary hover:text-white': variant === 'secondary',
      'bg-gov-error border-gov-error text-white hover:opacity-90': variant === 'danger',
      'bg-transparent border-transparent text-gov-blue-primary hover:underline px-2': variant === 'ghost',
    }"
  >
    <slot />
  </button>
</template>
