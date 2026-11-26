<script setup lang="ts">
import { computed } from "vue";
import { useData, withBase } from "vitepress";

import FooterIcon from "./FooterIcon.vue";

interface FooterAction {
  text?: string;
  link?: string;
  icon?: string;
}

interface FooterAbout {
  title?: string;
  text?: unknown;
  image?: string;
  imageAlt?: string;
  actions?: unknown;
}

interface FooterConfig {
  message?: string;
  copyright?: string;
  about?: FooterAbout;
}

const EXTERNAL_PATTERN = /^(?:[a-z][a-z\d+.-]*:|\/\/)/i;

const { site, theme } = useData();

/**
 * 主题按 ``themeConfig.akari`` 读站点配置，页脚只取其中的页脚与顶栏两段。其余字段由主题自己处理。
 */
const akari = computed<Record<string, unknown>>(() => {
  const value = (theme.value as { akari?: unknown }).akari;
  return value && typeof value === "object" ? (value as Record<string, unknown>) : {};
});

const footer = computed<FooterConfig>(() => {
  const value = akari.value.footer;
  return value && typeof value === "object" ? (value as FooterConfig) : {};
});

const about = computed<FooterAbout | null>(() => {
  const value = footer.value.about;
  return value && typeof value === "object" ? value : null;
});

const title = computed(() => (about.value?.title ?? "").trim());

const lines = computed<string[]>(() => {
  const value = about.value?.text;
  if (typeof value === "string") return value.trim() ? [value] : [];
  if (!Array.isArray(value)) return [];
  return value.filter((line): line is string => typeof line === "string" && !!line.trim());
});

const actions = computed<FooterAction[]>(() => {
  const value = about.value?.actions;
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is FooterAction => {
    if (!item || typeof item !== "object") return false;
    const link = (item as FooterAction).link;
    return typeof link === "string" && !!link.trim();
  });
});

const image = computed(() => assetUrl(about.value?.image));

const imageAlt = computed(() => (about.value?.imageAlt ?? "").trim() || title.value);

const hasAbout = computed(() => !!title.value || lines.value.length > 0 || actions.value.length > 0 || !!image.value);

const logo = computed(() => {
  const appBar = akari.value.appBar;
  const value = appBar && typeof appBar === "object" ? (appBar as { logo?: string }).logo : undefined;
  return assetUrl(value);
});

const brandTitle = computed(() => {
  const appBar = akari.value.appBar;
  const value = appBar && typeof appBar === "object" ? (appBar as { title?: string }).title : undefined;
  return (value ?? "").trim() || site.value.title;
});

const message = computed(() => (footer.value.message ?? "").trim());

const copyright = computed(() => (footer.value.copyright ?? "").trim());

const hasBottom = computed(() => !!copyright.value || (hasAbout.value && !!message.value));

function assetUrl(value: string | undefined): string {
  const path = (value ?? "").trim();
  if (!path) return "";
  if (EXTERNAL_PATTERN.test(path)) return path;
  return withBase(path.startsWith("/") ? path : `/${path}`);
}

function isExternal(link: string): boolean {
  return EXTERNAL_PATTERN.test(link);
}
</script>

<template>
  <div class="akari-docs-footer">
    <div class="akari-docs-footer__divider" role="separator"></div>
    <footer class="akari-docs-footer__surface">
      <div class="akari-surface-cap" aria-hidden="true"></div>
      <div class="akari-docs-footer__inner">
        <section v-if="hasAbout" class="akari-docs-footer__band">
          <figure v-if="image" class="akari-docs-footer__art">
            <img class="akari-docs-footer__art-image" :src="image" :alt="imageAlt" loading="lazy" decoding="async" />
          </figure>
          <div class="akari-docs-footer__body">
            <h2 v-if="title" class="akari-docs-footer__heading">{{ title }}</h2>
            <p v-for="(line, index) in lines" :key="index" class="akari-docs-footer__copy">{{ line }}</p>
            <ul v-if="actions.length" class="akari-docs-footer__actions">
              <li v-for="action in actions" :key="action.link">
                <a
                  class="akari-docs-footer__action"
                  :href="assetUrl(action.link)"
                  :title="action.text"
                  :target="isExternal(action.link ?? '') ? '_blank' : undefined"
                  :rel="isExternal(action.link ?? '') ? 'noreferrer' : undefined"
                >
                  <FooterIcon :icon="action.icon" />
                  <span class="akari-docs-footer__action-text">{{ action.text }}</span>
                </a>
              </li>
            </ul>
          </div>
        </section>

        <section v-else class="akari-docs-footer__brand-block">
          <p class="akari-docs-footer__brand">
            <img v-if="logo" class="akari-docs-footer__logo" :src="logo" alt="" loading="lazy" decoding="async" />
            <span class="akari-docs-footer__title">{{ brandTitle }}</span>
          </p>
          <p v-if="message" class="akari-docs-footer__message">{{ message }}</p>
        </section>

        <div v-if="hasBottom" class="akari-docs-footer__bottom" :class="{ 'akari-docs-footer__bottom--about': hasAbout }">
          <p v-if="hasAbout && message" class="akari-docs-footer__message">{{ message }}</p>
          <p v-if="copyright" class="akari-docs-footer__copyright">{{ copyright }}</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* 波浪分隔线画在页面背景上，页脚本身是顶端圆角、向页面底部展开的独立表面。 */
