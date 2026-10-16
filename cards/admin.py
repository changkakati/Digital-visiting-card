from django.contrib import admin
from .models import VisitingCard

@admin.register(VisitingCard)
class VisitingCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'email', 'slug')
    search_fields = ('name', 'user__username', 'email')
    readonly_fields = ('qr_code',)
