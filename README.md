Opis projektu DevOps

Projekt polega na stworzeniu prostego, ale kompletnego srodowiska DevOps, ktore umozliwia budowanie, uruchamianie oraz testowanie aplikacji z wykorzystaniem narzedzi takich jak Docker, Docker Compose oraz GitHub Actions.
Aplikacja realizuje funkcjonalnosc zarzadzania lista zadan (Task Manager) i sklada sie z backendu, frontendu oraz bazy danych.

docker-compose.yml

Plik docker-compose.yml sluzy do uruchamiania calego srodowiska aplikacji.
Dzieki niemu nie trzeba uruchamiac kazdego kontenera osobno, poniewaz wszystkie uslugi sa opisane w jednym miejscu.
W projekcie docker-compose uruchamia dwa kontenery:
-kontener z aplikacja backendowa (API)
-kontener z baza danych PostgreSQL
Kontener aplikacji laczy sie z baza danych za pomoca wewnetrznej sieci Dockera.
Dane bazy danych sa zapisywane wwolumenie Dockera, co oznacza, ze nie sa tracone po restarcie kontenerow ani po restarcie Dockera.

Takie podejscie jest zgodne z dobrymi praktykami DevOps, poniewaz oddziela aplikacje od bazy danych i pozwala latwo odtworzyc cale srodowisko na innym komputerze.

Dockerfile

Plik Dockerfile opisuje sposob budowania obrazu aplikacji.
Zostal on przygotowany jako wieloetapowy (multi-stage), co bylo jednym z wymagan projektu.

W pierwszym etapie przygotowywane sa zaleznosci aplikacji Pythona.
Ten etap sluzy tylko do budowania i nie trafia do obrazu koncowego.

W drugim etapie tworzony jest finalny obraz aplikacji, ktory zawiera jedynie:
-srodowisko uruchomieniowe Pythona
-zainstalowane zaleznosci
-kod aplikacji
Dzieki temu obraz jest mniejszy, czystszy i bezpieczniejszy.
Aplikacja jest uruchamiana przy pomocy serwera Uvicorn, ktory obsluguje przychodzace zapytania HTTP.

app/main.py
Plik main.py jest glownym plikiem aplikacji backendowej.
To w nim tworzona jest instancja FastAPI oraz definiowane sa wszystkie endpointy REST API.
Plik ten odpowiada miedzy innymi za:
obsluge zapytan HTTP
logike endpointow do zarzadzania zadaniami
udostepnienie prostego interfejsu frontendowego (HTML + JavaScript)
inicjalizacje tabel w bazie danych przy starcie aplikacji

Mozna powiedziec, ze jest to centralny punkt aplikacji, ktory laczy wszystkie pozostale elementy.

app/db.py
Plik db.py zawiera konfiguracje polaczenia z baza danych.
Zostal wydzielony po to, aby logika aplikacji byla oddzielona od konfiguracji infrastrukturalnej.
W pliku tym:
tworzony jest silnik SQLAlchemy
definiowana jest fabryka sesji bazy danych
zdefiniowana jest klasa bazowa dla modeli ORM
Takie rozwiazanie ulatwia dalszy rozwoj aplikacji i poprawia czytelnosc kodu.

app/models.py
Plik models.py zawiera definicje struktury danych aplikacji.
Zdefiniowany jest w nim model zadania (Task), ktory odpowiada tabeli w bazie danych.
Model zawiera miedzy innymi:
identyfikator zadania
tytul
status (todo, in_progress, done)
daty utworzenia i modyfikacji
Dzieki zastosowaniu ORM struktura bazy danych jest tworzona automatycznie.

app/crud.py

Plik crud.py zawiera logike operacji na bazie danych.
To tutaj znajduja sie funkcje odpowiedzialne za tworzenie, pobieranie, aktualizacje oraz usuwanie zadan.

Oddzielenie tej logiki od pliku main.py sprawia, ze kod jest bardziej uporzadkowany i latwiejszy do testowania.

app/static/index.html

Plik index.html jest prostym frontendem aplikacji.
Zostal napisany w czystym HTML i JavaScript, bez dodatkowych frameworkow.

Interfejs umozliwia:

dodawanie nowych zadan
zmiane statusu zadan
usuwanie zadan

podglad odpowiedzi serwera w panelu debug
Frontend komunikuje sie z backendem wylacznie za pomoca REST API, tak samo jak narzedzia typu curl czy PowerShell.

.github/workflows
Katalog .github/workflows zawiera konfiguracje pipeline CI/CD w GitHub Actions.

Pipeline:

uruchamia testy i linting
buduje obraz Dockera
publikuje obraz do rejestru
posiada oddzielne workflow dla pull requestow oraz glownego brancha
wykorzystuje reusable workflows
Dzieki temu proces budowania i testowania aplikacji jest w pelni zautomatyzowany.

requirements.txt

Plik requirements.txt zawiera liste bibliotek Pythona wymaganych do uruchomienia aplikacji.
Jest wykorzystywany zarowno lokalnie, jak i w Dockerze oraz pipeline CI.

Podsumowanie

Projekt pokazuje praktyczne zastosowanie narzedzi DevOps w niewielkiej, ale kompletnej aplikacji.
Zawiera backend, frontend, baze danych, konteneryzacje oraz automatyzacje CI/CD.
Cala architektura jest zgodna z dobrymi praktykami i spelnia wymagania przedmiotu.