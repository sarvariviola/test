from django.db import models


class NormalityTestCountry(models.Model):
    """
    Országszintű normalitási tesztek eredményei.
    Tárolja a különböző statisztikai normalitási tesztek (Shapiro-Wilk, Kolmogorov-Smirnov,
    Cramér-von Mises, Anderson-Darling) eredményeit országonként és változónként.
    """
    country = models.CharField(max_length=100)
    variable = models.CharField(max_length=100)

    # Shapiro-Wilk teszt eredményei
    sw_w = models.FloatField(null=True, blank=True)
    sw_p = models.CharField(max_length=20, null=True, blank=True)

    # Kolmogorov-Smirnov teszt eredményei
    ks_d = models.FloatField(null=True, blank=True)
    ks_p = models.CharField(max_length=20, null=True, blank=True)

    # Cramér-von Mises teszt eredményei
    cvm_w_sq = models.FloatField(null=True, blank=True)
    cvm_p = models.CharField(max_length=20, null=True, blank=True)

    # Anderson-Darling teszt eredményei
    ad_a_sq = models.FloatField(null=True, blank=True)
    ad_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.country} – {self.variable}"


class NormalityTestRegion(models.Model):
    """
    Régiószintű normalitási tesztek eredményei.
    Tárolja a különböző statisztikai normalitási tesztek eredményeit régiónként és változónként.
    """
    region = models.CharField(max_length=100)
    variable = models.CharField(max_length=100)

    # Shapiro-Wilk teszt eredményei
    sw_w = models.FloatField(null=True, blank=True)
    sw_p = models.CharField(max_length=20, null=True, blank=True)

    # Kolmogorov-Smirnov teszt eredményei
    ks_d = models.FloatField(null=True, blank=True)
    ks_p = models.CharField(max_length=20, null=True, blank=True)

    # Cramér-von Mises teszt eredményei
    cvm_w_sq = models.FloatField(null=True, blank=True)
    cvm_p = models.CharField(max_length=20, null=True, blank=True)

    # Anderson-Darling teszt eredményei
    ad_a_sq = models.FloatField(null=True, blank=True)
    ad_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.region} – {self.variable}"


class AnovaTestCountry(models.Model):
    """
    Országszintű ANOVA és Levene-teszt eredményei.
    Tárolja az egyszempontos ANOVA és a Levene-teszt (szóráshomogenitás)
    eredményeit változónként az országok összehasonlításához.
    """
    variable = models.CharField(max_length=200)

    # Levene-teszt eredményei (szóráshomogenitás vizsgálata)
    levene_f = models.FloatField(null=True, blank=True)
    levene_p = models.FloatField(null=True, blank=True)

    # ANOVA teszt eredményei
    anova_f = models.FloatField(null=True, blank=True)
    anova_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.variable


class AnovaTestRegion(models.Model):
    """
    Régiószintű ANOVA és Levene-teszt eredményei.
    Tárolja az egyszempontos ANOVA és a Levene-teszt eredményeit
    változónként a régiók összehasonlításához.
    """
    variable = models.CharField(max_length=200)

    # Levene-teszt eredményei (szóráshomogenitás vizsgálata)
    levene_f = models.FloatField(null=True, blank=True)
    levene_p = models.FloatField(null=True, blank=True)

    # ANOVA teszt eredményei
    anova_f = models.FloatField(null=True, blank=True)
    anova_p = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.variable

