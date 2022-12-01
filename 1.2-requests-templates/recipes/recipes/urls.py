"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#from django.urls import path

from django.contrib import admin
from django.urls import path, include

from calculator.views import home_view, omlet_view, pasta_view, buter_view, hotdog_view

urlpatterns = [
    # здесь зарегистрируйте вашу view-функцию
    path("", home_view, name='home'),
    path('omlet/', omlet_view, name='omlet'),
    path('pasta/', pasta_view, name='pasta'),
    path('buter/', buter_view, name='buter'),
    path('hotdog/', hotdog_view, name='hotdog'),

]
