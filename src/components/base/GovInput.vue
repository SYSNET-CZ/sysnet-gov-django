<script setup lang="ts">
interface Props {
  label?: string;
  modelValue: string | number;
  type?: string;
  placeholder?: string;
  error?: string;
  hint?: string;
  required?: boolean;
}
defineProps<Props>();
defineEmits(['update:modelValue']);
</script>

<template>
  <div class="flex flex-col gap-1.5 w-full">
    <label v-if="label" class="text-sm font-bold text-gov-text">
      {{ label }} <span v-if="required" class="text-gov-error">*</span>
    </label>
    <input
      :type="type || 'text'"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :placeholder="placeholder"
      class="px-3 py-2 border-2 border-gov-border focus:border-gov-blue-primary focus:outline-none transition-colors"
      :class="{ 'border-gov-error': error }"
    />
    <p v-if="error" class="text-xs text-gov-error font-medium">{{ error }}</p>
    <p v-else-if="hint" class="text-xs text-gray-500">{{ hint }}</p>
  </div>
</template>
