from django.db import models


class Refbook(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=False)


class RefbookVersion(models.Model):
    id = models.AutoField(primary_key=True)
    refbook_id = models.ForeignKey(Refbook, on_delete=models.CASCADE)
    version = models.CharField(max_length=50)
    date = models.DateField()

    class Meta:
        unique_together = (('refbook_id', 'version'), ('refbook_id', 'date'))


class RefbookElement(models.Model):
    id = models.AutoField(primary_key=True)
    version_id = models.ForeignKey(RefbookVersion, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    value = models.CharField(max_length=300)

    class Meta:
        unique_together = (('version_id', 'code'),)
