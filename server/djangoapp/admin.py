from django.contrib import admin
# from .models import related models
from .models import CarMake,CarModel



class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'Name', "Dealerid", "Type", "Year", )

class CarMakeAdmin(admin.ModelAdmin):
    inlines=[CarModelInline]
    list_display=("Name", "Description")

admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)
