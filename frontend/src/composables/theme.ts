import {
  computed,
  inject,
  onBeforeUnmount,
  onMounted,
  provide,
  ref,
  type InjectionKey,
  type Ref
} from 'vue';

export type ThemeMode = 'system' | 'light' | 'dark';
type ResolvedTheme = Exclude<ThemeMode, 'system'>;

interface ThemeContext {
  themeMode: Ref<ThemeMode>;
  setThemeMode: (themeMode: ThemeMode) => void;
}

const THEME_STORAGE_KEY = 'rpi-gpio-simple-ctrl.theme';
const SYSTEM_DARK_THEME_QUERY = '(prefers-color-scheme: dark)';
const themeContextKey: InjectionKey<ThemeContext> = Symbol('theme-context');

function isThemeMode(value: string | null): value is ThemeMode {
  return value === 'system' || value === 'light' || value === 'dark';
}

function readStoredThemeMode(): ThemeMode {
  try {
    const storedThemeMode = window.localStorage.getItem(THEME_STORAGE_KEY);

    return isThemeMode(storedThemeMode) ? storedThemeMode : 'system';
  } catch {
    return 'system';
  }
}

function updateDocumentTheme(theme: ResolvedTheme): void {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
}

export function provideTheme(): ThemeContext {
  const themeMode = ref<ThemeMode>(readStoredThemeMode());
  const systemPrefersDark = ref(false);
  let mediaQuery: MediaQueryList | undefined;

  const resolvedTheme = computed<ResolvedTheme>(() => {
    if (themeMode.value === 'system') {
      return systemPrefersDark.value ? 'dark' : 'light';
    }

    return themeMode.value;
  });

  function applyTheme(): void {
    updateDocumentTheme(resolvedTheme.value);
  }

  function handleSystemThemeChange(event: MediaQueryListEvent): void {
    systemPrefersDark.value = event.matches;

    if (themeMode.value === 'system') {
      applyTheme();
    }
  }

  function setThemeMode(nextThemeMode: ThemeMode): void {
    themeMode.value = nextThemeMode;

    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, nextThemeMode);
    } catch {
      // A blocked browser storage boundary must not prevent a usable theme choice.
    }

    applyTheme();
  }

  onMounted(() => {
    if (typeof window.matchMedia === 'function') {
      mediaQuery = window.matchMedia(SYSTEM_DARK_THEME_QUERY);
      systemPrefersDark.value = mediaQuery.matches;

      if (typeof mediaQuery.addEventListener === 'function') {
        mediaQuery.addEventListener('change', handleSystemThemeChange);
      } else {
        mediaQuery.addListener(handleSystemThemeChange);
      }
    }

    applyTheme();
  });

  onBeforeUnmount(() => {
    if (mediaQuery === undefined) {
      return;
    }

    if (typeof mediaQuery.removeEventListener === 'function') {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    } else {
      mediaQuery.removeListener(handleSystemThemeChange);
    }
  });

  const context = {
    themeMode,
    setThemeMode
  };

  provide(themeContextKey, context);

  return context;
}

export function useTheme(): ThemeContext {
  const themeContext = inject(themeContextKey);

  if (themeContext === undefined) {
    throw new Error('Theme context is not available.');
  }

  return themeContext;
}
