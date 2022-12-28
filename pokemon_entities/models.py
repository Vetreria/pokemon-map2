from django.db import models  # noqa F401


class PokemonElement(models.Model):
    icon = models.ImageField(
        upload_to='images', null=True, blank=True, verbose_name="Иконка")
    title = models.CharField(
        max_length=200, verbose_name="Название по-русски")
    strong_against_type = models.ManyToManyField("self",
                                                 related_name="strong_againsts", null=True, blank=True, verbose_name="Силён против")

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200, verbose_name="Название по-русски")
    title_en = models.CharField(
        max_length=200, blank=True, verbose_name="Название по-английски")
    title_jp = models.CharField(
        max_length=200, blank=True, verbose_name="Название по-японски")
    photo = models.ImageField(
        upload_to='images', null=True, blank=True, verbose_name="Картинка")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание")
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name="next_evolutions",
                                           verbose_name="Из кого эволюционировал")
    elements = models.ManyToManyField(PokemonElement,
                                      related_name="elements", null=True, verbose_name="Стихии")

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                related_name="entities", null=True, verbose_name="Что за покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, verbose_name="Начало спауна")
    disappeared_at = models.DateTimeField(
        null=True, verbose_name="Конец спауна")
    level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    health = models.IntegerField(
        null=True, blank=True, verbose_name="Здоровье")
    strenght = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(
        null=True, blank=True, verbose_name="Выносливость")
