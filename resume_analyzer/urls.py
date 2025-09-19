
from django.urls import path,include
from . import views

urlpatterns = [
  path('', views.simple_upload, name='home'),
  # path('uploaded/', views.history_view, name='uploaded'),
 # path('contact/', views.contact, name='contact'),
  path("__reload__/", include("django_browser_reload.urls")),
]
