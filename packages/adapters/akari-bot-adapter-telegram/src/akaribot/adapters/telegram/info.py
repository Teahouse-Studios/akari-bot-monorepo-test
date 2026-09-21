from core.constants import Info

platform_name = "Telegram"
client_name = Info.resolve_client_name(platform_name)

sender_prefix = f"{client_name}|User"
sender_prefix_list = [sender_prefix]

target_prefix = client_name
target_prefix_list = [
    f"{client_name}|Private",
    f"{client_name}|Group",
    f"{client_name}|Supergroup",
    f"{client_name}|Channel",
]
