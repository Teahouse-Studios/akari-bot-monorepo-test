from akaribot.core.api import wiki_allowlist_url_default, on_module_config


@on_module_config("wiki")
class WikiConfig:
    wiki_allowlist_url: str = wiki_allowlist_url_default
