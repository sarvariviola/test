from django.shortcuts import render
from .models import NormalityTestCountry, NormalityTestRegion, AnovaTestCountry


# -------------------------------
# VÁLTOZÓK SZÉP ELNEVEZÉSEI
# -------------------------------
DISPLAY_NAMES = {
    "Gdp_mill_eur": "Bruttó hazai termék (millió EUR)",
    "Gdp_ezer_fore": "GDP egy főre (ezer EUR)",
    "AVFK": "Államháztartás végső fogyasztási kiadásai (ÁVFK)",
    "AVFK_ezer_fore": "Államháztartás végső fogyasztási kiadásai (ezer főre)",
    "Haztartasok_fogy_kiadasa": "Háztartások végső fogyasztási kiadásai",
    "Haztartas_fogy_kiadas_ezer_fore": "Háztartások fogyasztási kiadásai (ezer főre)",
    "Nepesseg_term_valtozasa": "A népesség természetes változásának nyers mértéke",
    "Termekenysegi_rata": "Termékenységi ráta",
    "Nok_atlageletkor_szules": "Nők átlagéletkora a gyermek születésekor",
    "Elveszuletesek_szama": "Élveszületések száma",
    "Szul_aranyszam_ezer_fo": "Születési arányszám (ezer főre)",
    "Halalozasok_szama": "Halálozások száma",
    "Halal_aranyszam_ezer_fo": "Halálozási arányszám (ezer főre)",
    "Csecsemohalandosag": "Csecsemőhalandóság",
    "Bevandorlok_nemzetkozi_mig": "Bevándorlók – nemzetközi migráció",
    "Bevandorlasi_arany": "Bevándorlási arány",
    "Kivandorlok_nemzetkozi_mig": "Kivándorlók – nemzetközi migráció",
    "Kivandorlasi_arany": "Kivándorlási arány",
    "Brutto_jovedelem_eur": "Éves átlagos bruttó jövedelem (EUR)",
    "Netto_jovedelem_eur": "Éves átlagos nettó jövedelem (EUR)",
    "Inflacios_rata": "Inflációs ráta (%)",
    "Teljes_munkanelkulisegi_rata": "Teljes munkanélküliségi ráta (%)",
    "Nepesseg": "Népesség",
    "Kiadas_elelmiszer": "Háztartási kiadások élelmiszerre",
    "Kiadas_alkohol": "Háztartási kiadások alkoholra és dohányra",
    "Kiadas_ruhazat": "Háztartási kiadások ruházatra",
    "Kiadas_egeszseg": "Háztartási kiadások egészségre",
    "Kiadas_transzport": "Háztartási kiadások transzportra",
    "Kiadas_oktatas": "Háztartási kiadások oktatásra",
    "Kiadas_etterem_szallas": "Háztartási kiadások étteremre és szállásra",
    "Kiadas_etterem_szallas_ezer_fo": "Háztartási kiadások étteremre és szállásra (ezer főre)",
    "Haztartasi_megtak_rata": "Háztartási megtakarítási ráta (%)",
    "Mezogazdasagi_ter": "Mezőgazdasági terület (hektár)",
    "Mezogazdasagi_ter_ezer_fo": "Mezőgazdasági terület (ezer főre)",
}


def index(request):
    level = request.GET.get("szint")
    selected_var = request.GET.get("valtozo")

    variables = []
    display_var = None

    stats = {
        "anova": None,
        "normality": [],
        "all_normal": False,
    }

    # -----------------------------
    # VÁLTOZÓK LISTÁJA ORSZÁG / RÉGIÓ
    # -----------------------------
    if level == "orszag":
        variables = (
            NormalityTestCountry.objects
            .values_list("variable", flat=True)
            .distinct()
            .order_by("variable")
        )

    elif level == "regio":
        variables = (
            NormalityTestRegion.objects
            .values_list("variable", flat=True)
            .distinct()
            .order_by("variable")
        )

    # Ha nincs kiválasztott változó → automatikusan az első
    if selected_var is None and variables:
        selected_var = variables[0]

    # Szép név
    if selected_var:
        display_var = DISPLAY_NAMES.get(selected_var, selected_var)

    # ------------------------------------
    # NORMALITÁS LEKÉRÉSE
    # ------------------------------------
    if level == "orszag" and selected_var:
        qs = NormalityTestCountry.objects.filter(variable=selected_var).order_by("country")
        key_name = "country"

    elif level == "regio" and selected_var:
        qs = NormalityTestRegion.objects.filter(variable=selected_var).order_by("region")
        key_name = "region"

    else:
        qs = []

    normality_list = []
    for row in qs:
        raw_p = row.sw_p
        try:
            p_value = float(raw_p.replace("<", "").replace(">", "").replace(",", "."))
        except:
            p_value = None

        normality_list.append({
            key_name: getattr(row, key_name),
            "w": row.sw_w,
            "p": raw_p,
            "normal": (p_value is not None and p_value > 0.05)
        })

    stats["normality"] = normality_list
    stats["all_normal"] = all(item["normal"] for item in normality_list) if normality_list else False

    # ------------------------------------
    # ANOVA LEKÉRÉSE ORSZÁGRA / RÉGIÓRA
    # ------------------------------------
    model = None  # <<< FONTOS

    if selected_var:
        if level == "orszag":
            model = AnovaTestCountry
        elif level == "regio":
            from .models import AnovaTestRegion
            model = AnovaTestRegion

    if model:
        try:
            a = model.objects.get(variable=selected_var)
            # p-érték konvertálása float-tá
            raw_p = a.p_value
            try:
                p_clean = float(raw_p.replace("<", "").replace(">", "").replace(",", "."))
            except:
                p_clean = None

            stats["anova"] = {
                "f_value": a.f_value,
                "p_value": raw_p,     # eredeti szöveg
                "p_float": p_clean,   # szám
            }
        except model.DoesNotExist:
            stats["anova"] = None

    # KÉP ELÉRÉSI ÚTVONALA
    image_filename = None

    if selected_var and level:
        image_filename = f"{level}_{selected_var}.png"   # pl. 'regio_Gdp_mill_eur.png'

    image_path = f"main/plots/{image_filename}" if image_filename else None

    # ------------------------------------
    # RENDER
    # ------------------------------------
    return render(request, "index.html", {
        "level": level,
        "variables": variables,
        "selected_var": selected_var,
        "display_var": display_var,
        "stats": stats,
        "DISPLAY_NAMES": DISPLAY_NAMES,  # HTML-nek kell!
        "image_path": image_path,
    })
