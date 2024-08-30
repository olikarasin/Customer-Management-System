from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Credential

class CustomerBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            credential = Credential.objects.get(username=username)
            # Access the related User object via the Customer's user_profile
            user = credential.customer.user_profile.user
            if user.check_password(password):  # Use Django's check_password method
                return user
        except (Credential.DoesNotExist, AttributeError):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
