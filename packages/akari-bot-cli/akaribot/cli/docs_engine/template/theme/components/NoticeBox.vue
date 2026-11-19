<script setup lang="ts">
import { computed } from "vue"

const props = withDefaults(
  defineProps<{
    type?: string
    title?: string
  }>(),
  { type: "info", title: "" },
)

const titles: Record<string, string> = {
  info: "提示",
  tip: "提示",
  warning: "警告",
  danger: "危险",
  example: "示例",
  help: "帮助",
  deprecated: "已弃用",
}

const heading = computed(() => props.title || titles[props.type] || "提示")
</script>

<template>
  <aside class="notice-box" :class="`notice-box--${props.type}`">
    <div class="notice-box__title">{{ heading }}</div>
    <div class="notice-box__body">
      <slot />
    </div>
  </aside>
</template>
