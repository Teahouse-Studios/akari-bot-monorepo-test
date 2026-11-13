<script setup lang="ts">
import { computed } from "vue"

const props = withDefaults(
  defineProps<{
    log?: string[]
    caption?: string
    // 按钮交互由外部模板提供；这里声明属性以避免透传到根元素。
    buttons?: unknown[]
  }>(),
  { log: () => [], caption: "", buttons: () => [] },
)

interface Bubble {
  role: "user" | "bot" | "divider"
  text: string
}

function isDivider(line: string): boolean {
  const text = line.trim()
  return /^[〰~～\s\uFE0F]+$/u.test(text) && text.replace(/[\s\uFE0F]/gu, "").length >= 3
}

const bubbles = computed(() => {
  const result: Bubble[] = []
  for (const raw of props.log) {
    const line = raw.trimEnd()
    if (!line.trim()) continue
    if (isDivider(line)) {
      result.push({ role: "divider", text: "" })
      continue
    }
    const user = /^(?:用户|user)\s*[：:]\s*/i.exec(line)
    const bot = /^(?:机器人|bot)\s*[：:]\s*/i.exec(line)
    if (user) {
      result.push({ role: "user", text: line.slice(user[0].length) })
    } else if (bot) {
      result.push({ role: "bot", text: line.slice(bot[0].length) })
    } else if (result.length && result[result.length - 1].role !== "divider") {
      result[result.length - 1].text += `\n${line}`
    } else {
      result.push({ role: "bot", text: line.trimStart() })
    }
  }
  return splitTrailingImages(result)
})

interface Segment {
  text?: string
  code?: boolean
  image?: { src: string; alt: string; natural?: boolean }
}

function segments(text: string): Segment[] {
  const result: Segment[] = []
  const pattern = /`([^`]*)`|!\[([^\]]*)\]\(([^)\s]+)\)(\{natural\})?/g
  let last = 0
  let match: RegExpExecArray | null
  while ((match = pattern.exec(text))) {
    if (match.index > last) result.push({ text: text.slice(last, match.index) })
    if (match[1] !== undefined) {
      result.push({ text: match[1], code: true })
    } else {
      result.push({ image: { alt: match[2], src: match[3], natural: match[4] !== undefined } })
    }
    last = match.index + match[0].length
  }
  if (last < text.length) result.push({ text: text.slice(last) })
  return result
}

function isImageOnly(text: string): boolean {
  const parts = segments(text).filter(
    (segment) => segment.text === undefined || segment.text.trim() !== "",
  )
  return parts.length > 0 && parts.every((segment) => segment.image !== undefined)
}

function segmentSource(segment: Segment): string {
  if (segment.image) {
    const marker = segment.image.natural ? "{natural}" : ""
    return `![${segment.image.alt}](${segment.image.src})${marker}`
  }
  if (segment.code) return `\`${segment.text ?? ""}\``
  return segment.text ?? ""
}

function splitTrailingImages(bubbles: Bubble[]): Bubble[] {
  const split: Bubble[] = []
  for (const bubble of bubbles) {
    if (bubble.role === "divider") {
      split.push(bubble)
      continue
    }
    const parts = segments(bubble.text)
    let end = parts.length
    const images: { src: string; alt: string; natural?: boolean }[] = []
    while (end > 0) {
      const part = parts[end - 1]
      if (part.image) {
        images.unshift(part.image)
        end -= 1
        continue
      }
      if (part.text !== undefined && part.text.trim() === "" && images.length) {
        end -= 1
        continue
      }
      break
    }
    if (!images.length || end === 0) {
      split.push(bubble)
      continue
    }
    const text = parts.slice(0, end).map(segmentSource).join("").trimEnd()
    if (!text) {
      split.push(bubble)
      continue
    }
    split.push(
      { role: bubble.role, text },
      {
        role: bubble.role,
        text: images
          .map((image) => `![${image.alt}](${image.src})${image.natural ? "{natural}" : ""}`)
          .join("\n"),
      },
    )
  }
  return split
}
</script>

<template>
  <section v-if="bubbles.length" class="chat-example">
    <p v-if="props.caption" class="chat-example__caption">{{ props.caption }}</p>
    <template v-for="(bubble, index) in bubbles" :key="index">
      <div v-if="bubble.role === 'divider'" class="chat-example__divider" role="separator" aria-label="一段时间过去">
        <span class="chat-example__divider-rule"></span>
        <span class="chat-example__divider-wave" aria-hidden="true">〰〰〰</span>
        <span class="chat-example__divider-rule"></span>
      </div>
      <div v-else class="chat-example__row" :class="`chat-example__row--${bubble.role}`">
        <div
          class="chat-example__bubble"
          :class="{ 'chat-example__bubble--image': isImageOnly(bubble.text) }"
        >
          <span class="chat-example__role">{{ bubble.role === "user" ? "用户" : "机器人" }}</span>
          <span v-for="(segment, segmentIndex) in segments(bubble.text)" :key="segmentIndex">
            <code v-if="segment.code">{{ segment.text }}</code>
            <a
              v-else-if="segment.image"
              class="chat-example__image"
              :class="{ 'chat-example__image--natural': segment.image.natural }"
              :href="segment.image.src"
              target="_blank"
              rel="noreferrer"
            >
              <img :src="segment.image.src" :alt="segment.image.alt" loading="lazy" />
            </a>
            <template v-else>{{ segment.text }}</template>
          </span>
        </div>
      </div>
    </template>
  </section>
</template>
