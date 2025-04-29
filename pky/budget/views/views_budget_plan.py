from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ..models import Budget


class BudgetView(TemplateView):
    template_name = "budget/budget_plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Budget.get_results()
        context['inkomen'] = Budget.objects.filter(category="IN").order_by('-budget')
        context['vast'] = Budget.objects.filter(category="VAST").order_by('-budget')
        context['flex'] = Budget.objects.filter(category="FLEX").order_by('-budget')
        context['inkomen_kaart'] = results['income']
        context['uitgaven_kaart'] = results['expense']
        context['balans_kaart'] = results['balance']
        return context


class CreateBudgetView(CreateView):
    template_name = "budget/generic_form.html"
    model = Budget
    fields = ["name", "budget", "category"]
    success_url = reverse_lazy('plan')


class UpdateBudgetView(UpdateView):
    template_name = "budget/generic_form.html"
    model = Budget
    fields = ["name", "budget", "category"]
    success_url = reverse_lazy('plan')


class DeleteBudgetView(DeleteView):
    template_name = 'budget/budget_confirm_delete.html'
    model = Budget
    success_url = reverse_lazy('plan')