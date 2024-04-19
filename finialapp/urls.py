from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name = 'home'),
    path('index/', views.index, name = 'index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('serial_data/', views.serial_data, name='serial_data'),
    path('csv_data/', views.csv_data, name= 'csv_data'),
    path('send_command/', views.send_command, name='send_command'),
    path('ad_in/', views.ad_in, name='ad_in'),
    path('video_feed/', views.video_feed, name='video_feed'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
