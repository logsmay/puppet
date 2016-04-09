def from_bytes(payload, encoding='utf8'):
    return str(payload, encoding=encoding)

def to_bytes(payload, encoding='utf8'):
    return bytes(payload, encoding=encoding)