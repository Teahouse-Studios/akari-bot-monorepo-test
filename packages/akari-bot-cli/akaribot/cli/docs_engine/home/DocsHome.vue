<script setup lang="ts">
import { computed } from "vue";
import { useData, withBase } from "vitepress";
import { useAkariColorScheme } from "../../composables/useColorScheme";
import { useBrandAsset } from "../../composables/useBrandAsset";

type HomeAction = {
  label: string;
  href: string;
  icon?: string;
  tone?: "filled" | "tonal" | "text";
};

type HomeStat = {
  value: string;
  label: string;
  icon?: string;
};

type HomeLink = {
  label: string;
  href: string;
  icon?: string;
};

type HomeRole = {
  eyebrow: string;
  title: string;
  description: string;
  href: string;
  icon: string;
  links: HomeLink[];
};

type HomeTopic = {
  title: string;
  description: string;
  href: string;
  image: string;
  tag: string;
};

type HomeContribute = {
  title: string;
  description: string;
  icon?: string;
  logo?: string;
  links: HomeLink[];
};

type HomeSection = {
  eyebrow: string;
  title: string;
};

type HomeSections = {
  searchPlaceholder: string;
  statsLabel: string;
  start: HomeSection;
  topics: HomeSection;
  contributeLabel: string;
};

type HomeData = {
  title: string;
  lead: string;
  sections: HomeSections;
  actions: HomeAction[];
  stats: HomeStat[];
  roles: HomeRole[];
  topics: HomeTopic[];
  contribute: {
    cards: HomeContribute[];
  };
};

const { frontmatter } = useData();
const { resolved } = useAkariColorScheme();
const isDark = computed(() => resolved.value === "dark");
const logo = useBrandAsset("logo", "/home/logo.png");
const logoDark = useBrandAsset("logoDark", "/home/logo-night.png");

const lightVineColors = {
  leaf: "#ea71ca",
  flower: "#f4c3e6",
  flowerStem: "#d71da6",
  bud: "#e873c9",
  base: "#d025a2",
  fill: "#dd46b5",
  tint: "#ea7bcd",
  halo: "#e83bba",
  edge: "#f042c1",
  fine: "#d02fa5",
};

const darkVineColors = {
  leaf: "#480436",
  flower: "#f0b7e1",
  flowerStem: "#e684cc",
  bud: "#c577b0",
  base: "#e69ed3",
  fill: "#870d6d",
  tint: "#f07fd2",
  halo: "#e580ca",
  edge: "#c346a2",
  fine: "#d841b0",
};

const lightPopoutColors = {
  leaf: "#ff80dd",
  flower: "#f5ade1",
  flowerStem: "#e52eb4",
  bud: "#b41389",
  base: "#f051c6",
  fill: "#ee17b4",
  tint: "#eb37bb",
  halo: "#d714a3",
  edge: "#f22cbd",
  fine: "#a91481",
};

const darkPopoutColors = {
  leaf: "#5c0a46",
  flower: "#a16891",
  flowerStem: "#8e2572",
  bud: "#902373",
  base: "#9a4c85",
  fill: "#912173",
  tint: "#74255f",
  halo: "#6f1557",
  edge: "#7b1e62",
  fine: "#832168",
};


const home = computed<HomeData | null>(() => {
  const value = frontmatter.value.home;
  if (!value) return null;
  if (typeof value === "string") {
    try {
      return JSON.parse(value) as HomeData;
    } catch {
      return null;
    }
  }
  return value as HomeData;
});

function href(value: string): string {
  return value.startsWith("/") && !value.startsWith("//") ? withBase(value) : value;
}

function asset(value: string): string {
  return withBase(value);
}
</script>

