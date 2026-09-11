import { mount } from '@vue/test-utils';
import { createMemoryHistory, createRouter } from 'vue-router';
import { describe, expect, it } from 'vitest';

import App from '@/App.vue';
import { routes } from '@/router';

describe('home route', () => {
  it('renders the project name at the root path', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes
    });

    await router.push('/');
    await router.isReady();

    const wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    });

    expect(wrapper.get('h1').text()).toBe('RPI GPIO Simple Controller');
  });
});
