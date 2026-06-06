<template>
  <GovMasterLayout 
    page-title="Styleguide | Gov UI"
    :sidebar-items="demoSidebar"
    :breadcrumbs="demoBreadcrumbs"
  >
    <template #content>
        <section class="gov-section">
            <GovCard title="Tlačítka">
                <template #content>
                    <div class="gov-button-group">
                        <GovButton text="Primární" type="primary" />
                        <GovButton text="Sekundární" type="secondary" />
                        <GovButton text="Danger" type="danger" />
                    </div>
                </template>
            </GovCard>

            <GovCard title="Data">
                <template #content>
                    <GovTable :headers="['ID', 'Název']" :rows="[['1', 'Test'], ['2', 'Demo']]" />
                </template>
            </GovCard>

            <GovButton text="Otevřít Modál" @click="showModal = true" />
        </section>

        <GovModal v-model="showModal" title="Ukázka modálu">
            <template #content>
                Toto je Vue verze GDS modálu.
            </template>
            <template #footer>
                <GovButton text="Zavřít" @click="showModal = false" />
            </template>
        </GovModal>
    </template>
  </GovMasterLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import GovMasterLayout from './components/layout/GovMasterLayout.vue'
import GovCard from './components/base/GovCard.vue'
import GovButton from './components/base/GovButton.vue'
import GovTable from './components/base/GovTable.vue'
import GovModal from './components/base/GovModal.vue'

const showModal = ref(false)
const demoSidebar = [
    { label: 'Domů', url: '#', active: true },
    { label: 'Uživatelé', url: '#' }
]
const demoBreadcrumbs = [
    { label: 'Domu', url: '/' },
    { label: 'Komponenty', url: '#' }
]
</script>