<template>
  <div v-if="home" class="akari-home">
    <div class="akari-home__hero-layer">
      <section class="akari-home__hero" aria-labelledby="akari-home-title">
      <AkariFluidWall
        class="akari-home__fluid"
        variant="blossom"
        texture="vine"
        :ripple="1.55"
        :ripple-speed="1.55"
        :ripple-rings="3.2"
        :ripple-sway="1.55"
        :vine-glow="0.9"
        :shadow="0.45"
        shadow-color="#8a4bd2"
        :wall-shadow="0.45"
        :wall-shadow-size="0.9"
        wall-shadow-color="#a443f4"
        :wall-shadow-angle="162"
        :wall-shadow-blur="5"
        :underlay-color="isDark ? '#3c2a2a' : '#a510a8'"
        :underlay-opacity="isDark ? 0.25 : 1"
        mote-blend="additive"
        height="300px"
        :texture-opacity="0.55"
        :vine-colors="isDark ? darkVineColors : lightVineColors"
        :vine-popout-colors="isDark ? darkPopoutColors : lightPopoutColors"
        popout
        inward
        :style="{
          '--md-sys-color-primary': isDark ? '#e69ed3' : '#60154c',
          '--md-sys-color-primary-container': isDark ? '#480436' : '#e3cedd',
        }"
      >
        <h1 id="akari-home-title" class="akari-home__title">{{ home.title }}</h1>
        <p class="akari-home__lead">{{ home.lead }}</p>
        <div class="akari-home__search">
          <SearchDock
            variant="hero"
            immersive
            align="center"
            width="min(100%, 560px)"
            :placeholder="home.sections.searchPlaceholder"
          />
        </div>
      </AkariFluidWall>

      <div class="akari-home__stats" :aria-label="home.sections.statsLabel">
        <div v-for="stat in home.stats" :key="stat.label" class="akari-home__stat">
          <span class="akari-home__stat-icon" aria-hidden="true">
            <m3e-icon :name="stat.icon || 'description'"></m3e-icon>
          </span>
          <strong>{{ stat.value }}</strong>
          <span>{{ stat.label }}</span>
        </div>
      </div>

      </section>
    </div>

    <div class="akari-home__content">

    <section class="akari-home__start" aria-labelledby="akari-home-start">
      <div class="akari-home__start-brand">
        <img :src="asset(isDark ? logoDark : logo)" alt="AkariBot" />
      </div>

      <div class="akari-home__start-panel">
        <header class="akari-home__section-head">
          <div>
            <p class="akari-home__eyebrow">{{ home.sections.start.eyebrow }}</p>
            <h2 id="akari-home-start">{{ home.sections.start.title }}</h2>
          </div>
        </header>

        <div class="akari-home__roles">
          <article v-for="role in home.roles" :key="role.title" class="akari-home__role">
            <div class="akari-home__role-copy">
              <p class="akari-home__eyebrow">{{ role.eyebrow }}</p>
              <h3><a :href="href(role.href)">{{ role.title }}</a></h3>
              <p class="akari-home__role-description">{{ role.description }}</p>

              <div v-if="role.links.length > 2" class="akari-home__role-extra">
                <a v-for="link in role.links.slice(2)" :key="link.label" :href="href(link.href)">
                  {{ link.label }}
                </a>
              </div>
            </div>

            <div class="akari-home__role-actions">
              <a
                v-for="link in role.links.slice(0, 2)"
                :key="link.label"
                class="akari-home__role-button"
                :href="href(link.href)"
              >
                <span>{{ link.label }}</span>
                <m3e-icon name="arrow_forward" aria-hidden="true"></m3e-icon>
              </a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="akari-home__section" aria-labelledby="akari-home-topics">
      <header class="akari-home__section-head">
        <div>
          <p class="akari-home__eyebrow">{{ home.sections.topics.eyebrow }}</p>
          <h2 id="akari-home-topics">{{ home.sections.topics.title }}</h2>
        </div>
      </header>
      <div class="akari-home__topic-grid">
        <a v-for="topic in home.topics" :key="topic.title" class="akari-home__topic" :href="href(topic.href)">
          <img class="akari-home__topic-image" :src="asset(topic.image)" alt="" loading="lazy" />
          <span class="akari-home__topic-copy">
            <span class="akari-home__topic-tag">{{ topic.tag }}</span>
            <strong>{{ topic.title }}</strong>
            <span class="akari-home__topic-description">{{ topic.description }}</span>
          </span>
        </a>
      </div>
    </section>

    <section class="akari-home__contribute" :aria-label="home.sections.contributeLabel">
      <article v-for="card in home.contribute.cards" :key="card.title" class="akari-home__contribute-card">
        <div class="akari-home__contribute-head">
          <img
            v-if="card.logo"
            class="akari-home__contribute-logo"
            :src="asset(card.logo)"
            :alt="card.title"
          />
          <span v-else class="akari-home__contribute-icon">
            <m3e-icon :name="card.icon || 'code'" aria-hidden="true"></m3e-icon>
          </span>
          <h2>{{ card.title }}</h2>
        </div>
        <p>{{ card.description }}</p>
        <div class="akari-home__contribute-links">
          <a v-for="link in card.links" :key="link.label" :href="href(link.href)">
            <m3e-icon v-if="link.icon" :name="link.icon" aria-hidden="true"></m3e-icon>
            {{ link.label }}
            <m3e-icon name="open_in_new" aria-hidden="true"></m3e-icon>
          </a>
        </div>
      </article>
    </section>
    </div>

  </div>
</template>

