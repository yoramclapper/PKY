from django.views.generic import TemplateView, ListView
from django.views.generic.base import RedirectView
from ..models import Actual, Archive, ArchiveRecord


class ConfirmToArchiveView(TemplateView):
    template_name = "budget/confirm_to_archive.html"


class SaveToArchiveView(RedirectView):
    pattern_name = "create_actual"

    def get_redirect_url(self, *args, **kwargs):
        actuals = Actual.objects.all()
        archive = Archive(
            sheet_name=actuals[0].sheet_name
        )
        archive.save()
        for actual in actuals:
            archive_record = ArchiveRecord(
                archive=archive,
                name=actual.budget.name,
                budget=actual.budget.budget,
                actual=actual.actual,
                category=actual.budget.category
            )
            archive_record.save()
        return super().get_redirect_url(*args, **kwargs)


class ArchiveView(ListView):
    template_name = 'budget/archive.html'
    model = Archive
    context_object_name = 'archive_objects'
    ordering = ['-creation_date']


class ArchiveRecordView(TemplateView):
    template_name = "budget/archive_record.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['ref_actual'] = Archive.objects.get(pk=pk)
        context['inkomen'] = ArchiveRecord.objects.filter(archive__pk=pk, category="IN").order_by('-budget')
        context['vast'] = ArchiveRecord.objects.filter(archive__pk=pk, category="VAST").order_by('-budget')
        context['flex'] = ArchiveRecord.objects.filter(archive__pk=pk, category="FLEX").order_by('-budget')
        return context
