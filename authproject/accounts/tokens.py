from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include is_active so that once activated, any existing token becomes invalid
        return f"{user.pk}{user.is_active}{timestamp}"


account_activation_token = AccountActivationTokenGenerator()
