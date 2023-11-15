from django.contrib import admin

from .models import City, Street, Shop


class AdminCity(admin.ModelAdmin):
    list_display = ('pk', 'name')


class AdminStreet(admin.ModelAdmin):
    list_display = ('pk', 'name', 'city')
    list_filter = ('city',)


class AdminShop(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_city', 'street', 'house_number',
                    'time_open', 'time_close')

    def get_city(self, obj):
        return obj
    get_city.short_description = 'Город'


admin.site.register(City, AdminCity)
admin.site.register(Street, AdminStreet)
admin.site.register(Shop, AdminShop)
