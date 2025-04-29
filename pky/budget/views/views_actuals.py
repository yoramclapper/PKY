from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Budget, Actual


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