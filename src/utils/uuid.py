import uuid

def is_valid_uuid(val):
    try:
        uuid_obj = uuid.UUID(val, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == val