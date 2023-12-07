from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import Collector

from users.managers import UserManager
from common.utils import manage_delete_dependency


# Override Base User
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    date_joined = None
    email = models.EmailField(unique=True, error_messages={'unique': 'This email already exists'})
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    image = models.ImageField()
    password_reset_key = models.IntegerField(null=True)
    password_reset_key_generated_on = models.DateTimeField(null=True)
    forced_logout_time = models.DateTimeField(null=True, blank=True)

    # TimeStamp Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft Delete
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='%(class)s_deleted', null=True,
                                   blank=True)

    objects = UserManager()
    all_objects = UserManager(non_deleted_only=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'date_of_birth']

    class Meta:
        ordering = ('name',)

    def delete(self, user=None):
        """
        Soft deletes the object and its dependencies.

        Args:
            user: The user initiating the deletion (optional).
        """
        # Use a collector to gather related objects for deletion
        collector = Collector(using='default')
        collector.collect([self], keep_parents=False)

        # Manage dependencies and mark objects for deletion
        manage_delete_dependency(collector, user)

        # Set 'deleted_at' attribute to mark soft deletion
        self.deleted_at = datetime.utcnow()
        self.save()

    def hard_delete(self):
        """
        Hard deletes (permanently removes) the object.
        """
        super(User, self).delete()

    def __str__(self) -> str:
        """
        Returns String Representation of User Model
        """
        return f"{self.name}"
