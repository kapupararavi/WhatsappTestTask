import sys
from django.core.management import BaseCommand
from django.contrib.auth.models import User

from wa_messages.models import APIToken


class Command(BaseCommand):
    help = 'Creates a new token for user to access the API endpoint'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('user_email', type=str)

    def handle(self, *args, **options):
        user_email = options['user_email']
        user = User.objects.filter(email=user_email).first()

        if user is None:
            print(f"User doesn't exists with email address: {user_email}")
            sys.exit(1)

        access_token, api_token_obj = APIToken.create_token(user=user)

        print("A token has been created successfully.")
        print("Access token:", access_token)
        print("API token identifier:", api_token_obj.token_id)
