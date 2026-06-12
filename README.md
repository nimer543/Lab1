# TravelPlanner — Platforma do planowania podróży

Projekt to prosta aplikacja internetowa do planowania wyjazdów i kontrolowania wydatków. Jest napisana w Pythonie przy użyciu FastAPI oraz bazy danych SQLite. Całość została stworzona zgodnie z wzorcem architektonicznym MVC.

## Co potrafi aplikacja

Aplikacja pozwala na wygodne zarządzanie swoimi wyjazdami. Możesz dodawać nowe podróże, określać ich cel, czas trwania oraz planowany budżet.

Wewnątrz każdej podróży możesz dodawać konkretne rezerwacje, takie jak noclegi, transport czy bilety na atrakcje. Aplikacja automatycznie sumuje koszty wszystkich rezerwacji, pokazuje ile wolnych środków zostało z założonego budżetu i ostrzega, jeśli przekroczysz planowane wydatki.

Na stronie głównej dostępne jest wyszukiwanie podróży po nazwie oraz filtrowanie według budżetu. Wszystkie formularze posiadają walidację danych. Na przykład system nie pozwoli wpisać daty zakończenia wyjazdu wcześniejszej niż data rozpoczęcia.

## Struktura folderów w projekcie

Projekt jest podzielony na przejrzyste części:

* app/models — tutaj znajdują się pliki odpowiadające za bazę danych SQLite i tabele podróży oraz rezerwacji (warstwa Model).
* app/views — tutaj są szablony stron HTML oraz pliki CSS i JS, które odpowiadają za to, co widzi użytkownik (warstwa View).
* app/controllers — te pliki obsługują zapytania z przeglądarki, pobierają dane z bazy i przesyłają je na odpowiednie strony (warstwa Controller).
* app/schemas — pliki walidacji danych za pomocą biblioteki Pydantic.
* tests — folder zawierający automatyczne testy jednostkowe.

## Jak uruchomić projekt na komputerze

Aby uruchomić aplikację lokalnie, musisz mieć zainstalowanego Pythona w wersji 3.9 lub nowszej.

Kroki instalacji:

1. Wejdź do katalogu z projektem w terminalu:
   cd "/Users/nimer/Documents/Project MVC"

2. Utwórz środowisko wirtualne:
   python3 -m venv venv

3. Aktywuj środowisko wirtualne:
   source venv/bin/activate

4. Zainstaluj potrzebne biblioteki:
   pip install -r requirements.txt

5. Uruchom serwer aplikacji:
   uvicorn app.main:app --reload

6. Otwórz aplikację w przeglądarce pod adresem: http://127.0.0.1:8000

## Uruchomienie przy użyciu Docker

Jeśli wolisz skorzystać z Dockera i masz zainstalowany program Docker Desktop, możesz uruchomić projekt jednym poleceniem.

Wystarczy wejść do folderu projektu w terminalu i wpisać:
docker-compose up --build

Po zbudowaniu kontenera strona będzie dostępna pod tym samym adresem: http://127.0.0.1:8000

## Jak uruchomić testy

Aby sprawdzić czy wszystko działa prawidłowo i przechodzi testy walidacji, wpisz w terminalu (przy aktywnym środowisku wirtualnym):
pytest -v
