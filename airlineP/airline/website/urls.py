from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    #path('home/', views.exemple, name="pa"),
    #path('flights/', views.all_flights, name="flights_list"),
    path('flights/', views.exemple, name="pa"),
    path('flightsDirect/', views.exemple, name="pa"),
    path('flightsStop1/', views.exemple, name="pa"),
    path('flightsStop2/', views.exemple, name="pa"),
    path('admin/', admin.site.urls),
    path('', include("Home.urls")),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 




]
