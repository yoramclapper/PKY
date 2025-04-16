from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Budget


class ActualsView(TemplateView):
    template_name = "budget/actuals.html"


class BudgetView(TemplateView):
    template_name = "budget/budget_plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inkomen'] = Budget.objects.filter(category="IN")
        context['vast'] = Budget.objects.filter(category="VAST")
        context['flex'] = Budget.objects.filter(category="FLEX")
        return context


class CreateBudgetView(CreateView):
    template_name = "budget/budget_form.html"
    model = Budget
    fields = ["name", "budget", "category"]
    success_url = reverse_lazy('plan')


class UpdateBudgetView(UpdateView):
    template_name = "budget/budget_form.html"
    model = Budget
    fields = ["name", "budget", "category"]
    success_url = reverse_lazy('plan')


class DeleteBudgetView(DeleteView):
    template_name = 'budget/budget_confirm_delete.html'
    model = Budget
    success_url = reverse_lazy('plan')

