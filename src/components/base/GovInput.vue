<script setup lang="ts">
import { useId } from 'vue';

interface Props {
  label?: string;
  modelValue: string | number;
  type?: string;
  placeholder?: string;
  error?: string;
  hint?: string;
  required?: boolean;
}
const props = defineProps<Props>();
defineEmits(['update:modelValue']);

const inputId = useId();
const hintId = useId();
const errorId = useId();
</script>

<template>
  <div class="flex flex-col gap-1.5 w-full">
    <label :for="inputId" v-if="label" class="text-sm font-bold text-gov-text">
      {{ label }} <span v-if="required" class="text-gov-error" aria-hidden="true">*</span>
    </label>
    
    <input
      :id="inputId"
      :type="type || 'text'"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :placeholder="placeholder"
      :required="required"
      :aria-invalid="!!error"
      :aria-describedby="`${error ? errorId : ''} ${hint ? hintId : ''}`.trim()"
      class="px-3 py-2 border-2 border-gov-border focus:border-gov-blue-primary focus:ring-4 focus:ring-gov-blue-light focus:outline-none transition-all"
      :class="{ 'border-gov-error': error }"
    />
    
    <p v-if="error" :id="errorId" class="text-xs text-gov-error font-medium" role="alert">
      {{ error }}
    </p>
    <p v-else-if="hint" :id="hintId" class="text-xs text-gray-500">
      {{ hint }}
    </p>
  </div>
</template>
