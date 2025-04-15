from django.views.generic import TemplateView


class ActualsView(TemplateView):
    template_name = "budget/actuals.html"
