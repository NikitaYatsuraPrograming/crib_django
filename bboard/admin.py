from django.contrib import admin
from .models import Bb, Rubric, Spare, Machine, Kit, Img, MachineTest, SpareTest


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'rubric', 'price', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


class MachineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('spares',)


class MaAdmin(admin.ModelAdmin):
    filter_horizontal = ('spares',)  # Создает табличку для перетаскивания выбраных рубрик


admin.site.register(Spare)
admin.site.register(SpareTest)
admin.site.register(Img)
admin.site.register(Kit)
admin.site.register(Machine, MachineAdmin)
admin.site.register(MachineTest, MaAdmin)
admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)

