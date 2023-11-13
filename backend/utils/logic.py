import bcrypt


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def same_uuids(uuid1, uuid2):
    return str(uuid1).strip() == str(uuid2).strip()


if __name__ == '__main__':
    p = input().strip()
    print(hash_password(p))
