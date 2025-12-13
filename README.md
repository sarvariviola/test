# Statisztikai Elemzési Platform

Ország- és régiószintű különbségek statisztikai elemzése Szerbiában és a szomszédos országokban.

## Tartalomjegyzék

- [Áttekintés](#áttekintés)
- [Funkciók](#funkciók)
- [Technológiák](#technológiák)
- [Telepítés](#telepítés)
- [Adatbázis beállítása](#adatbázis-beállítása)
- [Adatok importálása](#adatok-importálása)
- [Használat](#használat)
- [Projekt struktúra](#projekt-struktúra)
- [Statisztikai módszerek](#statisztikai-módszerek)
- [Responsive design](#responsive-design)

## Áttekintés

Ez a Django-alapú webalkalmazás statisztikai elemzéseket végez demográfiai és gazdasági adatokon. Az alkalmazás lehetővé teszi ország- és régiószintű adatok összehasonlítását ANOVA és normalitási tesztek segítségével.

### Készítette

Sárvári Viola

## Funkciók

### Kétszintű elemzés
- **Országszintű elemzés**: Szerbia és szomszédos országok összehasonlítása
- **Régiószintű elemzés**: Szerbia régióinak belső összehasonlítása

### Statisztikai tesztek
- **Shapiro-Wilk normalitási teszt**: Az adatok normális eloszlásának vizsgálata
- **ANOVA (Analysis of Variance)**: Csoportok közötti különbségek tesztelése
- **Levene-teszt**: Szóráshomogenitás vizsgálata

### Vizualizáció
- Interaktív grafikonok régiónkénti és országonkénti bontásban
- Eredmények vizuális megjelenítése PNG formátumban

### Felhasználói felület
- Modern, responsive design
- Mobil-optimalizált nézet
- Glassmorphism stílusú kártyák
- Animált háttér kulcsszavakkal
- Sidebar vezérlőpanel mobil toggle funkcióval

## Technológiák

### Backend
- Python 3.13
- Django 5.2.8
- PostgreSQL
- psycopg 3.2.12

### Frontend
- HTML5
- CSS3 (responsive design, media queries)
- JavaScript (ES6+)
- Bootstrap 5.3.3

### Adatkezelés
- CSV fájlok importálása Django management parancsokkal
- Statisztikai modellek Django ORM használatával

## Telepítés

### Előfeltételek
- Python 3.13 vagy újabb
- PostgreSQL 15 vagy újabb
- pip (Python package manager)

### Lépések

1. Klónozd le a repositoryt:
```bash
git clone <repository-url>
cd test
```

2. Hozz létre virtuális környezetet:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

3. Telepítsd a függőségeket:
```bash
pip install -r requirements.txt
```

4. Hozz létre egy `.env` fájlt a projekt gyökérkönyvtárában:
```env
DB_NAME=test_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Adatbázis beállítása

### PostgreSQL adatbázis létrehozása

1. Telepítsd a PostgreSQL-t (macOS):
```bash
brew install postgresql@15
brew services start postgresql@15
```

2. Hozd létre az adatbázist:
```bash
createdb -U postgres test_db
```

Vagy PostgreSQL konzolból:
```bash
psql -U postgres
CREATE DATABASE test_db;
\q
```

### Django migrációk futtatása

```bash
python manage.py migrate
```

Ez létrehozza az összes szükséges táblát:
- `main_normalitytestcountry` - Országszintű normalitási tesztek
- `main_normalitytestregion` - Régiószintű normalitási tesztek
- `main_anovatestcountry` - Országszintű ANOVA eredmények
- `main_anovatestregion` - Régiószintű ANOVA eredmények

## Adatok importálása

Az alkalmazás CSV fájlokból importálja az előre kiszámított statisztikai eredményeket.

### Importálási sorrend

```bash
# 1. Normalitási adatok importálása
python manage.py import_normality data/normalitas_orszag.csv
python manage.py import_normality_reg data/normalitas_regio.csv

# 2. ANOVA adatok importálása
python manage.py import_anova data/anova_orszag.csv
python manage.py import_anova_region data/anova_regio.csv
```

### CSV fájl formátumok

**normalitas_orszag.csv**
- Változó név
- Ország/régió név
- W érték (Shapiro-Wilk statisztika)
- p-érték
- Normalitás (boolean)

**anova_orszag.csv**
- Változó név
- ANOVA F érték
- ANOVA p-érték
- Levene F érték
- Levene p-érték

## Használat

### Szerver indítása

```bash
python manage.py runserver
```

Az alkalmazás elérhető: `http://127.0.0.1:8000`

### Navigáció

1. **Kezdőképernyő**: Válaszd ki az elemzési szintet (ország vagy régió)
2. **Változó választás**: Válaszd ki az elemezni kívánt változót a legördülő listából
3. **Eredmények**:
   - Normalitási teszt eredményei országonként/régiónként
   - Levene-teszt eredménye (szóráshomogenitás)
   - ANOVA F érték és p-érték
   - Grafikus megjelenítés (ha elérhető)

### Elemzési szintek váltása

A sidebar segítségével bármikor válthatsz ország- és régiószintű elemzés között, illetve választhatsz másik változót az elemzéshez.

## Projekt struktúra

```
test/
├── dashboard/              # Django projekt beállítások
│   ├── settings.py        # Fő konfiguráció
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI konfiguráció
├── main/                  # Fő alkalmazás
│   ├── management/        # Custom Django parancsok
│   │   └── commands/      # Import parancsok
│   ├── migrations/        # Adatbázis migrációk
│   ├── static/            # Statikus fájlok
│   │   └── main/
│   │       ├── plots/     # Grafikon PNG fájlok
│   │       └── style.css  # Egyedi CSS stílusok
│   ├── templates/         # Django template-ek
│   │   ├── index.html     # Fő oldal
│   │   └── sas/           # SAS elemzési eredmények
│   ├── templatetags/      # Custom template filterek
│   ├── models.py          # Adatbázis modellek
│   ├── views.py           # View logika
│   └── utils.py           # Segédfüggvények
├── data/                  # CSV adatfájlok
├── db.sqlite3             # SQLite adatbázis (fejlesztéshez)
├── manage.py              # Django management szkript
└── requirements.txt       # Python függőségek
```

## Statisztikai módszerek

### Shapiro-Wilk teszt

Normális eloszlás tesztelésére használatos. A nullhipotézis szerint az adatok normális eloszlásúak.
- Ha p > 0.05: Az adatok normális eloszlásúak
- Ha p < 0.05: Az adatok NEM normális eloszlásúak

### ANOVA (Varianciaanalízis)

Három vagy több csoport átlagainak összehasonlítására szolgál.
- Ha p < 0.05: Szignifikáns különbség van a csoportok között
- Ha p > 0.05: Nincs szignifikáns különbség

### Levene-teszt

A csoportok varianciáinak homogenitását teszteli (ANOVA előfeltétel).
- Ha p > 0.05: A szóráshomogenitás teljesül
- Ha p < 0.05: A szóráshomogenitás NEM teljesül

### Eredmények értelmezése

Az alkalmazás automatikusan értékeli az eredményeket:
- **Zöld**: Minden feltétel teljesül, az eredmények megbízhatóak
- **Sárga**: Az ANOVA szignifikáns, de valamelyik előfeltétel nem teljesül
- **Piros**: Az ANOVA nem mutatott szignifikáns különbséget

## Responsive design

Az alkalmazás teljes mértékben reszponzív és optimalizált:

### Breakpointok
- Mobil: < 768px
- Kis mobil: < 480px
- Extra kis mobil: < 380px
- Tablet/Desktop: > 768px

### Mobil funkciók
- Hamburger menü a sidebar-hez (jobb alsó sarok)
- Csúszó sidebar animáció
- Optimalizált betűméretek
- Touch-friendly gombok (min. 44px)
- Landscape orientáció támogatás
- iOS zoom megelőzés (16px input font-size)

### Tesztelés
Használd a böngésző DevTools-t a mobil nézet teszteléséhez:
- Chrome: `Cmd + Shift + M` (Mac) vagy `F12` + Device Toggle
- Firefox: `Cmd + Option + M`
- Safari: `Develop` > `Responsive Design Mode`

## Fejlesztési környezet

### Debug mód

A `settings.py` fájlban:
```python
DEBUG = True
```

Csak fejlesztéshez! Production környezetben mindig legyen `False`.

### Admin felület

Django admin létrehozása:
```bash
python manage.py createsuperuser
```

Admin elérése: `http://127.0.0.1:8000/admin`

### Új migráció létrehozása

```bash
python manage.py makemigrations
python manage.py migrate
```

## Teljesítmény optimalizálás

### Statikus fájlok gyűjtése (production)
```bash
python manage.py collectstatic
```

### PostgreSQL indexek
Az adatbázis modellek automatikusan indexeket hoznak létre a `variable` mezőkön a gyorsabb lekérdezésekhez.

## Hibaelhárítás

### "relation does not exist" hiba
Futtasd le a migrációkat:
```bash
python manage.py migrate
```

### Adatbázis kapcsolódási hiba
Ellenőrizd a `.env` fájl beállításait és a PostgreSQL szerver állapotát:
```bash
brew services list  # macOS
```

### Statikus fájlok nem jelennek meg
Győződj meg róla, hogy a `DEBUG = True` van beállítva fejlesztésben, vagy futtasd:
```bash
python manage.py collectstatic
```

## Licenc

Minden jog fenntartva - Sárvári Viola

## Kapcsolat

Kérdések vagy javaslatok esetén vedd fel a kapcsolatot a projekt készítőjével.
