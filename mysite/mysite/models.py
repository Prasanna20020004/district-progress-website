from django.db import models

class MGNREGAData(models.Model):
    fin_year = models.CharField(max_length=20, blank=True, null=True)
    month = models.CharField(max_length=20, blank=True, null=True)
    state_code = models.CharField(max_length=10, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    district_code = models.CharField(max_length=10, blank=True, null=True)
    district_name = models.CharField(max_length=100, blank=True, null=True)
    approved_labour_budget = models.FloatField(blank=True, null=True)
    average_wage_rate = models.FloatField(blank=True, null=True)
    total_expenditure = models.FloatField(blank=True, null=True)
    total_households_worked = models.IntegerField(blank=True, null=True)
    women_persondays = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = 'mysite'  # since you're not using a separate app

    def __str__(self):
        return f"{self.district_name} ({self.fin_year})"
