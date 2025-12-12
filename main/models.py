from django.db import models

class NormalityTestCountry(models.Model):
    country = models.CharField(max_length=100)
    variable = models.CharField(max_length=100)

    sw_w = models.FloatField(null=True, blank=True)
    sw_p = models.CharField(max_length=20, null=True, blank=True)

    ks_d = models.FloatField(null=True, blank=True)
    ks_p = models.CharField(max_length=20, null=True, blank=True)

    cvm_w_sq = models.FloatField(null=True, blank=True)
    cvm_p = models.CharField(max_length=20, null=True, blank=True)

    ad_a_sq = models.FloatField(null=True, blank=True)
    ad_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.country} – {self.variable}"

class NormalityTestRegion(models.Model):
    region = models.CharField(max_length=100)
    variable = models.CharField(max_length=100)

    sw_w = models.FloatField(null=True, blank=True)
    sw_p = models.CharField(max_length=20, null=True, blank=True)

    ks_d = models.FloatField(null=True, blank=True)
    ks_p = models.CharField(max_length=20, null=True, blank=True)

    cvm_w_sq = models.FloatField(null=True, blank=True)
    cvm_p = models.CharField(max_length=20, null=True, blank=True)

    ad_a_sq = models.FloatField(null=True, blank=True)
    ad_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.region} – {self.variable}"

class AnovaTestCountry(models.Model):
    variable = models.CharField(max_length=200)
    f_value = models.FloatField(null=True, blank=True)
    p_value = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.variable} – F={self.f_value}, p={self.p_value}"

class AnovaTestRegion(models.Model):
    variable = models.CharField(max_length=200)
    levene_f = models.FloatField(null=True, blank=True)
    levene_p = models.FloatField(null=True, blank=True)
    anova_f = models.FloatField(null=True, blank=True)
    anova_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.variable

