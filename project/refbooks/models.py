from django.db import models


def generate_CharAutoField(_model):
    """
    Функция для генерации строкового порядкового ID
    :param _model: Модель объекта
    :return: (str) - ID
    """
    #
    last_obj = _model.objects.all().order_by('id').last()
    return str(int(0 if not last_obj else last_obj.id) + 1)


class Refbook(models.Model):
    """
    Модель справочника
    """
    id = models.CharField(primary_key=True, max_length=255, verbose_name="Идентификатор")
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return f'Код: {self.code}. "{self.name}"'

    def save(self, *args, **kwargs):
        self.id = generate_CharAutoField(Refbook)
        super().save(*args, **kwargs)


class RefbookVersion(models.Model):
    """
    Модель версии справочника
    """
    id = models.CharField(primary_key=True, max_length=255, verbose_name="Идентификатор")
    refbook = models.ForeignKey(Refbook, on_delete=models.CASCADE, verbose_name="Справочник")
    version = models.CharField(max_length=50, verbose_name="Версия")
    date = models.DateField(verbose_name="Дата начала действия")

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        unique_together = (('refbook_id', 'version'), ('refbook_id', 'date'))

    def __str__(self):
        return f"{self.version}"

    def save(self, *args, **kwargs):
        self.id = generate_CharAutoField(RefbookVersion)
        super().save(*args, **kwargs)


class RefbookElement(models.Model):
    """
    Модель элемента справочника
    """
    id = models.CharField(primary_key=True, max_length=255, verbose_name="Идентификатор")
    version = models.ForeignKey(RefbookVersion, on_delete=models.CASCADE, verbose_name="Версия")
    code = models.CharField(max_length=100, verbose_name="Код элемента")
    value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"
        unique_together = (('version_id', 'code'),)

    def save(self, *args, **kwargs):
        self.id = generate_CharAutoField(RefbookElement)
        super().save(*args, **kwargs)
