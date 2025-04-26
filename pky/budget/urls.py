from django.urls import path

from .views import ActualsView, UpdateActualView, CreateActualView, ConfirmToArchiveView, SaveToArchiveView, ArchiveView, ArchiveRecordView, BudgetView, CreateBudgetView, UpdateBudgetView, DeleteBudgetView

urlpatterns = [
    path("", ActualsView.as_view(), name="index"),
    path("actual/update/<int:pk>", UpdateActualView.as_view(), name="update_actual"),
    path("actual/create", CreateActualView.as_view(), name="create_actual"),
    path("actual/confirm_to_archive", ConfirmToArchiveView.as_view(), name="confirm_to_archive"),
    path("actual/save_to_archive", SaveToArchiveView.as_view(), name="save_to_archive"),
    path("plan", BudgetView.as_view(), name="plan"),
    path("plan/create", CreateBudgetView.as_view(), name="create_budget"),
    path("plan/update/<int:pk>", UpdateBudgetView.as_view(), name="update_budget"),
    path("plan/delete/<int:pk>", DeleteBudgetView.as_view(), name="delete_budget"),
    path("archive", ArchiveView.as_view(), name="archive"),
    path("archive/<int:pk>", ArchiveRecordView.as_view(), name="archive_records"),
]