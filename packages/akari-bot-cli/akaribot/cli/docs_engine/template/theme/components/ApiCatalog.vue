<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

interface Parameter { name: string; type: string; default: string; description: string }
interface Method { name: string; kind: string; description: string; signature: string; parameters: Parameter[] }
interface Entry { name: string; kind: string; description: string; signature: string; parameters: Parameter[]; methods?: Method[] }

const { site } = useData();
const groups = computed(() => {
  const config = (site.value.themeConfig ?? {}) as {
    akari?: { apiCatalog?: { groups?: { name: string; entries: Entry[] }[] } };
  };
  return config.akari?.apiCatalog?.groups ?? [];
});

function params(entry: Entry | Method): Parameter[] {
  return entry.parameters ?? [];
}

function kindLabel(entry: Entry): string {
  return entry.kind === "class" ? "类" : entry.kind === "function" ? "函数" : "常量";
}
</script>

<template>
  <div class="akari-api-catalog">
    <p v-if="!groups.length" class="akari-api-catalog__empty">
      当前构建没有生成 API 目录。
    </p>
    <section v-for="group in groups" :key="group.name" class="akari-api-catalog__group">
      <h2>{{ group.name }}</h2>
      <article v-for="entry in group.entries" :key="entry.name" class="akari-api-catalog__entry">
        <h3>
          <code>{{ entry.name }}</code>
          <span class="akari-api-catalog__kind">{{ kindLabel(entry) }}</span>
        </h3>
        <p v-if="entry.description" class="akari-api-catalog__description">{{ entry.description }}</p>
        <p v-if="entry.signature" class="akari-api-catalog__signature">
          <code>{{ entry.signature }}</code>
        </p>
        <dl v-if="params(entry).length" class="akari-api-catalog__params">
          <template v-for="parameter in params(entry)" :key="parameter.name">
            <dt>
              <code>{{ parameter.name }}</code>
              <span v-if="parameter.type" class="akari-api-catalog__type">{{ parameter.type }}</span>
              <span v-if="parameter.default" class="akari-api-catalog__default">默认 {{ parameter.default }}</span>
            </dt>
            <dd v-if="parameter.description">{{ parameter.description }}</dd>
          </template>
        </dl>
        <section v-if="entry.methods?.length" class="akari-api-catalog__methods">
          <article v-for="method in entry.methods" :key="method.name" class="akari-api-catalog__method">
            <h4><code>{{ method.name }}</code></h4>
            <p v-if="method.description" class="akari-api-catalog__description">{{ method.description }}</p>
            <p v-if="method.signature" class="akari-api-catalog__signature">
              <code>{{ method.signature }}</code>
            </p>
            <dl v-if="params(method).length" class="akari-api-catalog__params">
              <template v-for="parameter in params(method)" :key="parameter.name">
                <dt>
                  <code>{{ parameter.name }}</code>
                  <span v-if="parameter.type" class="akari-api-catalog__type">{{ parameter.type }}</span>
                  <span v-if="parameter.default" class="akari-api-catalog__default">默认 {{ parameter.default }}</span>
                </dt>
                <dd v-if="parameter.description">{{ parameter.description }}</dd>
              </template>
            </dl>
          </article>
        </section>
      </article>
    </section>
  </div>
</template>

<style scoped>
.akari-api-catalog {
  display: grid;
  gap: 28px;
  margin-block-start: 28px;
}

.akari-api-catalog__group > h2 {
  margin-block: 0 16px;
}

.akari-api-catalog__entry,
.akari-api-catalog__method {
  padding-block: 14px;
  border-block-start: 1px solid var(--md-sys-color-outline-variant);
}

.akari-api-catalog__entry > h3,
.akari-api-catalog__method > h4 {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-block: 0 6px;
}

.akari-api-catalog__kind,
.akari-api-catalog__type,
.akari-api-catalog__default {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.78rem;
  font-weight: 400;
}

.akari-api-catalog__description {
  margin-block: 4px 8px;
  color: var(--md-sys-color-on-surface-variant);
}

.akari-api-catalog__signature {
  margin-block: 6px 10px;
  overflow-x: auto;
}

.akari-api-catalog__params {
  display: grid;
  grid-template-columns: minmax(8rem, max-content) 1fr;
  gap: 4px 14px;
  margin-block: 8px 0;
}

.akari-api-catalog__params dt {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: baseline;
}

.akari-api-catalog__params dd {
  margin: 0;
  color: var(--md-sys-color-on-surface-variant);
}

.akari-api-catalog__methods {
  display: grid;
  gap: 8px;
  margin-block-start: 12px;
  padding-inline-start: 14px;
  border-inline-start: 1px solid var(--md-sys-color-outline-variant);
}

.akari-api-catalog__empty {
  color: var(--md-sys-color-on-surface-variant);
}

@media (max-width: 640px) {
  .akari-api-catalog__params {
    grid-template-columns: 1fr;
    gap: 2px;
  }

  .akari-api-catalog__params dd {
    margin-block-end: 6px;
  }
}
</style>
