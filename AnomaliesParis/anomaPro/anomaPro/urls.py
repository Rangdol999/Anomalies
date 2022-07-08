"""anomaPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("question1/", views.question1, name="question1"),
    path("question1/<int:pk>/", views.Q1_ParAnnée, name="Q1_ParAnnée"),
    path("question1/<int:pk>/<str:type>/", views.Q1_ParAnnée, name="Q1_ParAnnée"),
    path("question2/", views.question2, name="question2"),
    path("question2/<str:mois>/", views.Q2_ParMois, name="Q2_ParMois"),
    #path("question2/<int:pk>/<str:type>/", views.Q1_ParArrondissement, name="Q1_ParArrondissement"),
    path("question3/", views.question3, name="question3"),
    path("question3/<int:arr>", views.Q3_ParArr, name="Q3_ParArr"),
    path('admin/', admin.site.urls),
]