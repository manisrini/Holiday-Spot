from django.urls import path,include

from . import views
from register import views as rv

app_name = 'holspot'
urlpatterns = [
    # ex: /polls/
   path('',views.home),
   path('register/',rv.register,name='register'),
   path('location/<int:pk_from_url>',views.detailed_location,name="location"),
   path('profile/<int:pk_from_url>',views.profile,name="profile"),
   path('',include('django.contrib.auth.urls')),
]