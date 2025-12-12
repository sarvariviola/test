from django.core.management.base import BaseCommand
from main.models import AnovaTestRegion
import csv

class Command(BaseCommand):
    help = "ANOVA + Levene eredmények betöltése CSV-ből a régió szintű táblába"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Az ANOVA CSV fájl elérési útvonala"
        )

    def handle(self, *args, **options):
        csv_path = options["csv_file"]

        def to_float(value):
            if value is None:
                return None
            value = value.strip()
            if value == "":
                return None
            try:
                return float(value.replace(",", "."))
            except ValueError:
                return None

        created = 0

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")

            for row in reader:
                AnovaTestRegion.objects.create(
                    variable=row["variable"],
                    anova_f=to_float(row.get("anova_f")),
                    anova_p=row.get("anova_p"),
                    levene_f=to_float(row.get("levene_f")),
                    levene_p=to_float(row.get("levene_p")),
                )
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Siker! {created} régiós ANOVA + Levene rekord betöltve."
            )
        )
