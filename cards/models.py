from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class VisitingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # ✅ Images
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # profile photo
    cover_photo = models.ImageField(upload_to='covers/', blank=True, null=True)  # new field for banner / cover
    
    slug = models.SlugField(unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def get_absolute_url(self):
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        return f"{site_url.rstrip('/')}/card/{self.slug}/"

    def save(self, *args, **kwargs):
        # create unique slug if missing
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while VisitingCard.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # First save to get ID and slug
        super().save(*args, **kwargs)

        # Generate QR code if missing
        if not self.qr_code:
            qr_img = qrcode.make(self.get_absolute_url())
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            file_name = f"qr_{self.slug}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
            buffer.close()
            super().save(update_fields=['qr_code'])
