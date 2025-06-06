from django.db import models
from django.core.validators import MinValueValidator


class Budget(models.Model):
    CATEGORIES = [
        ("IN", "Inkomen"),
        ("VAST", "Vaste lasten"),
        ("FLEX", "Flexibele lasten"),
    ]
    name = models.CharField(max_length=50, unique=True, verbose_name="Naam")
    budget = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Budget")
    category = models.CharField(max_length=5, choices=CATEGORIES, verbose_name="Categorie")
    active = models.BooleanField(default=True)

    @classmethod
    def get_results(cls) -> dict[str, float]:
        income = sum([budget.budget for budget in cls.objects.filter(category="IN")])
        expense = sum([budget.budget for budget in cls.objects.filter(category__in=["VAST", "FLEX"])])
        return {'income': income, 'expense': expense, 'balance': income - expense}


class Actual(models.Model):
    sheet_name = models.CharField(max_length=50, verbose_name="Naam registratieblad")
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    actual = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Werkelijk bedrag')


class Archive(models.Model):
    sheet_name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sheet_name


class ArchiveRecord(models.Model):
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, verbose_name="Naam")
    budget = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    actual = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=5, choices=Budget.CATEGORIES, verbose_name="Categorie")

    def __str__(self):
        return self.name
