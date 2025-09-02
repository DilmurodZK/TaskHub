from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.utils import timezone

class Command(BaseCommand):
    help = "Remove expired tokens from the blacklist"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now)

        count = 0
        for token in expired_tokens:
            BlacklistedToken.objects.filter(token=token).delete()
            token.delete()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} expired tokens"))
