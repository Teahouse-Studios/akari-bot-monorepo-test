<script setup lang="ts">
interface ModuleMetaEntry {
  name: string
  aliases?: string[]
  type?: string[]
  permission?: string
  platforms?: string[]
  excluded?: string[]
  forced?: boolean
  hidden?: boolean
  note?: string
}

const props = defineProps<{ modules: ModuleMetaEntry[] }>()

const typeLabels: Record<string, string> = {
  command: "命令",
  rss: "订阅",
  regex: "正则",
  event: "事件",
  option: "设置",
}

const permissionLabels: Record<string, string> = {
  public: "公开",
  admin: "管理员",
  superuser: "超级用户",
  base_superuser: "基础超级用户",
}

const platformLabels: Record<string, string> = {
  "QQBot": "QQ",
  "QQBot|Group": "QQ 群",
  "QQBot|Guild": "QQ 频道",
  "Discord": "Discord",
  "Telegram": "Telegram",
  "KOOK": "KOOK",
  "Matrix": "Matrix",
  "Web": "Web",
  "Console": "控制台",
}

function labelFor(value: string, labels: Record<string, string>): string {
  return labels[value] || value
}
</script>

<template>
  <section class="module-meta" aria-label="模块属性">
    <div v-for="item in props.modules" :key="item.name" class="module-meta__item">
      <div class="module-meta__name">
        <code>{{ item.name }}</code>
      </div>
      <div class="module-meta__badges">
        <span v-if="item.aliases?.length" class="meta-badge meta-badge--alias">
          别名
          <code v-for="alias in item.aliases" :key="alias">{{ alias }}</code>
        </span>
        <span
          v-for="kind in item.type"
          :key="kind"
          class="meta-badge"
          :class="`meta-badge--${kind}`"
        >
          {{ labelFor(kind, typeLabels) }}
        </span>
        <span v-if="item.permission" class="meta-badge" :class="`meta-badge--permission-${item.permission}`">
          模块权限 {{ labelFor(item.permission, permissionLabels) }}
        </span>
        <span v-if="item.forced" class="meta-badge meta-badge--forced">强制开启</span>
        <span v-if="item.hidden" class="meta-badge meta-badge--hidden">已隐藏</span>
        <span v-for="platform in item.platforms" :key="platform" class="meta-badge meta-badge--platform">
          仅 {{ labelFor(platform, platformLabels) }}
        </span>
        <span v-for="platform in item.excluded" :key="platform" class="meta-badge meta-badge--platform">
          排除 {{ labelFor(platform, platformLabels) }}
        </span>
        <span v-if="item.note" class="module-meta__note">{{ item.note }}</span>
      </div>
    </div>
  </section>
</template>
