<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

import {
  featureLabelKey,
  featureName,
  useGeneratedLabels,
  type BundledPackageEntry,
} from "./generated";

interface AdapterColumn {
  key: string;
  features: Record<string, boolean>;
}

interface AkariThemeConfig {
  akari?: {
    generated?: {
      packages?: Record<string, BundledPackageEntry>;
    };
  };
}

const props = withDefaults(defineProps<{ adapter?: string }>(), { adapter: "" });
const { site } = useData();
const { labels, label } = useGeneratedLabels();

function matchesAdapter(key: string, name: string): boolean {
  return (
    key === name ||
    key.endsWith(`.${name}`) ||
    key.endsWith(`/${name}`) ||
    key.endsWith(`-${name}`)
  );
}

const columns = computed<AdapterColumn[]>(() => {
  const config = (site.value.themeConfig ?? {}) as AkariThemeConfig;
  const packages = config.akari?.generated?.packages ?? {};
  const available: AdapterColumn[] = [];
  for (const [key, pkg] of Object.entries(packages)) {
    const features = pkg.facts?.features ?? {};
    if (Object.keys(features).length) {
      available.push({ key, features });
    }
  }
  if (!props.adapter) {
    return available;
  }
  const match = available.find((column) => matchesAdapter(column.key, props.adapter));
  return match ? [match] : [];
});

/** 文案给出的顺序在前，其余按键名排在后面。 */
const labelOrder = computed<string[]>(() => {
  const order: string[] = [];
  for (const key of Object.keys(labels.value)) {
    if (!key.startsWith("gen_feature_")) continue;
    order.push(key);
  }
  return order;
});

function rank(feature: string): number {
  const index = labelOrder.value.indexOf(featureLabelKey(feature));
  return index === -1 ? Number.MAX_SAFE_INTEGER : index;
}

const capabilityNames = computed<string[]>(() => {
  const names = new Set<string>();
  for (const column of columns.value) {
    for (const name of Object.keys(column.features)) names.add(name);
  }
  return [...names].sort((a, b) => {
    const left = rank(a);
    const right = rank(b);
    return left === right ? a.localeCompare(b) : left - right;
  });
});

function capabilityLabel(feature: string): string {
  return label(featureLabelKey(feature)) || featureName(feature);
}

function status(features: Record<string, boolean>, feature: string): string {
  return features[feature] === true
    ? label("gen_supported")
    : label("gen_placeholder");
}

const empty = computed(() => !columns.value.length || !capabilityNames.value.length);
</script>

<template>
  <section class="adapter-capabilities" :aria-label="label('gen_aria_capabilities')">
    <p v-if="empty" class="generated-hint">{{ label("gen_missing_features") }}</p>
    <div v-else-if="props.adapter" class="generated-table">
      <table>
        <thead>
          <tr>
            <th>{{ label("gen_capability") }}</th>
            <th>{{ label("gen_status") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="name in capabilityNames" :key="name">
            <td>{{ capabilityLabel(name) }}</td>
            <td>{{ status(columns[0]?.features ?? {}, name) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="generated-table">
      <table>
        <thead>
          <tr>
            <th>{{ label("gen_capability") }}</th>
            <th v-for="column in columns" :key="column.key">
              <code>{{ column.key }}</code>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="name in capabilityNames" :key="name">
            <td>{{ capabilityLabel(name) }}</td>
            <td v-for="column in columns" :key="column.key">
              {{ status(column.features, name) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
