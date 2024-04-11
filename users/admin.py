from .models import Customer, User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

admin.site.register(Customer)


User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['email', 'id', 'is_admin', 'is_staff','is_seller','is_customer']
    list_filter = ['is_active','is_admin', 'is_staff','is_seller','is_customer']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_admin','is_seller','is_customer', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ['email']
    ordering = ['email']


admin.site.register(User, CustomUserAdmin)
