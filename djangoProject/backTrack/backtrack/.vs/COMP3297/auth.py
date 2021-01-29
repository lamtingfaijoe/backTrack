from django.contrib.auth.backends import ModelBackend
from COMP3297.models import Developer, Manager

class ManagerOrDeveloperBackTrack(ModelBackend):

    def authenticate(self, *args, **kwargs):
        return self.downcast_user_type(super().authenticate(*args, **kwargs))
        
    def get_user(self, *args, **kwargs):
        return self.downcast_user_type(super().get_user(*args, **kwargs))

    def downcast_user_type(self, user):
        try:
            developer = Developer.objects.get(pk=user.pk)
            return developer
        except:
            pass

        try:
            manager = Manager.objects.get(pk=user.pk)
            return manager
        except:
            pass

        return user