<style scoped>
.akari-home {
  --home-radius: 24px;
  display: flex;
  flex-direction: column;
  gap: clamp(24px, 3vw, 36px);
  color: var(--md-sys-color-on-surface);
}

.akari-home__hero-layer {
  width: calc(100% + 48px);
  margin: -24px -24px 0;
}

.akari-home__content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  width: calc(100% + 48px);
  margin-inline: -24px;
  padding-block: 0 20px;
  gap: clamp(32px, 5vw, 60px);
}

.akari-home a {
  color: inherit;
  text-decoration: none;
}

.akari-home a::before {
  content: none !important;
  display: none !important;
}

@media (max-width: 600px) {
  .akari-home__hero-layer {
    width: calc(100% + 24px);
    margin: -12px -12px 0;
  }

  .akari-home__content {
    width: calc(100% + 24px);
    margin-inline: -12px;
  }
}

@media (min-width: 1024px) {
  .akari-home__hero-layer {
    width: calc(100% + 80px);
    margin: -24px -56px 0 -24px;
  }

  .akari-home__content {
    width: calc(100% + 80px);
    margin-inline: -24px -56px;
  }
}

.akari-home__hero {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.akari-home__fluid {
  inline-size: 100%;
}

.akari-home :deep(.akari-fluid-wall) {
  border: 0;
  border-radius: 32px;
}

:global(.akari-search-dock[data-variant="hero"] .akari-search-trigger) {
  border: 1px solid var(--md-sys-color-outline-variant) !important;
  box-shadow: none !important;
}

.akari-home__title {
  align-self: center;
  margin: 0;
  max-inline-size: 12em;
  color: var(--md-sys-color-on-surface);
  font-size: clamp(2.2rem, 3.8vw, 3.5rem);
  font-weight: 500;
  line-height: 1.04;
  letter-spacing: -0.04em;
  text-align: center;
  text-wrap: balance;
}

.akari-home__lead {
  align-self: center;
  max-inline-size: 36em;
  margin: 0 auto;
  color: var(--md-sys-color-on-surface-variant);
  font-size: clamp(0.95rem, 1.1vw, 1.05rem);
  line-height: 1.6;
  text-align: center;
}

.akari-home__search {
  width: min(100%, 560px);
  margin: 10px auto 0;
}

:deep(.akari-fluid-wall__block[data-slot="main"]) {
  max-inline-size: none;
  inline-size: 100%;
}

.akari-home__lead {
  max-inline-size: 720px;
}

.akari-home__stats {
  position: relative;
  z-index: 2;
  display: grid;
  width: 100%;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-block-start: 12px;
}

.akari-home__stat {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 88px;
  padding: 14px 16px;
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: 20px;
  background-color: transparent;
  color: var(--md-sys-color-on-surface);
}

.akari-home__stat-icon {
  position: absolute;
  top: 12px;
  right: 12px;
  color: var(--md-sys-color-on-surface-variant);
  opacity: 0.8;
  font-size: 1.15rem;
  line-height: 1;
}

.akari-home__stat strong {
  font-size: clamp(1.6rem, 2.4vw, 2.1rem);
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.04em;
}

.akari-home__stat > span:last-child {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.82rem;
  opacity: 0.9;
}

.akari-home__start {
  display: grid;
  grid-template-columns: minmax(280px, 0.88fr) minmax(0, 1.12fr);
  gap: clamp(32px, 5vw, 72px);
  align-items: center;
}

.akari-home__start-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
  padding: 0;
  background-color: transparent;
}

.akari-home__start-brand img {
  display: block;
  width: min(100%, 460px);
  height: auto;
  margin: 0;
}

.akari-home__start-panel {
  padding: 0;
  background-color: transparent;
}

.akari-home__start-panel .akari-home__section-head {
  margin-bottom: clamp(20px, 2.4vw, 28px);
}

.akari-home__start-panel .akari-home__section-head h2 {
  font-size: clamp(2rem, 3.4vw, 2.9rem);
}

.akari-home__roles {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.akari-home__role {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(190px, 0.55fr);
  gap: 24px;
  align-items: center;
  padding: 22px 24px;
  border-radius: 20px;
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

.akari-home__role .akari-home__eyebrow {
  color: var(--md-sys-color-on-secondary-container);
  opacity: 0.68;
}

.akari-home__role h3 {
  margin: 0;
  font-size: clamp(1.35rem, 2vw, 1.65rem);
  font-weight: 500;
  letter-spacing: -0.03em;
}

.akari-home__role-description {
  max-inline-size: 34em;
  margin: 10px 0 0;
  color: var(--md-sys-color-on-secondary-container);
  font-size: 0.9rem;
  line-height: 1.6;
  opacity: 0.82;
}

.akari-home__role-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0;
}

.akari-home__role-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: 14px;
  background-color: var(--md-sys-color-surface-container-lowest);
  color: var(--md-sys-color-on-surface);
  font-size: 0.84rem;
  transition: background-color 180ms ease, border-color 180ms ease;
}

