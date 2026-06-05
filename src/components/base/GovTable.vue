<script setup lang="ts">
interface Column {
  key: string;
  label: string;
  class?: string;
}
defineProps<{
  columns: Column[];
  items: any[];
  loading?: boolean;
}>();
</script>

<template>
  <div class="overflow-x-auto border-2 border-gov-border">
    <table class="w-full text-left border-collapse">
      <thead>
        <tr class="bg-gov-bg-gray border-b-2 border-gov-border">
          <th 
            v-for="col in columns" 
            :key="col.key"
            class="px-4 py-3 font-bold text-sm uppercase tracking-wider text-gov-blue-dark"
            :class="col.class"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200">
        <tr v-if="loading">
          <td :colspan="columns.length" class="px-4 py-8 text-center text-gray-500 italic">
            Načítám data...
          </td>
        </tr>
        <tr v-else-if="items.length === 0">
          <td :colspan="columns.length" class="px-4 py-8 text-center text-gray-500">
            Žádné záznamy nebyly nalezeny.
          </td>
        </tr>
        <tr 
          v-for="(item, idx) in items" 
          :key="idx"
          class="hover:bg-blue-50/30 transition-colors"
        >
          <td 
            v-for="col in columns" 
            :key="col.key"
            class="px-4 py-3 text-sm"
            :class="col.class"
          >
            <slot :name="`cell(${col.key})`" :item="item">
              {{ item[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
