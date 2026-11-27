from datetime import datetime


def check_svg(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:  # skipcq
            check = file.read(1024)
            return "<svg" in check
    except Exception:
        return False


def strptime2ts(date_string):
    """把日期字符串转换为时间戳。"""
    return datetime.fromisoformat(date_string).timestamp()
