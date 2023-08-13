

def relation_validator(v):
    print("@@@@@@@@@@@@@@@-----------", type(v), v)
    if isinstance(v, str):
        return None
    return v