from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView

from django.views.decorators.cache import cache_page

from .views import index, by_rubric, BbCreateView, BbDetailView, BbDeleteView, add, api_rubrics, api_rubric_detail

app_name = 'bboard'  # Имя для пространства имен(если существует приложения где name='' повторется)

urlpatterns = [
    path('api/rubric/<int:pk>/', api_rubric_detail),
    path('api/rubrics/', api_rubrics, name='api_rubrics'),
    path('add/img/', add, name='add_img'),
    # Переход если замена пароля успешна
    path('account/reset/done',
         PasswordResetCompleteView.as_view(
             template_name='registration/confirm_password.html'
         ),
         name='password_reset_complete'
         ),
    # Замена пароля (этот адресс передается на почту при востановлении)
    path('account/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='registration/confirm_password.html'
         ),
         name='password_reset_confirm'
         ),
    # Письмо об замене пароля отправленно успешно
    path('account/password_reset/done', PasswordResetView.as_view(
        template_name='registration/email_sent.html'), name='password_reset_done'),
    # Адресс востановления пароля
    path('account/password_reset', PasswordResetView.as_view(
        template_name='registration/reset_password.html',
        subject_template_name='registration/reset_password.txt',
        email_template_name='registration/reset_email.html'
        ), name='password_reset'),
    # Установка пароля выполнена успешно
    path('account/password_change/done', PasswordChangeDoneView.as_view(
        template_name='registration/change_password.html'),
        name='password_change_done'),
    # Адресс для установки пароля
    path('account/password_change', PasswordChangeView.as_view(
        template_name='registration/change_password.html'),
        name='password_change'),
    # Выход
    path('account/logout', LogoutView.as_view(), name='logout'),
    # Вход
    path('account/login', LoginView.as_view(), name='login'),
    path('remove/<int:pk>/', BbDeleteView.as_view(), name='remove'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/', BbCreateView.as_view(), name='add'),  # Декоратор добавляет функционал cache_page(60 * 5)(
                                                       # кэша для этой страницы на 5 мин
    # path('<str:rubric_name>/', BbRubricView.as_view(), name='by_rubric'),
    path('<str:rubric_name>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
]
