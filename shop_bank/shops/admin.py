from django.contrib import admin

from .models import City, Street, Shop


class AdminCity(admin.ModelAdmin):
    list_display = ('pk', 'name')


class AdminStreet(admin.ModelAdmin):
    list_display = ('pk', 'name', 'city')
    list_filter = ('city',)


class AdminShop(admin.ModelAdmin):
    list_display = ('pk', 'name', 'city', 'street', 'house_number',
                    'time_open', 'time_close')


admin.site.register(City, AdminCity)
admin.site.register(Street, AdminStreet)
admin.site.register(Shop, AdminShop)
