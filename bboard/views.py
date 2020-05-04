from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView # Создание функциональности формы
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Bb, Rubric
from .forms import BbForm, BbFormFull, ImgForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition


# Главнвя страница
from .serializers import RubricSerializer


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'bbs': page.object_list, 'rubrics': rubrics, 'page': page}

    # truncatewords - ограничение вывода слов в шаблоне

    return render(request, 'bboard/index.html', context)


# Вывод рубрик
# @cache_page(60 * 5)  # Декоратор добавляет функционал кэша для этой страницы на 5 мин
def by_rubric(request, rubric_name):
    current_rubric = Rubric.objects.get(name=rubric_name)  # Вывод текущей рубрики
    bbs = Bb.objects.filter(rubric=current_rubric.pk)  # Вывод только тех записей у которых связаны id
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


# Класс для рапботы с формой
class BbCreateView(CreateView):
    template_name = 'bboard/create.html'  # путь к шаблону
    form_class = BbFormFull  # Форма которая используется
    success_url = reverse_lazy('index')  # Адресс перенаправления в случае успеха

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# Сделать класс который будет работать по строковым ссылкам
def bb_lmf(request, pk):
    return Bb.objects.get(pk=pk).published


# @condition(last_modified_func=bb_lmf)  # Кэширование на стороне клиента
class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])

        return context


# Класс для обновления записей
class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'
    # template_name = 'bboard/исправленый шаблон на обновление'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()

        return context


# Класс для удаления записей
class BbDeleteView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'
    template_name = 'bboard/delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()

        return context


def add(request):
    test = request.FILES
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bboard:index')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'bboard/add.html', context)


# Простой вывод JSON(api от rest framework)
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return JsonResponse(serializer.data, safe=False)


# Красивый вывод с применениями
@api_view(['GET'])
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_rubric_detail(request, pk):
    if request.method == 'GET':
        rubric = Rubric.objects.get(pk=pk)
        serializer = RubricSerializer(rubric)
        return Response(serializer.data)
