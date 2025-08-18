# models.py
import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image
from pathlib import Path


class Role(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Customer"
    MANAGER = "MANAGER", "Restaurant Manager"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})" #type:ignore



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto slugify, ensure global uniqueness
        if not self.slug:
            base = slugify(self.name)[:110]  # leave room for "-99"
            slug = base or "category"
            i = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to="products/", blank=True)
    stock = models.PositiveIntegerField(default=0)
    
    def _shrink_image(self, path, max_width=1200, quality=82):
        try:
            img = Image.open(path)
        except Exception:
            return  # not an image, or corrupt

        # Ensure RGB mode
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        # Resize if too wide
        w, h = img.size
        if w > max_width:
            ratio = max_width / w
            img = img.resize((max_width, int(h * ratio)), Image.Resampling.LANCZOS)

        # Overwrite the file with optimized version
        ext = os.path.splitext(path)[1].lower()
        if ext in (".jpg", ".jpeg"):
            img.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
        elif ext == ".png":
            img.save(path, "PNG", optimize=True)
        elif ext == ".webp":
            img.save(path, "WEBP", quality=quality, method=6)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "slug"], name="uniq_product_slug_per_category"
            ),
        ]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["category", "name"]),
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:150]
            slug = base or "product"
            i = 1
            qs = Product.objects.filter(category=self.category, slug=slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.exists():
                slug = f"{base}-{i}"
                i += 1
                qs = Product.objects.filter(category=self.category, slug=slug)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
            self.slug = slug
        super().save(*args, **kwargs)
        
class AddOn (TimeStampedModel):
        category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="addons"
    )
        name = models.CharField(max_length=150)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        is_active = models.BooleanField(default=True)
        
        
        def __str__(self):
            return self.name


class Address(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    full_name = models.CharField(max_length=120)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=60, default="Vietnam")
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_default", "created_at"]
        
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        user = self.user
        is_default = self.is_default
        super().delete(*args, **kwargs)

        if is_default:
            other = Address.objects.filter(user=user).first()
            if other and not other.is_default:
                other.is_default = True
                other.save()
        

    def __str__(self):
        return f"{self.full_name}, {self.line1}"
