import uuid
import boto3

from django.conf import settings
from django.db import models
from django.urls import reverse


from project.users.models import User


class Location(models.Model):
    unique_link = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    found = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)\


    @classmethod
    def create(cls, phone):
        new_location = cls()
        new_location.phone = phone
        new_location.save()
        return new_location

    def get_poll_url(self):
        return reverse('location:poll', args=[self.unique_link])

    def request_location(self, host):
        client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1"
        )

        client.publish(
            PhoneNumber=self.phone,
            Message=host + reverse('location:get', args=[self.unique_link])
        )

        print('SEND TEXT TO: ' + self.phone)
        # Send Twillio Text Message
        return self.unique_link




