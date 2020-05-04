# Связь одно к одному
from django.db import models
from django.contrib.auth.models import User
from  django.contrib.contenttypes.fields import GenericForeignKey
from  django.contrib.contenttypes.models import ContentType


class AdvUser(models.Model):
    is_activate = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Связь один ко многим
class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товары')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявления'
        ordering = ['-published']


class Rubric(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубкики'
        verbose_name = 'Рубкика'
        ordering = ['name']


# Связь многое со многим
class Spare(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    spares = models.ManyToManyField(Spare,
                                    through='Kit',
                                    through_fields=('machine',' spare')
                                    )  # Для вызова на странице используем цикл типа obj.spares.all()


# Класс для связи многое со многим и еще количества этих деталей
class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


# Кдасс полиморфной связи (в этом случае создание заметок к моделям)
class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id')


# Класс для загрузки изображений
class Img(models.Model):
    img = models.ImageField(verbose_name='Изображение')
    desc = models.TextField()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
