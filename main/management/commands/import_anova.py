from django.core.management.base import BaseCommand
from main.models import AnovaTestCountry
import csv

class Command(BaseCommand):
    help = "Import ANOVA F and p values from CSV into the database"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to ANOVA CSV file")

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

                obj = AnovaTestCountry(
                    variable=row["variable"],
                    f_value=to_float(row["f_value"]),
                    p_value=row["p_value"],
                )

                obj.save()
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Siker! {created} ANOVA rekord betöltve adatbázisba.")
        )
