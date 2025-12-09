from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import csv


class Command(BaseCommand):
    help = "Extract 'Tests for Normality' results for REGIONS from SAS HTML into CSV."

    def add_arguments(self, parser):
        parser.add_argument("html_file", type=str, help="Path to SAS HTML file")
        parser.add_argument("csv_out", type=str, help="Path to output CSV")

    def handle(self, *args, **options):
        html_path = options["html_file"]
        csv_out = options["csv_out"]

        # --- Load HTML ---
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # All "Tests for Normality" headers
        tests_headers = soup.find_all(
            string=lambda s: isinstance(s, str) and "Tests for Normality" in s
        )

        rows_data = []

        for th in tests_headers:

            # ------------------------------------
            # 1) FIND REGION + VARIABLE
            # ------------------------------------
            cur = th
            region = None
            variable = None
            steps = 0

            while cur and steps < 10000 and (region is None or variable is None):
                cur = cur.find_previous(string=True)
                steps += 1

                if not cur:
                    break

                text = cur.strip()

                # Region line example: "Regio = Vajdaság"
                if region is None and text.startswith("regio ="):
                    region = text.split("=", 1)[1].strip()

                # Variable line example: "Variable: GDP"
                if variable is None and text.startswith("Variable:"):
                    body = text[len("Variable:"):].strip()
                    if "(" in body:
                        variable = body.split("(", 1)[0].strip()
                    else:
                        variable = body

            # ------------------------------------
            # 2) FIND THE TABLE
            # ------------------------------------
            table = th.parent
            while table and table.name != "table":
                table = table.parent

            if not table:
                continue

            # Default row
            tests = {
                "region": region or "",
                "variable": variable or "",
                "sw_w": "",
                "sw_p": "",
                "ks_d": "",
                "ks_p": "",
                "cvm_w_sq": "",
                "cvm_p": "",
                "ad_a_sq": "",
                "ad_p": "",
            }

            # ------------------------------------
            # 3) PARSE THE NORMALITY TEST TABLE
            # ------------------------------------
            for tr in table.find_all("tr"):
                cells = [c.get_text(strip=True) for c in tr.find_all(["th", "td"])]
                if not cells:
                    continue

                name = cells[0].lower()

                if "shapiro-wilk" in name:
                    tests["sw_w"] = cells[2]
                    tests["sw_p"] = cells[4]

                elif "kolmogorov-smirnov" in name:
                    tests["ks_d"] = cells[2]
                    tests["ks_p"] = cells[4]

                elif "cramer-von mises" in name:
                    tests["cvm_w_sq"] = cells[2]
                    tests["cvm_p"] = cells[4]

                elif "anderson-darling" in name:
                    tests["ad_a_sq"] = cells[2]
                    tests["ad_p"] = cells[4]

            rows_data.append(tests)

        # ------------------------------------
        # 4) WRITE CSV
        # ------------------------------------
        fieldnames = [
            "region", "variable",
            "sw_w", "sw_p",
            "ks_d", "ks_p",
            "cvm_w_sq", "cvm_p",
            "ad_a_sq", "ad_p"
        ]

        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for row in rows_data:
                writer.writerow(row)

        self.stdout.write(
            self.style.SUCCESS(f"Siker! {len(rows_data)} régiós normalitási rekord mentve ide: {csv_out}")
        )
