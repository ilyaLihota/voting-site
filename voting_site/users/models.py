import base64
import random
import string
import urllib

from django.core.signing import Signer

from django.contrib.auth.models import AbstractUser
from django.db import models


ALPHABET = (string.digits + string.ascii_letters + string.punctuation) * 70


# Create your models here.
class User(AbstractUser):
    signer = Signer()

    email_verification_link = models.CharField(
        null=True,
        max_length=1024,
    )
    is_email_verified = models.BooleanField(default=False)
    verification_email_sent_at = models.DateTimeField(null=True)
    incorrect_attempts = models.PositiveSmallIntegerField(default=0)
    initial_secret_key = models.CharField(max_length=256)

    age = models.PositiveSmallIntegerField(default=0)
    gender = models.CharField(max_length=10)

    def generate_key(self):
        key = "".join(
            random.sample(ALPHABET, 256)
        )
        self.initial_secret_key = key
        self.save()

        signed_key = self.signer.sign(key)
        print(signed_key)
        encoded_key = base64.b64encode(bytes(signed_key, encoding='ascii')).decode('utf-8')
        return encoded_key

    def verify_email(self):
        encoded_key = self.generate_key()
        url = "http://127.0.0.1:8000/verify?key={}".format(
            urllib.parse.quote(encoded_key)
        )
        self.email_user(
            "Verification link",
            "<a href={}>Подтвердить почтовый адрес</a>".format(url),
            "admin@polls.com"
        )

    def check_key(self, key):
        signed_key = base64.b64decode(key).decode('utf-8')
        print(signed_key)
        initial_key = self.signer.unsign(signed_key)
        return self.initial_secret_key == initial_key
