from django.urls import path

from .views import ActualsView, BudgetView, CreateBudgetView, UpdateBudgetView, DeleteBudgetView

urlpatterns = [
    path("", ActualsView.as_view(), name="index"),
    path("plan", BudgetView.as_view(), name="plan"),
    path("plan/create", CreateBudgetView.as_view(), name="create_budget"),
    path("plan/update/<int:pk>", UpdateBudgetView.as_view(), name="update_budget"),
    path("plan/delete/<int:pk>", DeleteBudgetView.as_view(), name="delete_budget"),
]