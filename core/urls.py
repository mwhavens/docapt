from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('DOC', views.docSearch, name='docSearch'),
    path('SLOT', views.slot_search, name='slotSearch'),
]

