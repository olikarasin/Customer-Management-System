from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Credential

class CustomerBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            credential = Credential.objects.get(username=username)
            # Directly compare plaintext password for now
            if credential.password == password:
                return credential.customer.user_profile.user  # Use user_profile to get the User object
        except (Credential.DoesNotExist, AttributeError):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
