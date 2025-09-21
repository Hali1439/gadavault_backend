# apps/products/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Artisan(models.Model):
    """
    Legacy artisan profile (small makers not yet onboarded as full designers).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=128, blank=True)
    profile_image = models.URLField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 🔑 Ownership relations
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        help_text="The account that technically owns this product (billing, payouts)."
    )
    designer = models.ForeignKey(
      "designers.DesignerProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        help_text="The creative designer associated with this product."
    )
    artisan = models.ForeignKey(
        Artisan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        help_text="Optional small-scale artisan (non-designer) linked to the product."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    # === core product fields ===
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    attributes = models.JSONField(default=dict, blank=True)   # e.g. {size, material}
    images = models.JSONField(default=list, blank=True)        # list of {url, alt, order}

    # === provenance & storytelling ===
    provenance = models.JSONField(default=dict, blank=True)   # {ipfs_hash, signature, tx_id}
    story_markdown = models.TextField(blank=True)
    origin_region = models.CharField(max_length=128, blank=True)

    royalty_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["category", "price", "created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.id})"
