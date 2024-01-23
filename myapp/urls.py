from django.urls import path
from .import views

urlpatterns = [
    path('Resgistrations/', views.ResgistrationsView.as_view()),
    path('Login/', views.LoginView.as_view()),
    path('Activity/', views.ActivityView.as_view()),
    path('Purchase/', views.PurchaseView.as_view()),

]
