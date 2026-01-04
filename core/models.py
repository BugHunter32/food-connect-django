# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'donor'),
      (2, 'ngo'),
      (3, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    organization_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    # These solve the related_name clash
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=('The groups this user belongs to.'),
        related_name="core_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions_set",
        related_query_name="user",
    )

class Donation(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('delivered', 'Delivered'),
    )
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    food_description = models.TextField()
    quantity = models.CharField(max_length=100, help_text="e.g., 'Feeds 20 people', '15kg of rice'")
    pickup_location = models.TextField()
    pickup_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_donations')

    def __str__(self):
        return f"Donation by {self.donor.organization_name}"

    class Meta:
        ordering = ['pickup_time']