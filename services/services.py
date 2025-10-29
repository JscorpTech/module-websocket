from typing import Any
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_event(group: str, data: dict[str, Any]):
    return async_to_sync(get_channel_layer().group_send)(group, data)  # type: ignore
