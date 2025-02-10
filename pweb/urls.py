from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', include('home.urls')),  # Inclui as URLs do aplicativo 'home'
    path('admin/', admin.site.urls),  # URL para o admin do Django
    path('login/', LoginView.as_view(template_name='home/login.html'), name='login'),  # URL para a view de login com o template correto
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # URL para a view de logout com redirecionamento para a página de login
]
