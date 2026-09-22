from akaribot.core.constants import Info

platform_name = "Matrix"
client_name = Info.resolve_client_name(platform_name)

sender_prefix = client_name
sender_prefix_list = [sender_prefix]

target_prefix = f"{client_name}|Room"
target_prefix_list = [target_prefix]
