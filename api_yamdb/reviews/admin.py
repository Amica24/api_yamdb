from django.contrib import admin

from .models import (
    Category, Comment, Genre,
    Review, Title, User
)


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Review)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name',
        'last_name', 'email',
        'role'
    )
