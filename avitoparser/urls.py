"""avitoparser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from my_parser import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('work/', include('my_parser.urls')),
    path('admin/', admin.site.urls),
    #path("all/", views.AvitoListView.as_view()),

    #############
    path('', views.index, name='home'),
    path('work/parse/', views.parse_data, name='parse_data'),
    path('work/all/', views.AvitoListView.as_view(), name='all_list'),

    path('work/new/', views.AvitoNewListView.as_view(), name='new-ads'),

    path('work/deltas/', views.AvitoChangeListView.as_view(), name='deltas'),

    path('work/autoparse/', views.auto_parse, name='autoparse'),
    path('work/settings/', views.show_settings, name='showsettings'),

              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
