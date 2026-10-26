<script setup lang="ts">
import { computed } from "vue"

interface CommandOption {
  flag: string
  desc: string
}

const props = withDefaults(
  defineProps<{
    usage: string | string[]
    permission?: string
    type?: string
    aliases?: string[]
    options?: CommandOption[]
    note?: string
  }>(),
  { permission: "", type: "", aliases: () => [], options: () => [], note: "" },
)

const usages = computed(() => (Array.isArray(props.usage) ? props.usage : [props.usage]))

const permissionLabels: Record<string, string> = {
  public: "公开",
  admin: "管理员",
  superuser: "超级用户",
  base_superuser: "基础超级用户",
}

const typeLabels: Record<string, string> = {
  command: "命令",
  rss: "订阅",
  regex: "正则",
  event: "事件",
  option: "设置",
}
</script>

<template>
  <section class="command-usage">
    <div class="command-usage__head">
      <code v-for="line in usages" :key="line" class="command-usage__line">{{ line }}</code>
      <span v-if="props.permission" class="meta-badge" :class="`meta-badge--permission-${props.permission}`">
        {{ permissionLabels[props.permission] || props.permission }}
      </span>
      <span v-if="props.type" class="meta-badge" :class="`meta-badge--${props.type}`">
        {{ typeLabels[props.type] || props.type }}
      </span>
      <span v-if="props.aliases.length" class="meta-badge meta-badge--alias">
        别名
        <code v-for="alias in props.aliases" :key="alias">{{ alias }}</code>
      </span>
    </div>
    <table v-if="props.options.length" class="command-usage__options">
      <thead>
        <tr>
          <th>选项</th>
          <th>说明</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="option in props.options" :key="option.flag">
          <td><code>{{ option.flag }}</code></td>
          <td>{{ option.desc }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="props.note" class="command-usage__note">{{ props.note }}</p>
    <slot />
  </section>
</template>
