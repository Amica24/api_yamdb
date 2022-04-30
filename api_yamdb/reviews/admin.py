from django.contrib import admin

from .models import Categories, Genres, Titles, User


admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name',
        'last_name', 'email',
        'role'
    )
