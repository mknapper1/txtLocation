import uuid
import boto3
from django.db import models

from project.users.models import User


class Location(models.Model):
    unique_link = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    found = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def request_location(self):
        client = boto3.client(
            "sns",
            aws_access_key_id="your_access_key_id",
            aws_secret_access_key="you_secret_access_key",
            region_name="us-east-1"
        )

        # client.publish(
        #     PhoneNumber="your_phone_number",
        #     Message="Hello World!"
        # )

        print('SEND TEXT TO: ' + self.phone)
        # Send Twillio Text Message
        return self.unique_link




