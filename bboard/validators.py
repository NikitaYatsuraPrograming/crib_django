from django.core.exceptions import ValidationError


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s не четное', code='odd', params={'value': val})


class MinMaxValidator:
    def __init__(self, min_value, max_value):
        self.max_value = max_value
        self.min_value = min_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно находится в диапазоне от %(min)s до %(max)s',
                                  code='out_or_range',
                                  params={'min': self.min_value, 'max': self.max_value})
