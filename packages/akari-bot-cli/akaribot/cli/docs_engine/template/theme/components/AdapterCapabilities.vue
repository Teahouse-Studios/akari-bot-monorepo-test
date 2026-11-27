<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

interface AdapterColumn {
  key: string;
  features: Record<string, boolean>;
}

interface AkariThemeConfig {
  akari?: {
    generated?: {
      packages?: Record<string, { facts?: { features?: Record<string, boolean> } }>;
    };
  };
}

const props = withDefaults(defineProps<{ adapter?: string }>(), { adapter: "" });
const { site } = useData();

const capabilityLabels: Record<string, string> = {
  image: "图片",
  audio: "音频",
  video: "视频",
  mention: "提及",
  reaction: "表情回应",
  quote: "引用回复",
  typing: "输入状态",
  delete: "消息撤回",
  manage: "群组管理",
  permission_group: "权限组",
  private_msg: "私信",
  rss: "RSS 推送",
};

function stripPrefix(key: string): string {
  return key.startsWith("support_") ? key.slice("support_".length) : key;
}

function capabilityLabel(name: string): string {
  return capabilityLabels[name] ?? name;
}

function matchesAdapter(key: string, name: string): boolean {
  return (
    key === name ||
    key.endsWith(`.${name}`) ||
    key.endsWith(`/${name}`) ||
    key.endsWith(`-${name}`)
  );
}

function normalizeFeatures(features: Record<string, boolean>): Record<string, boolean> {
  const normalized: Record<string, boolean> = {};
  for (const [key, value] of Object.entries(features)) {
    const name = stripPrefix(key);
    if (!(name in normalized)) {
      normalized[name] = value === true;
    }
  }
  return normalized;
}

const columns = computed<AdapterColumn[]>(() => {
  const config = (site.value.themeConfig ?? {}) as AkariThemeConfig;
  const packages = config.akari?.generated?.packages ?? {};
  const available: AdapterColumn[] = [];
  for (const [key, pkg] of Object.entries(packages)) {
    const features = pkg.facts?.features ?? {};
    if (Object.keys(features).length) {
      available.push({ key, features: normalizeFeatures(features) });
    }
  }
  if (!props.adapter) {
    return available;
  }
  const match = available.find((column) => matchesAdapter(column.key, props.adapter));
  return match ? [match] : [];
});

const capabilityNames = computed<string[]>(() => {
  const names: string[] = [];
  for (const column of columns.value) {
    for (const name of Object.keys(column.features)) {
      if (!names.includes(name)) {
        names.push(name);
      }
    }
  }
  return names;
});

const empty = computed(() => !columns.value.length || !capabilityNames.value.length);
</script>

<template>
  <section class="adapter-capabilities" aria-label="适配器能力">
    <p v-if="empty" class="generated-hint">未找到适配器能力数据。</p>
    <div v-else-if="props.adapter" class="generated-table">
      <table>
        <thead>
          <tr>
            <th>能力</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="name in capabilityNames" :key="name">
            <td>{{ capabilityLabel(name) }}</td>
            <td>{{ columns[0].features[name] === true ? "支持" : "—" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="generated-table">
      <table>
        <thead>
          <tr>
            <th>能力</th>
            <th v-for="column in columns" :key="column.key">
              <code>{{ column.key }}</code>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="name in capabilityNames" :key="name">
            <td>{{ capabilityLabel(name) }}</td>
            <td v-for="column in columns" :key="column.key">
              {{ column.features[name] === true ? "支持" : "—" }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
