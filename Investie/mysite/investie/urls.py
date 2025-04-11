from django.urls import path, include

from . import views

urlpatterns = [
    path('get_live_price/', views.get_live_price, name='get_live_price'),
    path('', views.index, name="index"),
    path('b', views.entry_view, name='get_entry_view'),
path('watchlist/<int:id>/', views.view_watchlist, name='view_watchlist'),
]
