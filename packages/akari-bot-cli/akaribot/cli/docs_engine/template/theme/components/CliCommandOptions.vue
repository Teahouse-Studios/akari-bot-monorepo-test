<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

import { useGeneratedLabels, type BundledCliCommand } from "./generated";

interface AkariThemeConfig {
  akari?: {
    generated?: {
      cli?: Record<string, BundledCliCommand>;
    };
  };
}

const props = defineProps<{ command: string }>();
const { site } = useData();
const { label } = useGeneratedLabels();

const command = computed<BundledCliCommand | undefined>(() => {
  const config = (site.value.themeConfig ?? {}) as AkariThemeConfig;
  return config.akari?.generated?.cli?.[props.command];
});

const usages = computed<string[]>(() => {
  const usage = command.value?.usage;
  if (!usage) {
    return [];
  }
  return Array.isArray(usage) ? usage : [usage];
});

const argumentsList = computed(() => command.value?.arguments ?? []);
const options = computed(() => command.value?.options ?? []);

const argumentsLine = computed(() =>
  argumentsList.value
    .map((argument) =>
      [
        argument.name,
        label(argument.required ? "gen_argument_required" : "gen_argument_optional"),
      ].join(" "),
    )
    .join(label("gen_argument_separator")),
);
</script>

<template>
  <section class="cli-options" :aria-label="label('gen_aria_command_options')">
    <p v-if="!command" class="generated-hint">
      {{ label("gen_missing_command", { command: props.command }) }}
    </p>
    <template v-else>
      <div v-if="usages.length" class="cli-options__head">
        <code v-for="line in usages" :key="line" class="cli-options__usage">{{ line }}</code>
      </div>
      <p v-if="argumentsList.length" class="cli-options__arguments">
        {{ label("gen_arguments") }}{{ argumentsLine }}
      </p>
      <div v-if="options.length" class="generated-table">
        <table>
          <thead>
            <tr>
              <th>{{ label("gen_option") }}</th>
              <th>{{ label("gen_value") }}</th>
              <th>{{ label("gen_comment") }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="option in options" :key="(option.names ?? []).join(' ')">
              <td>
                <template v-for="(name, index) in option.names ?? []" :key="name">
                  <code>{{ name }}</code
                  ><span v-if="index < (option.names ?? []).length - 1">{{ label("gen_argument_separator") }}</span>
                </template>
              </td>
              <td>
                <span v-if="option.isFlag">{{ label("gen_flag") }}</span>
                <code v-else-if="option.metavar">{{ option.metavar }}</code>
                <span v-else>{{ label("gen_placeholder") }}</span>
              </td>
              <td>{{ option.help || "" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </section>
</template>
