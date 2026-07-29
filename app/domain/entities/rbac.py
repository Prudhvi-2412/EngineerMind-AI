from enum import Enum
from typing import Set


class Role(str, Enum):
    ADMIN = "ADMIN"
    ENGINEERING_MANAGER = "ENGINEERING_MANAGER"
    LEAD_ENGINEER = "LEAD_ENGINEER"
    ENGINEER = "ENGINEER"
    VIEWER = "VIEWER"


class Permission(str, Enum):
    ORG_MANAGE = "org:manage"
    USERS_READ = "users:read"
    USERS_WRITE = "users:write"
    USERS_DELETE = "users:delete"
    METRICS_READ = "metrics:read"
    DEPLOYMENTS_READ = "deployments:read"
    DEPLOYMENTS_TRIGGER = "deployments:trigger"
    INCIDENTS_READ = "incidents:read"
    INCIDENTS_WRITE = "incidents:write"


ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        Permission.ORG_MANAGE,
        Permission.USERS_READ,
        Permission.USERS_WRITE,
        Permission.USERS_DELETE,
        Permission.METRICS_READ,
        Permission.DEPLOYMENTS_READ,
        Permission.DEPLOYMENTS_TRIGGER,
        Permission.INCIDENTS_READ,
        Permission.INCIDENTS_WRITE,
    },
    Role.ENGINEERING_MANAGER: {
        Permission.USERS_READ,
        Permission.METRICS_READ,
        Permission.DEPLOYMENTS_READ,
        Permission.INCIDENTS_READ,
        Permission.INCIDENTS_WRITE,
    },
    Role.LEAD_ENGINEER: {
        Permission.USERS_READ,
        Permission.METRICS_READ,
        Permission.DEPLOYMENTS_READ,
        Permission.DEPLOYMENTS_TRIGGER,
        Permission.INCIDENTS_READ,
        Permission.INCIDENTS_WRITE,
    },
    Role.ENGINEER: {
        Permission.USERS_READ,
        Permission.METRICS_READ,
        Permission.DEPLOYMENTS_READ,
        Permission.INCIDENTS_READ,
    },
    Role.VIEWER: {
        Permission.USERS_READ,
        Permission.METRICS_READ,
    },
}


def has_permission(role: Role, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())
