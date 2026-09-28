"""通用工具模块:日志、格式化、输入校验。"""

import sys
from datetime import datetime
from typing import Optional

# 日志级别颜色(CLI 终端 ANSI 转义)
_LEVEL_COLORS = {
    "INFO": "\033[36m",      # 青色
    "SUCCESS": "\033[32m",   # 绿色
    "WARNING": "\033[33m",   # 黄色
    "ERROR": "\033[31m",     # 红色
    "DEBUG": "\033[90m",     # 灰色
}
_RESET = "\033[0m"


def log(msg: str, level: str = "INFO") -> None:
    """统一日志输出,带时间戳和级别颜色。

    :param msg: 日志内容
    :param level: INFO / SUCCESS / WARNING / ERROR / DEBUG
    """
    color = _LEVEL_COLORS.get(level, "")
    ts = datetime.now().strftime("%H:%M:%S")
    # Windows 终端可能不支持 ANSI,检测后降级
    if sys.platform == "win32" and not _supports_ansi():
        print(f"[{ts}] [{level}] {msg}", flush=True)
    else:
        print(f"{color}[{ts}] [{level}]{_RESET} {msg}", flush=True)


def _supports_ansi() -> bool:
    """检测当前终端是否支持 ANSI 转义码。"""
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        return bool(kernel32.GetConsoleMode(kernel32.GetStdHandle(-11)) & 0x0004)
    except Exception:
        return False


APP_VERSION = "1.2.0"


def print_banner() -> None:
    """打印程序启动横幅。"""
    banner = (
        "\n" + "=" * 52 + "\n"
        f"        ICVE_Toolkit v{APP_VERSION}\n"
        "        SPOC / MOOC / 资源库刷课 + 签到改签\n"
        "        协议: PolyForm Noncommercial 1.0.0 (禁止商用)\n"
        "        收费代刷、引流变现均属商用,禁止\n"
        + "=" * 52
    )
    print(banner, flush=True)


def print_menu(items: list) -> None:
    """打印数字菜单。

    :param items: [(编号, 文本), ...] 或 [文本, ...]
    """
    print("\n" + "-" * 40, flush=True)
    for i, item in enumerate(items, 1):
        if isinstance(item, tuple):
            num, text = item
            print(f"  [{num}] {text}", flush=True)
        else:
            print(f"  [{i}] {item}", flush=True)
    print("-" * 40, flush=True)


def input_choice(prompt: str, valid: Optional[list] = None) -> str:
    """读取用户输入并可选校验。

    :param prompt: 提示文本
    :param valid: 合法值列表,为 None 则不校验
    :return: 用户输入(已 strip)
    """
    while True:
        choice = input(f"  {prompt}: ").strip()
        if valid is None or choice in valid:
            return choice
        print("  无效选择,请重试", flush=True)


def input_int(prompt: str, min_val: int = 0, max_val: Optional[int] = None) -> Optional[int]:
    """读取整数输入,返回 None 表示用户放弃。

    :param prompt: 提示文本
    :param min_val: 最小值(含)
    :param max_val: 最大值(含),None 不限
    :return: 整数或 None
    """
    while True:
        raw = input(f"  {prompt}: ").strip()
        if raw == "":
            return None
        if raw.isdigit():
            val = int(raw)
            if val >= min_val and (max_val is None or val <= max_val):
                return val
        print(f"  请输入 {min_val}~{max_val or '∞'} 之间的数字", flush=True)


def truncate(text: str, max_len: int = 40) -> str:
    """截断文本,超长加省略号。"""
    if not text:
        return ""
    return text[:max_len] + "..." if len(text) > max_len else text
