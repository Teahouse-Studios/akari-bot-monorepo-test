from akaribot.core.api import Info

platform_name = "Web"
client_name = Info.resolve_client_name(platform_name)

sender_prefix = client_name
sender_prefix_list = [sender_prefix]

target_prefix = f"{client_name}|Console"
target_prefix_list = [target_prefix]
