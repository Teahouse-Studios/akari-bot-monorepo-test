import { computed, type ComputedRef } from "vue";
import { useData } from "vitepress";

/** 生成数据里附着在事实旁的文案，键以 `gen_` 开头。 */
export interface BundledGeneratedData {
  labels?: Record<string, string>;
}

/** 填充 `{name}` 占位；调用方未给出的名字保持原样。 */
export function formatGeneratedLabel(
  template: string,
  params: Readonly<Record<string, string | number>> = {},
): string {
  return template.replace(/\{(\w+)\}/g, (match, name: string) =>
    name in params ? String(params[name]) : match,
  );
}

/**
 * 读取构建期写入的组件文案。站点未写入时返回空表，组件照常渲染缺数据提示，
 * 空标题会直接暴露构建问题。
 */
export function useGeneratedLabels(): {
  labels: ComputedRef<Record<string, string>>;
  label: (
    key: string,
    params?: Readonly<Record<string, string | number>>,
  ) => string;
} {
  const { site } = useData();
  const labels = computed<Record<string, string>>(() => {
    const config = (site.value.themeConfig ?? {}) as {
      akari?: { generated?: BundledGeneratedData };
    };
    const value = config.akari?.generated?.labels;
    return value && typeof value === "object" ? value : {};
  });

  function label(
    key: string,
    params?: Readonly<Record<string, string | number>>,
  ): string {
    return formatGeneratedLabel(labels.value[key] ?? "", params);
  }

  return { labels, label };
}

/** 能力项的文案键，如 `support_image` 对应 `gen_feature_image`。 */
export function featureLabelKey(feature: string): string {
  const name = feature.startsWith("support_")
    ? feature.slice("support_".length)
    : feature;
  return `gen_feature_${name}`;
}

/** 文案未覆盖时使用的能力名称。 */
export function featureName(feature: string): string {
  return feature.startsWith("support_")
    ? feature.slice("support_".length)
    : feature;
}

/** 生成数据中单个包的事实。 */
export interface BundledPackageEntry {
  facts?: {
    config?: BundledConfigTable[];
    features?: Record<string, boolean>;
  };
}

/** 生成数据中一列配置字段。 */
export interface BundledConfigField {
  name: string;
  type: string;
  default?: unknown;
  secret?: boolean;
  comment?: string;
  required?: boolean;
}

/** 生成数据中的一张配置表。 */
export interface BundledConfigTable {
  table: string;
  file?: string;
  secret?: boolean;
  fields?: BundledConfigField[];
}

/** 生成数据中的一条命令。 */
export interface BundledCliCommand {
  usage?: string;
  summary?: string;
  arguments?: { name: string; required?: boolean }[];
  options?: {
    names?: string[];
    metavar?: string;
    help?: string;
    isFlag?: boolean;
    required?: boolean;
  }[];
}
