# core/permissions.py

from functools import wraps
from core.acl import ACLManager
from core.models import Message

class PermissionError(Exception):
    pass

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, message: Message, *args, **kwargs):
            acl: ACLManager = self.acl
            has_perm = await acl.check(
                username=message.user,
                protocol=message.protocol,
                hostname=message.hostname,
                channel=message.channel,
                permission=permission
            )
            if not has_perm:
                raise PermissionError(f"Permission denied for {permission}")
            return await func(self, message, *args, **kwargs)
        return wrapper
    return decorator
