from django.urls import path
from .import views

urlpatterns = [
    path('resgistrations/', views.ResgistrationsView.as_view(), name="resgistrations"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('activity/', views.ActivityView.as_view(), name="activity"),
    path('purchase/', views.PurchaseView.as_view(), name="purchase"),
]
