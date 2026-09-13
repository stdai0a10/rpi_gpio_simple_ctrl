<script setup lang="ts">
import { Monitor, Moon, Sun } from 'lucide-vue-next';

import ServiceConnectionStatus from '@/components/ServiceConnectionStatus.vue';
import { useTheme } from '@/composables/theme';

const { setThemeMode, themeMode } = useTheme();
</script>

<template>
  <main class="settings-page">
    <h1>設定</h1>

    <section class="settings-section" aria-labelledby="appearance-heading">
      <h2 id="appearance-heading">外觀</h2>

      <fieldset class="theme-fieldset">
        <legend>主題</legend>
        <div class="theme-options" role="radiogroup" aria-label="主題">
          <label
            class="theme-option"
            :class="{ 'theme-option--selected': themeMode === 'system' }"
          >
            <input
              :checked="themeMode === 'system'"
              type="radio"
              name="theme"
              value="system"
              @change="setThemeMode('system')"
            />
            <Monitor aria-hidden="true" :size="20" />
            <span>跟隨系統</span>
          </label>
          <label
            class="theme-option"
            :class="{ 'theme-option--selected': themeMode === 'light' }"
          >
            <input
              :checked="themeMode === 'light'"
              type="radio"
              name="theme"
              value="light"
              @change="setThemeMode('light')"
            />
            <Sun aria-hidden="true" :size="20" />
            <span>淺色</span>
          </label>
          <label
            class="theme-option"
            :class="{ 'theme-option--selected': themeMode === 'dark' }"
          >
            <input
              :checked="themeMode === 'dark'"
              type="radio"
              name="theme"
              value="dark"
              @change="setThemeMode('dark')"
            />
            <Moon aria-hidden="true" :size="20" />
            <span>深色</span>
          </label>
        </div>
      </fieldset>
    </section>

    <ServiceConnectionStatus />
  </main>
</template>

<style scoped>
.settings-page {
  width: min(100%, 720px);
  margin: 0 auto;
  padding: 24px 16px 48px;
}

h1 {
  margin: 0;
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 600;
  line-height: 1.3;
}

.settings-section {
  margin-top: 32px;
  padding: 20px 0;
  border-top: 1px solid var(--border-default);
  border-bottom: 1px solid var(--border-default);
}

h2,
legend {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
}

.theme-fieldset {
  min-width: 0;
  margin: 20px 0 0;
  padding: 0;
  border: 0;
}

legend {
  padding: 0;
  font-size: 14px;
}

.theme-options {
  display: grid;
  gap: 8px;
  margin-top: 12px;
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 48px;
  padding: 8px 12px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-control);
  background: var(--bg-surface);
  color: var(--text-secondary);
  cursor: pointer;
}

.theme-option:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.theme-option--selected,
.theme-option--selected:hover {
  border-color: var(--selected-option-border);
  background: var(--selected-option-background);
  color: var(--selected-option-foreground);
}

.theme-option input {
  width: 18px;
  height: 18px;
  margin: 0;
  accent-color: var(--color-primary);
}

@media (min-width: 1024px) {
  .settings-page {
    padding: 32px;
  }

  h1 {
    font-size: 24px;
  }
}
</style>
