from django.db import models

from base.error import Error
from base.response import Ret


def md5_hash(string):
    import hashlib
    md5 = hashlib.md5()
    md5.update(string.encode())
    return md5.hexdigest()


class User(models.Model):
    L = {
        'username': 32,
        'password': 32,
    }

    username = models.CharField(
        max_length=L['username'],
        unique=True,
    )

    password = models.CharField(
        max_length=L['password'],
    )

    def __str__(self):
        return str(self.id)+' - '+self.username

    @classmethod
    def create(cls, username, raw_pass):
        # check if the username exist
        ret = User.get_user_by_username(username)
        if ret.error is Error.OK:
            return Ret(Error.EXIST_USERNAME)

        try:
            o_user = cls(
                username=username,
                password=md5_hash(raw_pass),
            )
            o_user.save()
        except ValueError as err:
            return Ret(Error.ERROR_CREATE_USER)
        return Ret(Error.OK, o_user)

    @staticmethod
    def authenticate(username, password):
        ret = User.get_user_by_username(username)
        if ret.error is not Error.OK:
            return Ret(ret.error)

        o_user = ret.body
        if o_user.password != md5_hash(password):
            return Ret(Error.WRONG_PASSWORD)
        return Ret(Error.OK, o_user)

    @staticmethod
    def get_user_by_username(username):
        try:
            o_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Ret(Error.USER_NOT_EXIST)
        return Ret(Error.OK, o_user)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            o_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Ret(Error.USER_NOT_EXIST)
        return Ret(Error.OK, o_user)

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
        )
