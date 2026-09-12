// @vitest-environment node

import { describe, expect, it } from 'vitest';

import viteConfig from '../vite.config';

function matchesProxyContext(context: string, path: string): boolean {
  if (context.startsWith('^')) {
    return new RegExp(context).test(path);
  }

  return path.startsWith(context);
}

describe('Vite development server', () => {
  it('binds to loopback and proxies only backend paths', () => {
    expect(viteConfig.server?.host).toBe('127.0.0.1');

    expect(viteConfig.server?.proxy).toEqual({
      '^/health(?:\\?|$)': { target: 'http://127.0.0.1:8000' },
      '^/api(?:/|\\?|$)': { target: 'http://127.0.0.1:8000' }
    });
  });

  it('does not proxy paths outside the health or API endpoints', () => {
    const contexts = Object.keys(viteConfig.server?.proxy ?? {});
    const isProxied = (path: string) =>
      contexts.some((context) => matchesProxyContext(context, path));

    expect(isProxied('/health')).toBe(true);
    expect(isProxied('/health?refresh=true')).toBe(true);
    expect(isProxied('/api')).toBe(true);
    expect(isProxied('/api?limit=10')).toBe(true);
    expect(isProxied('/api/functions/open-door')).toBe(true);
    expect(isProxied('/healthcheck')).toBe(false);
    expect(isProxied('/apiary')).toBe(false);
  });
});
