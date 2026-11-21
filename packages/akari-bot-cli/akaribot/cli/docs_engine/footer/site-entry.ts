import type { Theme } from "vitepress";

import DocsFooter from "./footer/DocsFooter.vue";
import AkariTheme from "./theme-entry";
import { provideAkariComponents } from "./composables/useAkariConfig";

/**
 * 站点主题入口：套用模板主题，仅在 ``Footer`` 插槽换成文档引擎提供的页脚。
 * 模板主题原样保留在 ``theme-entry.ts``，升级模板不会与页脚改动冲突。
 */
export default {
  ...AkariTheme,
  enhanceApp(context) {
    AkariTheme.enhanceApp?.(context);
    provideAkariComponents(context.app, { Footer: DocsFooter });
  },
} satisfies Theme;

export * from "./theme-entry";
