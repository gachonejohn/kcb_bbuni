# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stk_push/', views.stk_push, name='stk_push'),
    path('', views.stk_push_form, name='stk_push_form'),
    # path('token/', views.display_token, name='display_token'),
]