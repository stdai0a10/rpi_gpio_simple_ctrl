import { flushPromises, mount } from '@vue/test-utils';
import { nextTick } from 'vue';
import { createMemoryHistory, createRouter } from 'vue-router';
import { afterEach, describe, expect, it, vi } from 'vitest';

import App from '@/App.vue';
import { routes } from '@/router';

async function mountApplication(path: string) {
  const router = createRouter({
    history: createMemoryHistory(),
    routes
  });

  await router.push(path);
  await router.isReady();

  return {
    router,
    wrapper: mount(App, {
      attachTo: document.body,
      global: {
        plugins: [router]
      }
    })
  };
}

describe('application shell', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.replaceChildren();
    document.body.style.overflow = '';
  });

  it('offers only Home and Settings navigation around the minimal HOME content', async () => {
    const { wrapper } = await mountApplication('/');

    expect(
      wrapper
        .get('[aria-label="主要導覽"]')
        .findAll('a')
        .map((link) => link.text())
    ).toEqual(['首頁', '設定']);
    expect(wrapper.findAll('h1')).toHaveLength(1);
    expect(wrapper.get('h1').text()).toBe('RPI GPIO Simple Controller');

    wrapper.unmount();
  });

  it('keeps Service connection out of HOME without a health request', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);

    const { wrapper } = await mountApplication('/');

    expect(
      wrapper.find('[aria-labelledby="service-connection-heading"]').exists()
    ).toBe(false);
    expect(fetchMock).not.toHaveBeenCalled();

    wrapper.unmount();
  });

  it('closes the mobile Drawer through overlay, navigation, or Escape', async () => {
    const { router, wrapper } = await mountApplication('/');
    const menuButton = wrapper.get('button[aria-label="開啟導覽選單"]');

    await menuButton.trigger('click');

    expect(wrapper.find('[data-test="mobile-drawer"]').exists()).toBe(true);
    expect(document.body.style.overflow).toBe('hidden');

    await wrapper.get('[data-test="drawer-overlay"]').trigger('click');
    await nextTick();

    expect(wrapper.find('[data-test="mobile-drawer"]').exists()).toBe(false);
    expect(document.body.style.overflow).toBe('');

    await menuButton.trigger('click');
    await wrapper
      .get('[data-test="mobile-drawer"] a[href="/settings"]')
      .trigger('click');
    await flushPromises();

    expect(router.currentRoute.value.path).toBe('/settings');
    expect(wrapper.find('[data-test="mobile-drawer"]').exists()).toBe(false);

    await menuButton.trigger('click');
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    await nextTick();

    expect(wrapper.find('[data-test="mobile-drawer"]').exists()).toBe(false);
    expect(document.activeElement).toBe(menuButton.element);
    expect(document.body.style.overflow).toBe('');

    wrapper.unmount();
  });

  it('closes the mobile Drawer when the viewport reaches the desktop breakpoint', async () => {
    const { wrapper } = await mountApplication('/');
    const menuButton = wrapper.get('button[aria-label="開啟導覽選單"]');

    await menuButton.trigger('click');
    expect(wrapper.find('[data-test="mobile-drawer"]').exists()).toBe(true);

    Object.defineProperty(window, 'innerWidth', {
      configurable: true,
      value: 1024
    });
    window.dispatchEvent(new Event('resize'));
    await nextTick();

    expect(wrapper.find('[data-test="mobile-drawer"]').exists()).toBe(false);
    expect(document.body.style.overflow).toBe('');

    wrapper.unmount();
  });
});
