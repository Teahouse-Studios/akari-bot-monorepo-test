from akaribot.core.constants import Info

platform_name = "QQ"
client_name = Info.resolve_client_name(platform_name)

sender_prefix = client_name
sender_prefix_list = [sender_prefix]

target_group_prefix = f"{client_name}|Group"
target_private_prefix = f"{client_name}|Private"
target_prefix_list = [target_group_prefix, target_private_prefix]
