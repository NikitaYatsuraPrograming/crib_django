from django.core import validators
from django.forms import ModelForm
from django import forms

from .models import Bb, Rubric, Img
# Создание формы в виде фабрики
from django.forms.widgets import Select
from django.forms import modelform_factory, DecimalField
from captcha.fields import CaptchaField


BbFormFactory = modelform_factory(Bb,
                                  fields=('title', 'content', 'price', 'rubric'),
                                  labels={'title': 'Название товара'},
                                  help_texts={'rubric': 'Не забудьте выбрать рубрику'},
                                  field_classes={'price': DecimalField},
                                  widgets={'rubric': Select(attrs={'size': 8})}
                                  )


# Создание в виде класса(быстрое объявление)
class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}
        help_texts = {'rubric': 'Не забудьте выбрать рубрику'}
        field_classes = {'price': DecimalField}
        widgets = {'rubric': Select(attrs={'size': 8})}


# Создания форм путем полного объявления(самый сложный способ)
class BbFormFull(forms.ModelForm):
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea()
                              )
    price = forms.DecimalField(label='Цена',
                               decimal_places=2
                               )
    rubrics = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                     label='Рубкика',
                                     help_text='Не забудьте выбрать рубрику',
                                     # widget=forms.widgets.Select(attrs={'size': 8}),
                                     empty_label='Не выбрано'
                                     )
    captcha = CaptchaField()

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        # Можно некоторые обьявить в верху, а те что не требуют изменений в мете как в способе быстрого объявления


# Форма для работы с загрузкой изображений
class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Загрузить изображение',
                           validators=[validators.FileExtensionValidator(
                               allowed_extensions=('gif', 'jpg', 'png')
                           )],
                           error_messages={'invalid': 'Этот формат файлов не поддерживается'})
    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'
