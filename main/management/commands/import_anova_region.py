from django.core.management.base import BaseCommand
from main.models import AnovaTestRegion
import csv

class Command(BaseCommand):
    help = "Import ANOVA F és p értékek betöltése CSV-ből a régió szintű táblába"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Az ANOVA CSV fájl elérési útvonala")

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
                obj = AnovaTestRegion(
                    variable=row["variable"],
                    f_value=to_float(row["f_value"]),
                    p_value=row["p_value"],
                )
                obj.save()
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Siker! {created} régiós ANOVA rekord betöltve.")
        )
