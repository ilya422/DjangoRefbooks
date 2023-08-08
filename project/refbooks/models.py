from django.db import models


def __generate_id(_model):
    """
    Метод для генерации строкового порядкового ID
    """
    last_obj = _model.objects.all().order_by('id').last()
    return str(int(0 if not last_obj else last_obj.id) + 1)


def generate_id_Refbook():
    return __generate_id(Refbook)


def generate_id_RefbookVersion():
    return __generate_id(RefbookVersion)


def generate_id_RefbookElement():
    return __generate_id(RefbookElement)


class Refbook(models.Model):
    """
    Модель справочника
    """
    id = models.CharField(primary_key=True, max_length=255, default=generate_id_Refbook, editable=False, verbose_name="Идентификатор")
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return f'Код: {self.code}. "{self.name}"'


class RefbookVersion(models.Model):
    """
    Модель версии справочника
    """
    id = models.CharField(primary_key=True, max_length=255, default=generate_id_RefbookVersion, editable=False, verbose_name="Идентификатор")
    refbook = models.ForeignKey(Refbook, on_delete=models.CASCADE, verbose_name="Справочник")
    version = models.CharField(max_length=50, verbose_name="Версия")
    date = models.DateField(verbose_name="Дата начала действия")

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        unique_together = (('refbook_id', 'version'), ('refbook_id', 'date'))

    def __str__(self):
        return f"{self.version}"


class RefbookElement(models.Model):
    """
    Модель элемента справочника
    """
    id = models.CharField(primary_key=True, max_length=255, default=generate_id_RefbookElement, editable=False, verbose_name="Идентификатор")
    version = models.ForeignKey(RefbookVersion, on_delete=models.CASCADE, verbose_name="Версия")
    code = models.CharField(max_length=100, verbose_name="Код элемента")
    value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"
        unique_together = (('version_id', 'code'),)
