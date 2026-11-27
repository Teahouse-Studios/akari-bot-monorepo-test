<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

import {
  useGeneratedLabels,
  type BundledConfigField,
  type BundledConfigTable,
} from "./generated";

interface AkariThemeConfig {
  akari?: {
    generated?: {
      packages?: Record<string, { facts?: { config?: BundledConfigTable[] } }>;
    };
  };
}

const props = defineProps<{ table: string }>();
const { site } = useData();
const { label } = useGeneratedLabels();

const table = computed<BundledConfigTable | undefined>(() => {
  const config = (site.value.themeConfig ?? {}) as AkariThemeConfig;
  const packages = config.akari?.generated?.packages ?? {};
  for (const pkg of Object.values(packages)) {
    const match = (pkg.facts?.config ?? []).find((item) => item.table === props.table);
    if (match) {
      return match;
    }
  }
  return undefined;
});

const fields = computed(() => table.value?.fields ?? []);

function fieldMarkers(field: BundledConfigField): string {
  const markers: string[] = [];
  if (field.required) {
    markers.push(label("gen_required"));
  }
  if (field.secret) {
    markers.push(label("gen_secret"));
  }
  return markers.join("");
}

function hasDefault(field: BundledConfigField): boolean {
  return field.default !== undefined && field.default !== null;
}

function formatDefault(field: BundledConfigField): string {
  const value = field.default;
  if (typeof value === "boolean") {
    return label(value ? "gen_true" : "gen_false");
  }
  if (typeof value === "string") {
    return value === "" ? '""' : value;
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}
</script>

<template>
  <section class="config-fields" :aria-label="label('gen_aria_config_fields')">
    <p v-if="!table" class="generated-hint">
      {{ label("gen_missing_config", { table: props.table }) }}
    </p>
    <p v-else-if="!fields.length" class="generated-hint">{{ label("gen_empty_config") }}</p>
    <div v-else class="generated-table">
      <table>
        <thead>
          <tr>
            <th>{{ label("gen_field") }}</th>
            <th>{{ label("gen_type") }}</th>
            <th>{{ label("gen_default") }}</th>
            <th>{{ label("gen_comment") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="field in fields" :key="field.name">
            <td>
              <code>{{ field.name }}</code>
              <span v-if="fieldMarkers(field)" class="config-fields__flag">{{ fieldMarkers(field) }}</span>
            </td>
            <td><code>{{ field.type }}</code></td>
            <td>
              <code v-if="hasDefault(field)">{{ formatDefault(field) }}</code>
              <span v-else>{{ label("gen_placeholder") }}</span>
            </td>
            <td>{{ field.comment || "" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
