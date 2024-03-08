from flask import Flask, request, abort
from flask_principal import Principal, RoleNeed, Permission
from functools import wraps

# Определите роли (пример: администратор, звичайний користувач)
admin_role = RoleNeed('admin')
user_role = RoleNeed('user')

# Створіть розрішення (прив'язку ролей до URL)
admin_permission = Permission(admin_role)
user_permission = Permission(user_role)


def require_default_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not admin_permission.can() and not user_permission.can():
            abort(403)  # Ошибка "Доступ заборонено"
        return f(*args, **kwargs)
    return decorated_function