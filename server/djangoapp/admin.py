from django.contrib import admin
from .models import CarMake, CarModel


# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


# CarModelAdmin class
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')
    list_filter = ('type', 'year', 'car_make')
    search_fields = ('name',)


# CarMakeAdmin class with CarModelInline
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CarModelInline]
