from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index_usuario/', views.index_usuario, name='index_usuario'),
    path('criar_conta/', views.criar_conta, name='criar_conta'),
    path('extrato/', views.extrato_view, name='extrato'),
    path('transacao/', views.transacao, name='transacao'),
]
