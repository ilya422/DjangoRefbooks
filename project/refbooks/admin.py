from datetime import date
from django.contrib import admin

from .models import Refbook, RefbookVersion, RefbookElement


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    """
    Панель справочников
    """

    class VersionInline(admin.TabularInline):
        model = RefbookVersion

    inlines = (VersionInline,)

    def current_version(self, obj):
        current_version = RefbookVersion.objects.filter(refbook=obj, date__lte=date.today()).latest('date')
        return current_version.version

    current_version.short_description = 'Текущая версия'

    def current_version_date(self, obj):
        current_version = RefbookVersion.objects.filter(refbook=obj, date__lte=date.today()).latest('date')
        return current_version.date

    current_version_date.short_description = 'Дата начала действия версии'

    readonly_fields = ('id',)
    list_display = ('id', 'code', 'name', 'current_version', 'current_version_date')


@admin.register(RefbookVersion)
class RefbookVersionAdmin(admin.ModelAdmin):
    """
    Панель версии справочника
    """

    class RefbookElementInline(admin.TabularInline):
        model = RefbookElement

    inlines = (RefbookElementInline,)

    def refbook_code(self, obj):
        refbook = Refbook.objects.get(id=obj.refbook.id)
        return refbook.code

    refbook_code.short_description = 'Код справочника'

    def refbook_name(self, obj):
        refbook = Refbook.objects.get(id=obj.refbook.id)
        return refbook.name

    refbook_name.short_description = 'Наименование справочника'

    readonly_fields = ('id',)
    list_display = ('refbook_code', 'refbook_name', 'version', 'date')


@admin.register(RefbookElement)
class RefbookElementAdmin(admin.ModelAdmin):
    """
    Панель элементов справочника
    """
    readonly_fields = ('id',)
