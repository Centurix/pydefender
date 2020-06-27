from .card_manager import CardManager


sdcard = CardManager("/sd")


__all__ = [
    "sdcard"
]
