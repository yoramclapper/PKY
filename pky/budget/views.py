from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Budget, Actual, Archive


class ActualsView(TemplateView):
    template_name = "budget/actuals.html"

    def get(self, request, *args, **kwargs):
        if not Actual.objects.exists():
            return redirect('create_actual')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ref_actual'] = Actual.objects.all()[0]
        context['inkomen'] = Actual.objects.filter(budget__category="IN").order_by('-budget__budget')
        context['vast'] = Actual.objects.filter(budget__category="VAST").order_by('-budget__budget')
        context['flex'] = Actual.objects.filter(budget__category="FLEX").order_by('-budget__budget')
        return context


class UpdateActualView(UpdateView):
    template_name = "budget/generic_form.html"
    model = Actual
    fields = ["actual"]
    success_url = reverse_lazy('index')


class CreateActualView(CreateView):
    template_name = "budget/generic_form.html"
    model = Actual
    fields = ["sheet_name"]
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        Actual.objects.all().delete()
        budgets = Budget.objects.all()
        for budget in budgets:
            actual = Actual(
                sheet_name=self.object.sheet_name,
                budget=budget,
                actual=0
            )
            actual.save()
        return HttpResponseRedirect(self.get_success_url())


class ConfirmToArchiveView(TemplateView):
    template_name = "budget/confirm_to_archive.html"


class SaveToArchiveView(RedirectView):
    pattern_name = "create_actual"

    def get_redirect_url(self, *args, **kwargs):
        actuals = Actual.objects.all()
        for actual in actuals:
            archive_record = Archive(
                sheet_name=actual.sheet_name,
                budget=actual.budget.budget,
                actual=actual.actual
            )
            archive_record.save()
        return super().get_redirect_url(*args, **kwargs)


class BudgetView(TemplateView):
    template_name = "budget/budget_plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inkomen'] = Budget.objects.filter(category="IN").order_by('-budget')
        context['vast'] = Budget.objects.filter(category="VAST").order_by('-budget')
        context['flex'] = Budget.objects.filter(category="FLEX").order_by('-budget')
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
