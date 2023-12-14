from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Post, Comment, CustomUser, Like
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
