from django.core.management.base import BaseCommand
from main.models import NormalityTestCountry
import csv

class Command(BaseCommand):
    help = "Normalitási teszt eredmények betöltése CSV fájlból az adatbázisba"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="A CSV fájl elérési útvonala")

    def handle(self, *args, **options):
        csv_path = options["csv_file"]

        def to_float(value):
            try:
                return float(value.replace(",", "."))
            except:
                return None

        created = 0

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")

            for row in reader:
                obj = NormalityTestCountry(
                    country=row["country"],
                    variable=row["variable"],
                    sw_w=to_float(row["sw_w"]),
                    sw_p=row["sw_p"],
                    ks_d=to_float(row["ks_d"]),
                    ks_p=row["ks_p"],
                    cvm_w_sq=to_float(row["cvm_w_sq"]),
                    cvm_p=row["cvm_p"],
                    ad_a_sq=to_float(row["ad_a_sq"]),
                    ad_p=row["ad_p"],
                )
                obj.save()
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Siker! {created} rekord betöltve adatbázisba."))
