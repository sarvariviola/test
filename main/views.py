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
    "fogy_alk_ezer": "A háztartások végső fogyasztási kiadásai alkoholos italokra, dohányra, kábítószerre",
    "fogy_egesz_ezer": "A háztartások végső fogyasztási kiadásai egészségre ",
    "fogy_etter_ezer": "A háztartások végső fogyasztási kiadásai éttermekre és szállásora",
    "fogy_okt_ezer": "A háztartások végső fogyasztási kiadásai oktatása ",
    "fogy_ruha_ezer": "A háztartások végső fogyasztási kiadásai ruházatra és lábbelire ",
    "fogy_transz_ezer": "A háztartások végső fogyasztási kiadásai transzportra ",
    "gdp_me": "Bruttó hazai termék (GDP)",
    "gdp_me_ezer": "Bruttó hazai termék (GDP)",
    "kivand": "Kivándorlók száma (emigráció)",
    "hal_sz": "Halálozások száma",
    "nep_jan1": "Népesség száma január 1-én",
    "nep_valt": "Teljes népességváltozás",
    "nep_valt_ar": "Teljes népesség változásának nyers mértéke",
    "nok_kora": "Nők átlagéletkora a gyermek születésekor",
    "nett_eur": "Nettó jövedelem euróban kifejezve",
}

keyword_list = [
    "Szerbia", "Magyarország", "Románia", "Régiók", "GDP",
    "Foglalkoztatás", "Fejlettség", "Demográfia", "Vajdaság",
    "Dél-Alföld", "Bánát", "Varianciaanalízis", "Elemzés", "Statisztika",
    "ANOVA", "Normalitás", "Shapiro–Wilk", "Gazdaság", "Régiók", "Országok",
]

# -------------------------------
# PÁROSÍTOTT VÁLTOZÓK
# -------------------------------
PAIRED_VARS = {
    "gdp_me": ["gdp_me", "gdp_me_ezer"],
    "fogy_alk": ["fogy_alk", "fogy_alk_ezer"],
    "fogy_egesz": ["fogy_egesz", "fogy_egesz_ezer"],
    "fogy_etter": ["fogy_etter", "fogy_etter_ezer"],
    "fogy_okt": ["fogy_okt", "fogy_okt_ezer"],
    "fogy_ruha": ["fogy_ruha", "fogy_ruha_ezer"],
    "fogy_transz": ["fogy_transz", "fogy_transz_ezer"],
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
    # VÁLTOZÓK LISTÁJA
    # -----------------------------
    if level == "orszag":
        variables = NormalityTestCountry.objects.values_list("variable", flat=True).distinct().order_by("variable")
    elif level == "regio":
        variables = NormalityTestRegion.objects.values_list("variable", flat=True).distinct().order_by("variable")

    filtered_variables = []
    for v in variables:
        has_anova = (
            AnovaTestCountry.objects.filter(variable=v).exists()
            if level == "orszag"
            else AnovaTestRegion.objects.filter(variable=v).exists()
        )

        img_path = os.path.join(settings.BASE_DIR, "main", "static", "main", "plots", f"{level}_{v}.png")
        if has_anova or os.path.exists(img_path):
            filtered_variables.append(v)

    variables = filtered_variables

    if selected_var is None and variables:
        selected_var = variables[0]

    if selected_var:
        display_var = DISPLAY_NAMES.get(selected_var, selected_var)

    # -----------------------------
    # NORMALITÁS
    # -----------------------------
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
            p_val = float(raw_p.replace("<", "").replace(">", "").replace(",", "."))
        except:
            p_val = None

        normality_list.append({
            key_name: getattr(row, key_name),
            "w": row.sw_w,
            "p": raw_p,
            "normal": (p_val is not None and p_val > 0.05),
        })

    stats["normality"] = normality_list
    stats["all_normal"] = all(x["normal"] for x in normality_list) if normality_list else False

    # -----------------------------
    # ANOVA + LEVENE – FŐ VÁLTOZÓ
    # -----------------------------
    model = AnovaTestCountry if level == "orszag" else AnovaTestRegion

    try:
        a = model.objects.get(variable=selected_var)
        raw_p = a.anova_p
        try:
            p_clean = float(raw_p.replace("<", "").replace(">", "").replace(",", "."))
        except:
            p_clean = None

        stats["anova"] = {
            "anova_f": a.anova_f,
            "anova_p": raw_p,
            "p_float": p_clean,
            "levene_f": a.levene_f,
            "levene_p": a.levene_p,
            "levene_ok": (a.levene_p is not None and a.levene_p > 0.05),
        }
    except:
        pass

    image_path = f"main/plots/{level}_{selected_var}.png" if selected_var else None

    # -----------------------------
    # PÁROSÍTOTT VÁLTOZÓ
    # -----------------------------
    paired_var = None
    paired_display = None
    paired_anova = None
    paired_image_path = None

    pair = PAIRED_VARS.get(selected_var)
    if pair:
        paired_var = pair[1]
        paired_display = DISPLAY_NAMES.get(paired_var, paired_var)

        try:
            a2 = model.objects.get(variable=paired_var)
            raw_p2 = a2.anova_p
            try:
                p_clean2 = float(raw_p2.replace("<", "").replace(">", "").replace(",", "."))
            except:
                p_clean2 = None

            paired_anova = {
                "anova_f": a2.anova_f,
                "anova_p": raw_p2,
                "p_float": p_clean2,
                "levene_f": a2.levene_f,
                "levene_p": a2.levene_p,
                "levene_ok": (a2.levene_p is not None and a2.levene_p > 0.05),
            }
        except:
            pass

        paired_image_path = f"main/plots/{level}_{paired_var}.png"

    return render(request, "index.html", {
        "level": level,
        "variables": variables,
        "selected_var": selected_var,
        "display_var": display_var,
        "stats": stats,
        "DISPLAY_NAMES": DISPLAY_NAMES,
        "image_path": image_path,
        "paired_var": paired_var,
        "paired_display": paired_display,
        "paired_anova": paired_anova,
        "paired_image_path": paired_image_path,
        "keyword_list": keyword_list,
    })
