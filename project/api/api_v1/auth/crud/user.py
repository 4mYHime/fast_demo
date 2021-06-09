class CRUDUser:

    @staticmethod
    def check_password(*, password: str, salt: str = None, hashed_password: str = None) -> bool:
        import hashlib

        sha1 = hashlib.sha1()
        sha1.update((password + salt).encode('utf-8'))
        return True if sha1.hexdigest() == hashed_password else False


curd_user = CRUDUser()
