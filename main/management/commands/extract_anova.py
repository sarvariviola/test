from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import csv

class Command(BaseCommand):
    help = "Extract first Overall ANOVA F and p values from SAS HTML"

    def add_arguments(self, parser):
        parser.add_argument("html_file", type=str, help="Path to ANOVA HTML")
        parser.add_argument("csv_out", type=str, help="Path to output CSV")

    def handle(self, *args, **options):
        html_path = options["html_file"]
        csv_out = options["csv_out"]

        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        results = []

        # ONLY Overall ANOVA tables
        anova_tables = soup.find_all("table", summary=lambda x: x and "Overall ANOVA" in x)

        for table in anova_tables:

            # Find variable above the table
            var_node = table.find_previous(string=lambda s: "Dependent Variable:" in s)
            if not var_node:
                continue

            raw = var_node.split("Dependent Variable:")[1].strip()

            # FIX: remove duplicates: "Gdp_mill_eur   Gdp_mill_eur"
            variable = raw.split()[0]

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

        # Write CSV
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["variable", "f_value", "p_value"], delimiter=";")
            writer.writeheader()
            for row in results:
                writer.writerow(row)

        self.stdout.write(
            self.style.SUCCESS(f"Siker! {len(results)} ANOVA rekord mentve ide: {csv_out}")
        )
