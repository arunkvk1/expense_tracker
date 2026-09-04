from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "description", "amount", "date")
    list_filter = ("type", "date", "user")
    search_fields = ("description",)
