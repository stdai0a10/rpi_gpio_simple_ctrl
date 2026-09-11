import pluginVitest from '@vitest/eslint-plugin';
import { withVueTs, vueTsConfigs } from '@vue/eslint-config-typescript';
import skipFormatting from 'eslint-config-prettier/flat';
import { globalIgnores } from 'eslint/config';
import pluginVue from 'eslint-plugin-vue';

export default withVueTs(
  {
    rootDir: import.meta.dirname,
    scriptLangs: ['ts', 'js']
  },
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,cjs,vue,ts,mts,cts}']
  },
  globalIgnores(['**/dist/**', '**/coverage/**']),
  pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,
  {
    ...pluginVitest.configs.recommended,
    files: ['tests/**/*.spec.ts']
  },
  skipFormatting,
  {
    name: 'app/project-rules',
    rules: {
      'space-before-function-paren': [
        'error',
        {
          anonymous: 'always',
          named: 'never',
          asyncArrow: 'always'
        }
      ]
    }
  }
);
