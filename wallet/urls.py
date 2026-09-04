from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/<str:kind>/", views.add_transaction, name="add_transaction"),
    path("delete/<int:pk>/", views.delete_transaction, name="delete_transaction"),
    path("signup/", views.signup, name="signup"),
]
