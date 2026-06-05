<script setup lang="ts">
const props = defineProps<{
  agency?: 'mzp' | 'mze' | 'dia' | 'gov';
  inverted?: boolean;
}>();

// Mapování barev dle JVS
const colors = {
  mzp: 'bg-[#007d32]', // Typická zelená MŽP
  mze: 'bg-[#005aab]', // Modrá MZe
  dia: 'bg-[#00469b]', // Primární modrá DIA
  gov: 'bg-[#0c1838]', // Tmavě modrá GOV
};
</script>

<template>
  <div class="flex items-center gap-3">
    <div 
      class="w-10 h-10 flex items-center justify-center text-white font-bold"
      :class="agency ? colors[agency] : colors.gov"
    >
      <span v-if="agency === 'mzp'">🌲</span>
      <span v-else-if="agency === 'mze'">🌾</span>
      <span v-else>🦁</span>
    </div>
    <div class="flex flex-col uppercase leading-none font-bold tracking-tight" :class="inverted ? 'text-white' : 'text-gov-text'">
      <template v-if="agency === 'mzp'">
        <span class="text-[10px]">Ministerstvo</span>
        <span class="text-[14px]">životního prostředí</span>
      </template>
      <template v-else-if="agency === 'mze'">
        <span class="text-[10px]">Ministerstvo</span>
        <span class="text-[14px]">zemědělství</span>
      </template>
      <template v-else>
        <span class="text-[10px]">Česká</span>
        <span class="text-[14px]">republika</span>
      </template>
    </div>
  </div>
</template>
