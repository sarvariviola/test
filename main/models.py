from django.db import models

# Modellek létrehozása 
class OrszagElemzes(models.Model):
    valtozo_neve = models.CharField(max_length=100)
    valtozo_teljes_neve = models.CharField(max_length=100)

    osszesen = models.FloatField(null=True, blank=True)
    ertek_egy_fore = models.FloatField(null=True, blank=True)

    f_ertek = models.FloatField(null=True)
    p_ertek = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.valtozo_neve


class RegioElemzes(models.Model):
    valtozo_neve = models.CharField(max_length=100)
    valtozo_teljes_neve = models.CharField(max_length=100)

    osszesen = models.FloatField(null=True, blank=True)
    ertek_egy_fore = models.FloatField(null=True, blank=True)

    f_ertek = models.FloatField(null=True)
    p_ertek = models.CharField(max_length=20, null=True)


    def __str__(self):
        return self.valtozo_neve
    