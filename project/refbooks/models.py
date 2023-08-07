from django.db import models


class Refbook(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Идентификатор")
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class RefbookVersion(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Идентификатор")
    refbook = models.ForeignKey(Refbook, on_delete=models.CASCADE, verbose_name="Справочник")
    version = models.CharField(max_length=50, verbose_name="Версия")
    date = models.DateField(verbose_name="Дата начала действия")

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        unique_together = (('refbook_id', 'version'), ('refbook_id', 'date'))


class RefbookElement(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Идентификатор")
    version = models.ForeignKey(RefbookVersion, on_delete=models.CASCADE, verbose_name="Версия")
    code = models.CharField(max_length=100, verbose_name="Код элемента")
    value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"
        unique_together = (('version_id', 'code'),)
