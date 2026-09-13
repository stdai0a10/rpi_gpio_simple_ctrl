<script setup lang="ts">
import { House, Menu, Settings, X } from 'lucide-vue-next';
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router';

import { provideTheme } from '@/composables/theme';

provideTheme();

const route = useRoute();
const isDrawerOpen = ref(false);
const menuButton = ref<HTMLButtonElement | null>(null);
let previousBodyOverflow = '';

const pageTitle = computed(() =>
  typeof route.meta.title === 'string'
    ? route.meta.title
    : 'RPI GPIO Simple Controller'
);

function openDrawer(): void {
  previousBodyOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  isDrawerOpen.value = true;
}

function closeDrawer(): void {
  closeDrawerWithFocus(true);
}

function closeDrawerWithFocus(returnFocus: boolean): void {
  if (!isDrawerOpen.value) {
    return;
  }

  isDrawerOpen.value = false;
  document.body.style.overflow = previousBodyOverflow;

  if (returnFocus) {
    void nextTick(() => {
      menuButton.value?.focus();
    });
  }
}

function handleKeydown(event: KeyboardEvent): void {
  if (event.key === 'Escape') {
    closeDrawer();
  }
}

function closeDrawerAtDesktopBreakpoint(): void {
  if (window.innerWidth >= 1024) {
    closeDrawerWithFocus(false);
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
  window.addEventListener('resize', closeDrawerAtDesktopBreakpoint);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);
  window.removeEventListener('resize', closeDrawerAtDesktopBreakpoint);

  if (isDrawerOpen.value) {
    document.body.style.overflow = previousBodyOverflow;
  }
});
</script>

<template>
  <div class="app-shell">
    <aside class="desktop-sidebar">
      <p class="sidebar-product-name">RPI GPIO Simple Controller</p>
      <nav class="primary-navigation" aria-label="主要導覽">
        <RouterLink to="/">
          <House class="navigation-icon" aria-hidden="true" :size="20" />
          <span>首頁</span>
        </RouterLink>
        <RouterLink to="/settings">
          <Settings class="navigation-icon" aria-hidden="true" :size="20" />
          <span>設定</span>
        </RouterLink>
      </nav>
    </aside>

    <div class="app-content">
      <header class="top-bar">
        <button
          ref="menuButton"
          class="menu-button"
          type="button"
          aria-label="開啟導覽選單"
          aria-controls="mobile-drawer"
          :aria-expanded="isDrawerOpen"
          @click="openDrawer"
        >
          <Menu aria-hidden="true" :size="24" />
        </button>
        <span class="top-bar-title">{{ pageTitle }}</span>
      </header>

      <RouterView />
    </div>

    <template v-if="isDrawerOpen">
      <button
        class="drawer-overlay"
        data-test="drawer-overlay"
        type="button"
        aria-label="關閉導覽選單"
        @click="closeDrawer"
      />
      <aside
        id="mobile-drawer"
        class="mobile-drawer"
        data-test="mobile-drawer"
        role="dialog"
        aria-modal="true"
        aria-label="導覽選單"
      >
        <div class="drawer-header">
          <span>RPI GPIO Simple Controller</span>
          <button
            class="close-drawer-button"
            type="button"
            aria-label="關閉導覽選單"
            @click="closeDrawer"
          >
            <X aria-hidden="true" :size="24" />
          </button>
        </div>
        <nav class="primary-navigation" aria-label="行動導覽">
          <RouterLink to="/" @click="closeDrawer">
            <House class="navigation-icon" aria-hidden="true" :size="20" />
            <span>首頁</span>
          </RouterLink>
          <RouterLink to="/settings" @click="closeDrawer">
            <Settings class="navigation-icon" aria-hidden="true" :size="20" />
            <span>設定</span>
          </RouterLink>
        </nav>
      </aside>
    </template>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100dvh;
  background: var(--bg-page);
}

.desktop-sidebar {
  display: none;
}

.app-content {
  min-height: 100dvh;
}

.top-bar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: var(--top-bar-height);
  padding: 0 16px;
  border-bottom: 1px solid var(--border-default);
  background: var(--bg-surface);
}

.top-bar-title {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.menu-button,
.close-drawer-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 44px;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 0;
  border-radius: var(--radius-control);
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
}

.menu-button:hover,
.close-drawer-button:hover {
  background: var(--bg-hover);
}

.drawer-overlay {
  position: fixed;
  z-index: 30;
  inset: 0;
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  background: var(--overlay);
  cursor: pointer;
}

.mobile-drawer {
  position: fixed;
  z-index: 40;
  inset: 0 auto 0 0;
  display: flex;
  flex-direction: column;
  width: min(320px, calc(100vw - 48px));
  min-height: 100dvh;
  padding: 16px 12px;
  border-right: 1px solid var(--border-default);
  background: var(--bg-surface);
  box-shadow: var(--shadow-drawer);
  animation: drawer-enter 180ms ease-out;
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-height: 48px;
  padding: 0 4px 16px;
  border-bottom: 1px solid var(--border-default);
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 600;
}

.primary-navigation {
  display: grid;
  gap: 4px;
  padding-top: 16px;
}

.primary-navigation a {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 48px;
  padding: 0 12px;
  border-radius: var(--radius-control);
  color: var(--text-secondary);
  font-weight: 600;
  text-decoration: none;
}

.primary-navigation a:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.primary-navigation a.router-link-active {
  background: var(--nav-active-background);
  color: var(--nav-active-text);
}

.primary-navigation a.router-link-active .navigation-icon {
  color: var(--nav-active-icon);
}

@keyframes drawer-enter {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translateX(0);
  }
}

@media (min-width: 1024px) {
  .drawer-overlay,
  .mobile-drawer {
    display: none;
  }

  .desktop-sidebar {
    position: fixed;
    z-index: 20;
    inset: 0 auto 0 0;
    display: flex;
    flex-direction: column;
    width: var(--sidebar-width);
    min-height: 100dvh;
    padding: 24px 12px;
    border-right: 1px solid var(--border-default);
    background: var(--bg-surface);
  }

  .sidebar-product-name {
    margin: 0;
    padding: 0 12px 20px;
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 700;
    line-height: 1.4;
  }

  .app-content {
    margin-left: var(--sidebar-width);
  }

  .menu-button {
    display: none;
  }

  .top-bar {
    padding: 0 32px;
  }

  .top-bar-title {
    font-size: 18px;
  }
}
</style>
