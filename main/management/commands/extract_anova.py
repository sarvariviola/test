from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import csv


class Command(BaseCommand):
    help = "Extract Overall ANOVA and Levene test results (country-level) from SAS HTML into CSV"

    def add_arguments(self, parser):
        parser.add_argument("html_file", type=str, help="Path to SAS HTML")
        parser.add_argument("csv_out", type=str, help="Path to output CSV")

    def handle(self, *args, **options):
        html_path = options["html_file"]
        csv_out = options["csv_out"]

        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # =====================================================
        # Eredmények változónként
        # =====================================================
        results = {}

        # =====================================================
        # 1️⃣ OVERALL ANOVA – Model sor
        # =====================================================
        anova_tables = soup.find_all(
            "table",
            summary=lambda x: x and "Overall ANOVA" in x
        )

        for table in anova_tables:

            # Függő változó neve
            var_node = table.find_previous(
                string=lambda s: s and "Dependent Variable:" in s
            )
            if not var_node:
                continue

            raw = var_node.split("Dependent Variable:")[1].strip()

            # duplikált SAS kiírások levágása
            variable = raw.split()[0]

            rows = table.find_all("tr")
            if len(rows) < 2:
                continue

            # 2. sor = Model
            model_row = rows[1]
            cells = [c.get_text(strip=True) for c in model_row.find_all("td")]

            if len(cells) < 5:
                continue

            results.setdefault(variable, {
                "variable": variable,
                "anova_f": "",
                "anova_p": "",
                "levene_f": "",
                "levene_p": "",
            })

            results[variable]["anova_f"] = cells[3]
            results[variable]["anova_p"] = cells[4]

        # =====================================================
        # 2️⃣ LEVENE TESZT – ország
        # =====================================================
        levene_headers = soup.find_all(
            "th",
            attrs={"scope": "colgroup"}
        )

        for header in levene_headers:
            header_text = header.get_text(" ", strip=True)

            if "Levene" not in header_text:
                continue

            # változónév: "... of gdp_me Variance"
            parts = header_text.split("of")
            if len(parts) < 2:
                continue

            variable = parts[1].split()[0]

            table = header.find_parent("table")
            if not table:
                continue

            tbody = table.find("tbody")
            if not tbody:
                continue

            for row in tbody.find_all("tr"):
                row_header = row.find("th", scope="row")
                if not row_header:
                    continue

                # ORSZÁG – kis/nagybetű és ékezetbiztos
                row_name = row_header.get_text(strip=True).lower()
                if row_name not in ["orszag", "ország", "country"]:
                    continue

                cells = row.find_all("td")
                if len(cells) >= 5:
                    results.setdefault(variable, {
                        "variable": variable,
                        "anova_f": "",
                        "anova_p": "",
                        "levene_f": "",
                        "levene_p": "",
                    })
                    results[variable]["levene_f"] = cells[3].get_text(strip=True)
                    results[variable]["levene_p"] = cells[4].get_text(strip=True)

                break

        # =====================================================
        # 3️⃣ CSV KIÍRÁS
        # =====================================================
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "variable",
                    "anova_f",
                    "anova_p",
                    "levene_f",
                    "levene_p",
                ],
                delimiter=";"
            )
            writer.writeheader()

            # rendezve, hogy stabil legyen
            for key in sorted(results.keys()):
                writer.writerow(results[key])

        self.stdout.write(
            self.style.SUCCESS(
                f"Kész! {len(results)} országos ANOVA + Levene eredmény CSV-be mentve."
            )
        )