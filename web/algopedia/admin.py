from django.contrib import admin
from algopedia.models import Algo, AlgoVersion, Implementation, Language, Category, Star, Notebook

class AlgoAdmin(admin.ModelAdmin):
    list_display = ['name']


class ImplementationAdmin(admin.ModelAdmin):
    list_display = ['algo', 'user', 'lang', 'date', 'visible']

class StarAdmin(admin.ModelAdmin):
    list_display = ['user', 'implementation', 'active']


admin.site.register(Algo, AlgoAdmin)
admin.site.register(AlgoVersion)
admin.site.register(Implementation, ImplementationAdmin)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Star, StarAdmin)
admin.site.register(Notebook)
