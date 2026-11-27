<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";

interface CliArgument {
  name: string;
  required?: boolean;
}

interface CliOption {
  names: string[];
  metavar?: string;
  help?: string;
  isFlag?: boolean;
  required?: boolean;
  default?: unknown;
}

interface CliCommand {
  usage?: string | string[];
  summary?: string;
  arguments?: CliArgument[];
  options?: CliOption[];
}

interface AkariThemeConfig {
  akari?: {
    generated?: {
      cli?: Record<string, CliCommand>;
    };
  };
}

const props = defineProps<{ command: string }>();
const { site } = useData();

const command = computed<CliCommand | undefined>(() => {
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
    .map((argument) => (argument.required ? `${argument.name}（必填）` : `${argument.name}（可选）`))
    .join("、"),
);
</script>

<template>
  <section class="cli-options" aria-label="命令选项">
    <p v-if="!command" class="generated-hint">
      未找到命令 <code>{{ props.command }}</code> 的生成数据。
    </p>
    <template v-else>
      <div v-if="usages.length" class="cli-options__head">
        <code v-for="line in usages" :key="line" class="cli-options__usage">{{ line }}</code>
      </div>
      <p v-if="argumentsList.length" class="cli-options__arguments">参数：{{ argumentsLine }}</p>
      <div v-if="options.length" class="generated-table">
        <table>
          <thead>
            <tr>
              <th>选项</th>
              <th>取值</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="option in options" :key="option.names.join(' ')">
              <td>
                <template v-for="(name, index) in option.names" :key="name">
                  <code>{{ name }}</code><span v-if="index < option.names.length - 1">、</span>
                </template>
              </td>
              <td>
                <span v-if="option.isFlag">开关</span>
                <code v-else-if="option.metavar">{{ option.metavar }}</code>
                <span v-else>—</span>
              </td>
              <td>{{ option.help || "" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </section>
</template>
