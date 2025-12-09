from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import csv

class Command(BaseCommand):
    help = "Extract Overall ANOVA F and p values for REGIONS from SAS HTML"

    def add_arguments(self, parser):
        parser.add_argument("html_file", type=str, help="Path to SAS HTML file")
        parser.add_argument("csv_out", type=str, help="Path to output CSV")

    def handle(self, *args, **options):
        html_path = options["html_file"]
        csv_out = options["csv_out"]

        # Load HTML
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        results = []

        # Find all Overall ANOVA tables
        anova_tables = soup.find_all("table", summary=lambda x: x and "Overall ANOVA" in x)

        for table in anova_tables:

            # -------------------------------
            # 2) FIND VARIABLE NAME ABOVE
            # -------------------------------
            var_node = table.find_previous(string=lambda s: "Dependent Variable:" in s)
            if not var_node:
                continue

            raw = var_node.split("Dependent Variable:")[1].strip()

            # FIX: Some HTML contains duplicates → keep the first
            variable = raw.split()[0]

            # ------------------------------------
            # 3) PARSE FIRST ANOVA (Model) ROW
            # ------------------------------------
            rows = table.find_all("tr")
            if len(rows) < 2:
                continue

            model_row = rows[1]
            cells = [c.get_text(strip=True) for c in model_row.find_all("td")]

            if len(cells) < 5:
                continue

            f_value = cells[3]
            p_value = cells[4]

            results.append({
                "variable": variable,
                "f_value": f_value,
                "p_value": p_value
            })

        # -------------------------------
        # 4) WRITE CSV FILE
        # -------------------------------
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["variable", "f_value", "p_value"],
                delimiter=";"
            )
            writer.writeheader()

            for row in results:
                writer.writerow(row)

        self.stdout.write(
            self.style.SUCCESS(f"Siker! {len(results)} régiós ANOVA rekord mentve ide: {csv_out}")
        )