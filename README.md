# PYMONDIS
Unofficial [Quatromondis](https://quatromondis.pl/) api

## CAUTION!
1. The whole documentation is written in Polish
2. This project is meant for [_Quatromondis_](https://quatromondis.pl/) community
3. Don't bother with the repository, if you're not a part of it, or you just don't know the language in general

### Fajne rzeczy
- Wszystkie zapytania są asynchroniczne z użyciem `httpx`
- Fajnie obiekty z użyciem `attrs` (nawet `str()` działa!)
- Ponawianie nieudanych zapytań z użyciem `backoff`
- Abstrakcyjne podłoże każdej klasy pozwalające na jej własne implementacje
- Epicka składnia pythona 3.10
- Cache'owanie zdjęć
- Type-hinty

## Co możesz zrobić
- Dostać listę wszystkich aktualnych obozów
- Dostać listę wszystkich aktualnych galerii
- Dostać listę wszystkich psorów z opisami (bez biura i HY ...)
- Dostać listę wszystkich kandydatów aktualnego plebiscytu (z opisami)
- Zobaczyć wszystkie zdjęcia ze wszystkich galerii od początku istnienia fotorelacji!
- Zagłosować w plebiscycie
- Męczyć się debugowaniem przez 5h, bo zapomniałeś dać await

## Co prawdopodobnie możesz zrobić
- Zarezerwować miejsce w inauguracji
- Zamówić książkę
- Zarezerwować miejsce na obozie
- Zarządzać rezerwacją obozu