<template>
  <div class="gov-layout-master">
    <GovHeader :title="pageTitle" :user="user" />
    
    <div class="gov-layout-grid">
      <aside v-if="sidebarItems" class="gov-layout-grid__sidebar">
        <GovSidebar :items="sidebarItems" />
      </aside>
      
      <main class="gov-layout-grid__main">
        <GovBreadcrumbs v-if="breadcrumbs" :items="breadcrumbs" />
        
        <header class="gov-layout-grid__page-header">
          <slot name="page_header">
            <h1 class="gov-title">{{ pageTitle }}</h1>
          </slot>
        </header>

        <div class="gov-layout-grid__body">
          <slot name="content"></slot>
        </div>
      </main>
    </div>

    <footer class="gov-footer">
        <div class="gov-container">
            <slot name="footer">&copy; {{ new Date().getFullYear() }} SYSNET s.r.o.</slot>
        </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import GovHeader from './GovHeader.vue'
import GovSidebar from './GovSidebar.vue'
import GovBreadcrumbs from '../base/GovBreadcrumbs.vue'

defineProps<{
  pageTitle: string
  user?: any
  sidebarItems?: any[]
  breadcrumbs?: any[]
}>()
</script>
