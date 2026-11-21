import DefaultTheme from "vitepress/theme"
import ChatExample from "./components/ChatExample.vue"
import CommandUsage from "./components/CommandUsage.vue"
import ModuleMeta from "./components/ModuleMeta.vue"
import NoticeBox from "./components/NoticeBox.vue"
import ApiCatalog from "./components/ApiCatalog.vue"
import PackageDependencies from "./components/PackageDependencies.vue"
import SupportedLanguages from "./components/SupportedLanguages.vue"
import "./custom.css"

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component("ModuleMeta", ModuleMeta)
    app.component("NoticeBox", NoticeBox)
    app.component("ApiCatalog", ApiCatalog)
    app.component("PackageDependencies", PackageDependencies)
    app.component("SupportedLanguages", SupportedLanguages)
    app.component("CommandUsage", CommandUsage)
    app.component("ChatExample", ChatExample)
  },
}
