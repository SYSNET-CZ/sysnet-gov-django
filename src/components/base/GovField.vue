<script setup lang="ts">
interface Props {
  label?: string;
  error?: string;
  hint?: string;
  required?: boolean;
}
defineProps<Props>();
</script>

<template>
  <div class="flex flex-col gap-1.5 w-full">
    <div v-if="label" class="flex justify-between items-baseline">
      <label class="text-sm font-bold text-gov-text">
        {{ label }} <span v-if="required" class="text-gov-error font-bold" aria-hidden="true">*</span>
      </label>
      <slot name="extra" />
    </div>
    
    <div class="relative">
      <slot :error="error" />
    </div>
    
    <div class="flex justify-between">
      <p v-if="error" class="text-xs text-gov-error font-medium" role="alert">
        {{ error }}
      </p>
      <p v-else-if="hint" class="text-xs text-gray-400">
        {{ hint }}
      </p>
      <slot name="footer" />
    </div>
  </div>
</template>
