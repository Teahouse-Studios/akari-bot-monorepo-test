<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

const props = defineProps<{ package: string }>();
const { site } = useData();

const dependencies = computed(() => {
  const config = (site.value.themeConfig ?? {}) as {
    akari?: { dependencies?: Record<string, string[]> };
  };
  return config.akari?.dependencies?.[props.package] ?? [];
});

function separator(index: number): string {
  return index === dependencies.value.length - 2 ? " 与 " : "、";
}
</script>

<template>
  <span class="package-dependencies" aria-label="运行依赖">
    <template v-for="(dependency, index) in dependencies" :key="dependency">
      <code>{{ dependency }}</code>
      <template v-if="index < dependencies.length - 1">{{ separator(index) }}</template>
    </template>
    <code v-if="!dependencies.length">{{ props.package }}</code>
  </span>
</template>