.akari-home__role-button:hover,
.akari-home__role-button:focus-visible {
  border-color: var(--md-sys-color-primary);
  background-color: var(--md-sys-color-surface-container-highest);
}

.akari-home__role-button m3e-icon {
  color: var(--md-sys-color-primary);
  font-size: 1rem;
}

.akari-home__role-extra {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  margin-top: 10px;
}

.akari-home__role-extra a {
  border-bottom: 1px solid transparent;
  color: var(--md-sys-color-on-secondary-container);
  font-size: 0.76rem;
  opacity: 0.72;
  transition: border-color 180ms ease, opacity 180ms ease;
}

.akari-home__role-extra a:hover {
  border-color: currentColor;
  opacity: 1;
}

.akari-home__section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: clamp(24px, 3vw, 36px);
}

.akari-home__eyebrow {
  margin: 0 0 10px;
  color: var(--md-sys-color-primary);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.akari-home__section-head h2 {
  margin: 0;
  font-size: clamp(2.2rem, 4.2vw, 3.6rem);
  font-weight: 500;
  line-height: 1.05;
  letter-spacing: -0.04em;
}

.akari-home__start-panel .akari-home__section-head {
  margin-bottom: 28px;
}

.akari-home__section-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid transparent;
  color: var(--md-sys-color-primary);
  font-size: 0.88rem;
  transition: border-color 180ms ease;
}

.akari-home__section-link:hover {
  border-color: var(--md-sys-color-primary);
}

.akari-home__contribute {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.akari-home__contribute-card {
  padding: clamp(22px, 3vw, 32px);
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: var(--home-radius);
  background-color: var(--md-sys-color-surface-container-low);
}

.akari-home__contribute-head {
  display: flex;
  align-items: center;
  gap: 14px;
}

.akari-home__contribute-head h2 {
  margin: 0;
  font-size: clamp(1.4rem, 2.2vw, 1.8rem);
  font-weight: 500;
  letter-spacing: -0.03em;
}

.akari-home__contribute-icon {
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background-color: var(--md-sys-color-surface-container-lowest);
  color: var(--md-sys-color-primary);
}

.akari-home__contribute-logo {
  width: 112px;
  height: auto;
}

.akari-home__contribute-card > p {
  max-width: 42em;
  margin: 16px 0 0;
  color: var(--md-sys-color-on-surface-variant);
  line-height: 1.65;
}

.akari-home__contribute-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
  margin-top: 18px;
}

.akari-home__contribute-links a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-bottom: 1px solid transparent;
  color: var(--md-sys-color-primary);
  font-size: 0.84rem;
  transition: border-color 180ms ease;
}

.akari-home__contribute-links a:hover {
  border-color: var(--md-sys-color-primary);
}

.akari-home__topic-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.akari-home__topic {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: var(--home-radius);
  background-color: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  transition: background-color 180ms ease;
}

.akari-home__topic:hover {
  background-color: var(--md-sys-color-surface-container);
}

.akari-home__topic-image {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  margin: 0;
  object-fit: cover;
}

.akari-home__topic-copy {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 18px 20px 22px;
}

.akari-home__topic-tag {
  color: var(--md-sys-color-primary);
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.akari-home__topic-copy strong {
  font-size: 1.18rem;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.akari-home__topic-description {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.85rem;
  line-height: 1.6;
}

@media (max-width: 900px) {
  .akari-home__content {
    gap: 44px;
  }

  .akari-home__start {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .akari-home__start-brand {
    min-height: 0;
    padding-block: 8px;
  }

  .akari-home__start-brand img {
    width: min(70%, 340px);
  }

  .akari-home__contribute {
    grid-template-columns: 1fr;
  }

  .akari-home__topic-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .akari-home__content {
    gap: 40px;
  }

  .akari-home__stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .akari-home__title {
    font-size: clamp(2.2rem, 9vw, 3rem);
  }

  .akari-home__start-brand img {
    width: min(74%, 260px);
  }

  .akari-home__role {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 20px;
  }

  .akari-home__role-actions {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .akari-home__role-button {
    flex: 1 1 160px;
  }

  .akari-home__section-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .akari-home__topic-grid {
    grid-template-columns: 1fr;
  }
}

</style>
