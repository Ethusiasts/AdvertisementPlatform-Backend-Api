from app.models.user_models import User

roles = ["ADMIN", "CUSTOMER", "EMPLOYEE", "LANDOWNER"]


def valid_role(role):
    if role.isalpha() and role.upper() in roles:
        return True
    return False


def find_role(role):
    for r in roles:
        if r == role.upper():
            return r