.akari-docs-footer {
  display: flex;
  flex: none;
  flex-direction: column;
}

.akari-docs-footer__divider {
  flex: none;
  height: 8px;
  margin-block: 24px;
  margin-inline: 64px;
  background-color: var(--akari-wavy-divider-color, var(--md-sys-color-outline-variant));
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='8'%3E%3Cpath d='M0 4c5.333 4.667 10.667 4.667 16 0s10.667-4.667 16 0' fill='none' stroke='black' stroke-width='1.5'/%3E%3C/svg%3E")
    left center / 32px 8px repeat-x;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='8'%3E%3Cpath d='M0 4c5.333 4.667 10.667 4.667 16 0s10.667-4.667 16 0' fill='none' stroke='black' stroke-width='1.5'/%3E%3C/svg%3E")
    left center / 32px 8px repeat-x;
}

@media (forced-colors: active) {
  .akari-docs-footer__divider {
    background-color: CanvasText;
  }
}

.akari-docs-footer__surface {
  padding: 48px var(--akari-doc-padding) 32px;
  border-start-start-radius: var(--akari-doc-radius);
  border-start-end-radius: var(--akari-doc-radius);
  background-color: var(--akari-doc-surface-color, var(--md-sys-color-surface));
  box-shadow:
    inset 1px 1px 0 var(--akari-doc-edge-color),
    inset -1px 0 0 var(--akari-doc-edge-color);
  --_cap-top: 48px;
  --_cap-bottom: 32px;
  color: var(--md-sys-color-on-surface);
}

.akari-docs-footer__inner {
  display: flex;
  flex-direction: column;
  gap: 40px;
  max-width: var(--akari-doc-max-width);
  margin-inline: auto;
}

.akari-docs-footer__band {
  display: grid;
  grid-template-columns: minmax(0, 680px) minmax(0, 460px);
  gap: 40px 48px;
  align-items: center;
  justify-content: center;
}

.akari-docs-footer__art {
  margin: 0;
  min-width: 0;
}

.akari-docs-footer__art-image {
  display: block;
  width: 100%;
  max-height: 680px;
  object-fit: contain;
  object-position: left center;
}

.akari-docs-footer__body {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.akari-docs-footer__heading {
  margin: 0;
  font-size: var(--md-sys-typescale-headline-small-font-size, 1.5rem);
  font-weight: var(--md-sys-typescale-headline-small-font-weight, 400);
  line-height: var(--md-sys-typescale-headline-small-line-height, 2rem);
}

.akari-docs-footer__copy {
  max-inline-size: 60ch;
  margin: 0;
  color: var(--md-sys-color-on-surface-variant);
  font-size: var(--md-sys-typescale-body-medium-font-size, 0.875rem);
  line-height: var(--md-sys-typescale-body-medium-line-height, 1.25rem);
}

.akari-docs-footer__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
}

.akari-docs-footer__action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 999px;
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  font-size: var(--md-sys-typescale-label-large-font-size, 0.875rem);
  font-weight: var(--md-sys-typescale-label-large-font-weight, 500);
  line-height: var(--md-sys-typescale-label-large-line-height, 1.25rem);
  text-decoration: none;
}

.akari-docs-footer__action:focus-visible {
  outline: 2px solid var(--md-sys-color-secondary);
  outline-offset: 2px;
}

.akari-docs-footer__brand-block {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.akari-docs-footer__brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  margin: 0;
}

.akari-docs-footer__logo {
  flex: none;
  width: 56px;
  height: 48px;
  object-fit: contain;
}

.akari-docs-footer__title {
  font-size: var(--md-sys-typescale-title-large-font-size, 1.375rem);
  font-weight: var(--md-sys-typescale-title-large-font-weight, 400);
  line-height: var(--md-sys-typescale-title-large-line-height, 1.75rem);
}

.akari-docs-footer__message {
  max-inline-size: 60ch;
  margin: 0;
  color: var(--md-sys-color-on-surface-variant);
  font-size: var(--md-sys-typescale-body-large-font-size, 1rem);
  line-height: var(--md-sys-typescale-body-large-line-height, 1.5rem);
}

.akari-docs-footer__bottom {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px 24px;
}

/* 关于区块是收束性的结尾，它下面这一行居中。 */
.akari-docs-footer__bottom--about {
  justify-content: center;
}

.akari-docs-footer__copyright {
  margin: 0;
  color: var(--md-sys-color-on-surface-variant);
  font-size: var(--md-sys-typescale-body-medium-font-size, 0.875rem);
  line-height: var(--md-sys-typescale-body-medium-line-height, 1.25rem);
}

@media (max-width: 840px) {
  .akari-docs-footer__band {
    grid-template-columns: minmax(0, 1fr);
  }

  .akari-docs-footer__art-image {
    max-height: 420px;
    object-position: center;
  }

  .akari-docs-footer__body {
    align-items: center;
    text-align: center;
  }

  .akari-docs-footer__copy {
    max-inline-size: 46ch;
  }

  .akari-docs-footer__actions {
    justify-content: center;
  }
}
</style>
