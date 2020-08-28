from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('parse/', views.parse_data, name='parse_data'),
    #path('all', views.AvitoList.as_view(), name='all_list'),
    #path('all/', views.all_ads, name='all_list'),
    path('all/', views.AvitoListView.as_view(), name='all_list'),

    path('new/', views.new_ads, name='new_ads'),
    path('deltas/', views.deltas_ads, name='deltas'),
    path('analyze/', views.analyze_methods, name='analyze'),
    path('autoparse/', views.auto_parse, name='autoparse')

]