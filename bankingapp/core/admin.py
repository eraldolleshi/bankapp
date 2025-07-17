from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BankAccount, DebitCard, Transaction

class BankerUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role='BANKER')

    def save_model(self, request, obj, form, change):
        obj.role = 'BANKER'
        super().save_model(request, obj, form, change)

admin.site.register(User, BankerUserAdmin)