import { mount } from '@vue/test-utils';
import { nextTick } from 'vue';
import { createMemoryHistory, createRouter } from 'vue-router';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import App from '@/App.vue';
import { routes } from '@/router';

async function mountSettings() {
  const router = createRouter({
    history: createMemoryHistory(),
    routes
  });

  await router.push('/settings');
  await router.isReady();

  return mount(App, {
    global: {
      plugins: [router]
    }
  });
}

function installMatchMedia(matches: boolean) {
  let changeListener: ((event: MediaQueryListEvent) => void) | undefined;
  const mediaQuery = {
    matches,
    media: '(prefers-color-scheme: dark)',
    onchange: null,
    addEventListener: vi.fn(
      (_event: string, listener: (event: MediaQueryListEvent) => void) => {
        changeListener = listener;
      }
    ),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn()
  } as unknown as MediaQueryList;

  vi.stubGlobal(
    'matchMedia',
    vi.fn(() => mediaQuery)
  );

  return {
    emitChange(nextMatches: boolean) {
      (mediaQuery as unknown as { matches: boolean }).matches = nextMatches;
      changeListener?.({ matches: nextMatches } as MediaQueryListEvent);
    }
  };
}

describe('SETTINGS Appearance', () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.documentElement.removeAttribute('data-theme');
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('offers an accessible System, Light, and Dark theme choice', async () => {
    const wrapper = await mountSettings();

    expect(wrapper.get('h1').text()).toBe('設定');

    const themeGroup = wrapper.get('[role="radiogroup"][aria-label="主題"]');
    expect(
      themeGroup
        .findAll('input[type="radio"]')
        .map((input) => input.attributes('value'))
    ).toEqual(['system', 'light', 'dark']);
    expect(themeGroup.text()).toContain('跟隨系統');
    expect(themeGroup.text()).toContain('淺色');
    expect(themeGroup.text()).toContain('深色');
  });

  it('uses System by default and persists an explicit Light preference', async () => {
    installMatchMedia(true);

    const wrapper = await mountSettings();

    expect(
      (wrapper.get('input[value="system"]').element as HTMLInputElement).checked
    ).toBe(true);
    expect(document.documentElement.dataset.theme).toBe('dark');

    await wrapper.get('input[value="light"]').setValue();

    expect(
      (wrapper.get('input[value="light"]').element as HTMLInputElement).checked
    ).toBe(true);
    expect(document.documentElement.dataset.theme).toBe('light');
    expect(window.localStorage.getItem('rpi-gpio-simple-ctrl.theme')).toBe(
      'light'
    );

    wrapper.unmount();

    const remountedWrapper = await mountSettings();

    expect(
      (remountedWrapper.get('input[value="light"]').element as HTMLInputElement)
        .checked
    ).toBe(true);
    expect(document.documentElement.dataset.theme).toBe('light');
  });

  it('falls back to System when browser storage contains an invalid theme', async () => {
    installMatchMedia(true);
    window.localStorage.setItem('rpi-gpio-simple-ctrl.theme', 'sepia');

    const wrapper = await mountSettings();

    expect(
      (wrapper.get('input[value="system"]').element as HTMLInputElement).checked
    ).toBe(true);
    expect(document.documentElement.dataset.theme).toBe('dark');
  });

  it('follows system theme changes only while System is selected', async () => {
    const matchMedia = installMatchMedia(false);
    const wrapper = await mountSettings();

    expect(document.documentElement.dataset.theme).toBe('light');

    matchMedia.emitChange(true);
    await nextTick();

    expect(document.documentElement.dataset.theme).toBe('dark');

    await wrapper.get('input[value="dark"]').setValue();
    matchMedia.emitChange(false);
    await nextTick();

    expect(document.documentElement.dataset.theme).toBe('dark');
  });
});
