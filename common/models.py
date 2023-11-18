from datetime import datetime
from django.db import models
from django.db.models.deletion import Collector

from common.managers import SoftDeletionManager
from common.utils import manage_delete_dependency
from common.constants import DEFAULT_SINGLETON_INSTANCE_ID
from users.models import User


# Base model for adding timestamp fields (created_at, updated_at) to other models
class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Base model for adding created_by, updated_by field to other models
class CreatedByUpdatedBy(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated', null=True,
                                   blank=True)

    class Meta:
        abstract = True


# Base model for implementing soft delete functionality
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_deleted', null=True,
                                   blank=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(non_deleted_only=False)

    class Meta:
        abstract = True

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
        super(SoftDeleteModel, self).delete()


class BaseModel(TimestampModel, CreatedByUpdatedBy, SoftDeleteModel):
    """
    Abstract base model that includes timestamp, created/updated by, and soft delete functionality.
    """
    class Meta:
        abstract = True


class SingletonModel(models.Model):
    # Singleton instance ID field
    singleton_instance_id = DEFAULT_SINGLETON_INSTANCE_ID

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Ensure the primary key is always set to the singleton instance ID
        self.pk = self.singleton_instance_id
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Disable the delete method to prevent deletion of the singleton instance
        pass

    @classmethod
    def load(cls):
        # Retrieve or create the singleton instance
        obj, created = cls.objects.get_or_create(pk=cls.singleton_instance_id)
        return obj


class SiteConfiguration(SingletonModel, TimestampModel, CreatedByUpdatedBy):
    # Boolean field to determine whether to bypass API permissions
    bypass_api_permissions = models.BooleanField(default=True)

    # Fields to store minimum and latest versions for Android and iOS
    min_android_version = models.CharField(max_length=20, default="0.0.0")
    min_ios_version = models.CharField(max_length=20, default="0.0.0")
    latest_android_version = models.CharField(max_length=20, default="0.0.0")
    latest_ios_version = models.CharField(max_length=20, default="0.0.0")

    def __str__(self):
        # String representation of the model
        return "Site Configuration"

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configurations'
