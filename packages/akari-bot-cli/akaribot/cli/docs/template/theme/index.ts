import DefaultTheme from "vitepress/theme"
import CommandUsage from "./components/CommandUsage.vue"
import ModuleMeta from "./components/ModuleMeta.vue"
import NoticeBox from "./components/NoticeBox.vue"
import "./custom.css"

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component("ModuleMeta", ModuleMeta)
    app.component("NoticeBox", NoticeBox)
    app.component("CommandUsage", CommandUsage)
  },
}
