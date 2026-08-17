from typing import Dict


COLORS: Dict[str, str] = {
    "BLACK": "\033[90m",
    "RED": "\033[91m",
    "SALMON": "\033[118m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "ORANGE": "\033[38;5;208m",
    "PURPLE": "\033[38;5;141m",
    "PINK": "\033[38;5;213m",
    "TEAL": "\033[38;5;43m",
    "GOLD": "\033[38;5;220m"
}

RESET = "\033[0m"

STYLE: Dict[str, str] = {
    "BOLD": "\033[1m",
    "DIM": "\033[2m",
    "UNDERLINE": "\033[4m",
    "BLINK": "\033[5m",
    "REVERSE": "\033[7m",
    "RESET": "\033[0m"
}
