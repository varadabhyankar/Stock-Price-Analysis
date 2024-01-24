# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('company_details/', views.company_details, name='company_details'),
    path('company_details/plot_graph/', views.plot_graph, name='plot_graph'),
]