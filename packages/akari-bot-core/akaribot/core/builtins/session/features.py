"""会话功能特性模块，定义消息会话支持的各项功能特性。"""

from attrs import define


@define
class Features:
    """会话功能特性类。"""

    support_image: bool = False

    support_audio: bool = False

    support_video: bool = False

    support_mention: bool = False

    support_embed: bool = False

    support_card: bool = False

    support_delete: bool = False

    support_manage: bool = False

    support_permission_group: bool = False

    support_markdown: bool = False

    # Markdown 扩展支持，指示会话是否支持渲染表格、代码块与 LaTeX 等内容。
    support_markdown_extension: bool = False

    support_reaction: bool = False

    support_quote: bool = False

    support_rss: bool = False

    support_typing: bool = False

    support_wait: bool = False

    # 处理消息节点支持，指示会话是否具备独立处理消息节点的能力。
    support_handle_message_nodes: bool = False

    support_private_msg: bool = False

    support_action_text: bool = False

    support_button: bool = False

    support_markdown_toggle: bool = False

    use_url_md_format: bool = False

    use_url_manager: bool = False

    use_running_mention: bool = True

    require_check_dirty_words: bool = False

    require_enable_modules: bool = True

    read_all_messages: bool = True

    @classmethod
    def override(cls, **kwargs) -> "Features":
        """创建新的 Features 实例，并根据提供的关键字参数覆盖默认值。"""
        return cls(**kwargs)
