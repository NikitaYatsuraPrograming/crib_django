from datetime import datetime
from os.path import splitext

from django.db import models
from django.core import validators
from .validators import validate_even
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товары',
                             # Валидатор по регулярному выражению
                             validators=[validators.RegexValidator(regex='[a-zA-Z0-9А-Яа-я_]')],
                             error_messages={
                                 'invalid': 'Неправильное название товара',
                             })
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', validators=[validate_even])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    def title_and_price(self):
        if self.price:
            return f'{self.title} {self.price}'
        else:
            return self.title

    # Валидатор формы взят с книги(лучще было сделать в валидаторе в методе)
    def clean(self):
        errors = {}
        # errors[NON_FIELD_ERRORS] = ValidationError('Ощибка в моделе')  # Сообщение о ошибке во всей моделе
        if not self.content:
            errors['content'] = ValidationError('Укажите неотрицательную цену')
        if errors:
            raise ValidationError(errors)

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


class Spare(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    spares = models.ManyToManyField(Spare,
                                    through='Kit'
                                    )  # Для вызова на странице используем цикл типа obj.spares.all()

    def __str__(self):
        return self.name


# Класс для связи многое со многим и еще количества этих деталей
class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.machine.name


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


class Img(models.Model):
    img = models.ImageField(verbose_name='Изображение',
                            upload_to=get_timestamp_path)
    desc = models.TextField()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class SpareTest(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class MachineTest(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    spares = models.ManyToManyField(SpareTest)  # Для вызова на странице используем цикл типа obj.spares.all()

    def __str__(self):
        return self.name

# Реализовать подрубрики рубрики типа (Машина - Мерседес)
