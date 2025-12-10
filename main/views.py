import os
from django.shortcuts import render
from .models import NormalityTestCountry, NormalityTestRegion, AnovaTestCountry, AnovaTestRegion
from django.conf import settings


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
    "belso_mig": "Bevándorlók száma (immigráció)",
    "brut_eur": "Bruttó jövedelem euróban kifejezve",
    "csecshal": "Csecsemőhalandóság száma",
    "elv_sz": "Élveszületések száma",
    "fogy_alk": "A háztartások végső fogyasztási kiadásai alkoholos italokra, dohányra, kábítószerre",
    "fogy_egesz": "A háztartások végső fogyasztási kiadásai egészségre ",
    "fogy_etter": "A háztartások végső fogyasztási kiadásai éttermekre és szállásora",
    "fogy_okt": "A háztartások végső fogyasztási kiadásai oktatása ",
    "fogy_ruha": "A háztartások végső fogyasztási kiadásai ruházatra és lábbelire ",
    "fogy_transz": "A háztartások végső fogyasztási kiadásai transzportra ",
    "gdp_me": "Bruttó hazai termék (GDP)",
    "kivand": "Kivándorlók száma (emigráció)",
    "hal_sz": "Halálozások száma",
    "nep_jan1": "Népesség száma január 1-én",
    "nep_valt": "Teljes népességváltozás",
    "nep_valt_ar": "Teljes népesség változásának nyers mértéke",
    "nok_kora": "Nők átlagéletkora a gyermek születésekor",
    "nett_eur": "Nettó jövedelem euróban kifejezve",
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
    # VÁLTOZÓLISTA
    # -----------------------------
    if level == "orszag":
        variables = (
            NormalityTestCountry.objects.values_list("variable", flat=True)
            .distinct().order_by("variable")
        )

    elif level == "regio":
        variables = (
            NormalityTestRegion.objects.values_list("variable", flat=True)
            .distinct().order_by("variable")
        )

    # ---------------------------------------
    # VÁLTOZÓK SZŰRÉSE: csak ha van ANOVA vagy ábra
    # ---------------------------------------
    filtered_variables = []
    for v in variables:

        # ANOVA létezik?
        if level == "orszag":
            has_anova = AnovaTestCountry.objects.filter(variable=v).exists()
        else:
            has_anova = AnovaTestRegion.objects.filter(variable=v).exists()

        # ÁBRA létezik?
        img_path = os.path.join(
            settings.BASE_DIR,
            "main", "static", "main", "plots",
            f"{level}_{v}.png"
        )
        has_plot = os.path.exists(img_path)

        if has_anova or has_plot:
            filtered_variables.append(v)

    variables = filtered_variables

    # Első változó automatikus kiválasztása
    if selected_var is None and variables:
        selected_var = variables[0]

    # Szép név
    if selected_var:
        display_var = DISPLAY_NAMES.get(selected_var, selected_var)

    # ---------------------------------------
    # NORMALITÁS
    # ---------------------------------------
    if selected_var and level == "orszag":
        qs = NormalityTestCountry.objects.filter(variable=selected_var).order_by("country")
        key_name = "country"

    elif selected_var and level == "regio":
        qs = NormalityTestRegion.objects.filter(variable=selected_var).order_by("region")
        key_name = "region"

    else:
        qs = []

    normality_list = []
    for row in qs:
        raw_p = row.sw_p
        try:
            p_val = float(raw_p.replace("<", "").replace(">", "").replace(",", "."))
        except:
            p_val = None

        normality_list.append({
            key_name: getattr(row, key_name),
            "w": row.sw_w,
            "p": raw_p,
            "normal": (p_val is not None and p_val > 0.05)
        })

    stats["normality"] = normality_list
    stats["all_normal"] = all(item["normal"] for item in normality_list) if normality_list else False

    # ---------------------------------------
    # ANOVA
    # ---------------------------------------
    model = AnovaTestCountry if level == "orszag" else AnovaTestRegion

    try:
        a = model.objects.get(variable=selected_var)

        raw_p = a.p_value
        try:
            p_clean = float(raw_p.replace("<", "").replace(">", "").replace(",", "."))
        except:
            p_clean = None

        stats["anova"] = {
            "f_value": a.f_value,
            "p_value": raw_p,
            "p_float": p_clean,
        }

    except model.DoesNotExist:
        stats["anova"] = None

    # ---------------------------------------
    # ÁBRA
    # ---------------------------------------
    image_path = f"main/plots/{level}_{selected_var}.png"

    return render(request, "index.html", {
        "level": level,
        "variables": variables,
        "selected_var": selected_var,
        "display_var": display_var,
        "stats": stats,
        "DISPLAY_NAMES": DISPLAY_NAMES,
        "image_path": image_path,
    })