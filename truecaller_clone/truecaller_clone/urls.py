from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls import url

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('app.urls'),name='index'),

]

