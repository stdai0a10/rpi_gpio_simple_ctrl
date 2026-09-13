import { flushPromises, mount } from '@vue/test-utils';
import { createMemoryHistory, createRouter } from 'vue-router';
import { afterEach, describe, expect, it, vi } from 'vitest';

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
    attachTo: document.body,
    global: {
      plugins: [router]
    }
  });
}

describe('Service connection', () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    document.body.replaceChildren();
  });

  it('shows checking then reachable only for the expected health response', async () => {
    let resolveFetch!: (response: Response) => void;
    const fetchMock = vi.fn(
      () =>
        new Promise<Response>((resolve) => {
          resolveFetch = resolve;
        })
    );
    vi.stubGlobal('fetch', fetchMock);

    const wrapper = await mountSettings();
    const connectionSection = wrapper.get(
      '[aria-labelledby="service-connection-heading"]'
    );

    expect(connectionSection.text()).toContain('檢查中');
    expect(fetchMock).toHaveBeenCalledWith(
      '/health',
      expect.objectContaining({
        cache: 'no-store',
        signal: expect.any(AbortSignal)
      })
    );

    resolveFetch({
      status: 200,
      json: async () => ({ status: 'ok' })
    } as Response);
    await flushPromises();

    expect(connectionSection.text()).toContain('服務可連線');
    expect(connectionSection.text()).not.toContain('重新檢查');

    wrapper.unmount();
  });

  it('labels a 403 response as access denied and offers a manual recheck', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 403 } as Response);
    vi.stubGlobal('fetch', fetchMock);

    const wrapper = await mountSettings();
    await flushPromises();

    const connectionSection = wrapper.get(
      '[aria-labelledby="service-connection-heading"]'
    );
    expect(connectionSection.text()).toContain('存取遭拒');
    expect(connectionSection.get('button').text()).toBe('重新檢查');
    expect(fetchMock).toHaveBeenCalledTimes(1);

    wrapper.unmount();
  });

  it('treats a malformed liveness payload as unavailable until the user retries', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        status: 200,
        json: async () => ({ status: 'not-ok' })
      } as Response)
      .mockResolvedValueOnce({
        status: 200,
        json: async () => ({ status: 'ok' })
      } as Response);
    vi.stubGlobal('fetch', fetchMock);

    const wrapper = await mountSettings();
    await flushPromises();

    const connectionSection = wrapper.get(
      '[aria-labelledby="service-connection-heading"]'
    );
    expect(connectionSection.text()).toContain('服務無法連線');
    expect(fetchMock).toHaveBeenCalledTimes(1);

    await connectionSection.get('button').trigger('click');
    await flushPromises();

    expect(connectionSection.text()).toContain('服務可連線');
    expect(fetchMock).toHaveBeenCalledTimes(2);

    wrapper.unmount();
  });

  it('labels a transport failure as unavailable without issuing a second request', async () => {
    const fetchMock = vi
      .fn()
      .mockRejectedValue(new TypeError('Network request failed'));
    vi.stubGlobal('fetch', fetchMock);

    const wrapper = await mountSettings();
    await flushPromises();

    const connectionSection = wrapper.get(
      '[aria-labelledby="service-connection-heading"]'
    );
    expect(connectionSection.text()).toContain('服務無法連線');
    expect(connectionSection.get('button').text()).toBe('重新檢查');
    expect(fetchMock).toHaveBeenCalledTimes(1);

    wrapper.unmount();
  });

  it('marks a timed-out check unavailable without retrying automatically', async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn(
      (_input: RequestInfo | URL, init?: RequestInit) =>
        new Promise<Response>((_resolve, reject) => {
          init?.signal?.addEventListener('abort', () => {
            reject(new DOMException('The request timed out.', 'AbortError'));
          });
        })
    );
    vi.stubGlobal('fetch', fetchMock);

    const wrapper = await mountSettings();

    await vi.advanceTimersByTimeAsync(5_000);
    await flushPromises();

    const connectionSection = wrapper.get(
      '[aria-labelledby="service-connection-heading"]'
    );
    expect(connectionSection.text()).toContain('服務無法連線');
    expect(connectionSection.get('button').text()).toBe('重新檢查');
    expect(fetchMock).toHaveBeenCalledTimes(1);

    await vi.advanceTimersByTimeAsync(60_000);

    expect(fetchMock).toHaveBeenCalledTimes(1);

    wrapper.unmount();
  });
});
