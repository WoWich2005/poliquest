from django.utils import timezone

from django.db import models


class Point(models.Model):
    name = models.CharField('Название точки', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Точка"
        verbose_name_plural = "Точки"


class Team(models.Model):
    name = models.CharField('Название команды', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class TeamPoints(models.Model):
    number = models.PositiveIntegerField('Номер точки назначения команды')

    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    point = models.ForeignKey(Point, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Точка команды"
        verbose_name_plural = "Точки команд"

    def __str__(self):
        obj_name = "Команда {team}. Точка №{number}. Имя точки: {point}"
        return obj_name.format(team=self.team, number=self.number, point=self.point)


class Stat(models.Model):
    ARRIVAL_TYPE = 1
    START_QUEST_TYPE = 2
    FINISH_QUEST_TYPE = 3

    STAT_TYPE_CHOICES = (
        (ARRIVAL_TYPE, 'Прибытие команды на точку'),
        (START_QUEST_TYPE, 'Старт квеста командой'),
        (FINISH_QUEST_TYPE, 'Завершение квеста командой')
    )

    point = models.ForeignKey(Point, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    type = models.IntegerField('Действие', choices=STAT_TYPE_CHOICES, default=1)
    time = models.DateTimeField('Время действия')

    def save(self, *args, **kwargs):
        if not self.id:
            self.time = timezone.now()
        return super(Stat, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Запись статистики"
        verbose_name_plural = "Записи статистики"
