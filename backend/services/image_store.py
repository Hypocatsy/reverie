import base64
import uuid
from collections import OrderedDict

_MAX_ENTRIES = 50
_store: OrderedDict[str, bytes] = OrderedDict()


def save(b64_data: str) -> str:
    """Decode and store image bytes; return a UUID key."""
    image_bytes = base64.b64decode(b64_data)
    key = str(uuid.uuid4())
    _store[key] = image_bytes
    while len(_store) > _MAX_ENTRIES:
        _store.popitem(last=False)
    return key


def get(key: str) -> bytes | None:
    return _store.get(key)
