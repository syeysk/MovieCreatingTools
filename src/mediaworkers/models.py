from django.db import models

class Sketch(models.Model):
    name = models.CharField('Название')
    # TODO: Добавить поля общих настроек?

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сценарий'
        verbose_name_plural = 'Сценарии'
