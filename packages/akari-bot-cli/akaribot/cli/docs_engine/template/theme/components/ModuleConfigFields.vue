<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

interface ConfigField {
  name: string;
  type: string;
  default?: unknown;
  secret?: boolean;
  comment?: string;
  required?: boolean;
}

interface ConfigTable {
  table: string;
  file?: string;
  secret?: boolean;
  fields?: ConfigField[];
}

interface AkariThemeConfig {
  akari?: {
    generated?: {
      packages?: Record<string, { facts?: { config?: ConfigTable[] } }>;
    };
  };
}

const props = defineProps<{ table: string }>();
const { site } = useData();

const table = computed<ConfigTable | undefined>(() => {
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

function fieldMarkers(field: ConfigField): string {
  const markers: string[] = [];
  if (field.required) {
    markers.push("必填");
  }
  if (field.secret) {
    markers.push("（敏感）");
  }
  return markers.join("");
}

function hasDefault(field: ConfigField): boolean {
  return field.default !== undefined && field.default !== null;
}

function formatDefault(field: ConfigField): string {
  const value = field.default;
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
  <section class="config-fields" aria-label="配置字段">
    <p v-if="!table" class="generated-hint">
      未找到配置表 <code>{{ props.table }}</code> 的生成数据。
    </p>
    <p v-else-if="!fields.length" class="generated-hint">该表没有配置字段。</p>
    <div v-else class="generated-table">
      <table>
        <thead>
          <tr>
            <th>字段</th>
            <th>类型</th>
            <th>默认值</th>
            <th>说明</th>
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
              <span v-else>—</span>
            </td>
            <td>{{ field.comment || "" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
