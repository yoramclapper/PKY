from django.db import models
from django.core.validators import MinValueValidator


class Budget(models.Model):
    CATEGORIES = [
        ("IN", "Inkomen"),
        ("VAST", "Vaste lasten"),
        ("FLEX", "Flexibele lasten"),
    ]
    name = models.CharField(max_length=50, unique=True)
    budget = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=5, choices=CATEGORIES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Actual(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    actual = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    creation_date = models.DateTimeField(auto_now_add=True)


class Archive(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    actual = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
