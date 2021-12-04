# PYMONDIS
<img src="README.png" alt="Banner pymondis" style="width: 100%;"/>

Nieoficjalny wrapper api [Quatromondis](https://quatromondis.pl/)

### Fajne rzeczy
- Wszystkie zapytania są asynchroniczne z użyciem `httpx`
- Fajnie obiekty z użyciem `attrs` (nawet `repr()` działa!)
- Ponawianie nieudanych zapytań
- Epicka składnia python-a 3.10
- Cache-owanie zdjęć
- Type-hint-y

## Co możesz zrobić
- Dostać listę wszystkich aktualnych obozów
- Dostać listę wszystkich aktualnych galerii
- Dostać listę wszystkich psorów z opisami (bez biura i HY ...)
- Dostać listę wszystkich kandydatów aktualnego plebiscytu
- Zobaczyć wszystkie zdjęcia ze wszystkich galerii od początku istnienia fotorelacji!
- Zagłosować w plebiscycie
- Męczyć się debugowaniem przez 5 godzin, bo zapomniałeś dać await ;)

## Co prawdopodobnie możesz zrobić
- Zarezerwować miejsce w inauguracji
- Zamówić książkę
- Zarezerwować miejsce na obozie
- ~~Dostać informacje o rezerwacji obozu~~
- ~~Zgłosić się o pracę~~

## Instalacja
Aktualna *chyba* działająca wersja
```
pip install pymondis
```
Aktualna wersja
```
pip install git+https://github.com/Asapros/pymondis.git
```