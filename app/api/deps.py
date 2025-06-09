from fastapi import Depends

def get_settings():
    from app.core import config
    return config