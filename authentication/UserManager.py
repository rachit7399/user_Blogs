from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):


    def create_user(self, uid, email, password=None):
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.uid = uid
        user.save()
        return user   

    def create_superuser(self, uid, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(uid, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user 