from django.urls import path
from django import urls
from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

# app_name='app'

urlpatterns = [
    path('', views.index ,name='index'),
    path('user/register', views.register ,name='register'),
    path('user/login', views.login ,name='login'),
    path('user/logout', views.logout ,name='logout'),
    path('user/search/<term>', views.user_search ,name='user_search'),
    path('user/details', views.user_details ,name='user_details'),
    path('markspam/<mobile>', views.mark_spam ,name='mark_spam'),
    path('dummy/markspam', views.dummy_mark_spam ,name='dummy_mark_spam'),
    path('dummy/user_data', views.dummy_user_data ,name='dummy_user_data'),
    path('dummy/contact_data', views.dummy_contact_data ,name='dummy_contact_data'),

]