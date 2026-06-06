<template>
  <div v-if="modelValue" class="gov-modal" :class="`gov-modal--${size}`" tabindex="-1" role="dialog" aria-modal="true">
    <div class="gov-modal__dialog">
      <div class="gov-modal__content">
        <div class="gov-modal__header">
          <h5 class="gov-modal__title">{{ title }}</h5>
          <button type="button" class="gov-modal__close" @click="$emit('update:modelValue', false)" aria-label="Zavřít">
            &times;
          </button>
        </div>
        <div class="gov-modal__body">
          <slot name="content"></slot>
        </div>
        <div v-if="$slots.footer" class="gov-modal__footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
    <div class="gov-modal__backdrop" @click="$emit('update:modelValue', false)"></div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg'
}>()

defineEmits(['update:modelValue'])
</script>
