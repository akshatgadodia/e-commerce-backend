from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import City
from users.models.user import User
from common.models import TimestampModel, CreatedByUpdatedBy, SoftDeleteModel


class UserAddresses(TimestampModel, SoftDeleteModel):
    # ForeignKey to the User model, specifying that if the referenced user is deleted,
    # also delete the user addresses associated with it
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Text field to store the address information
    address = models.TextField()
    # ForeignKey to the City model with DO_NOTHING on delete. Consider the implications
    # of not cascading delete actions to the related city.
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    # CharField to store the zip code information
    zip_code = models.CharField(max_length=10)
    # CharField to store the name information
    name = models.CharField(max_length=255)
    # CharField to store the mobile number information
    mobile = models.CharField(max_length=20)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'

    def __str__(self):
        # String representation of the user address, using the name field
        return self.name
