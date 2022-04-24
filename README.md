# PYMONDIS
<img src="banner.png" alt="(Banner pymondis)" style="width: 100%;"/>

Nieoficjalny wrapper api [Quatromondis](https://quatromondis.pl/) w pythonie

## Fajne rzeczy
- Wszystkie zapytania są asynchroniczne z użyciem `httpx`
- Moduł ``shell`` udostępnia prosty interfejs do używania biblioteki bez konieczności tworzenia asynchronicznej funckji
- Fajnie obiekty z użyciem `attrs` (nawet *repr()* działa!)
- Ponawianie nieudanych zapytań
- Epicka składnia pythona 3.10 (dlatego na razie można korzystać tylko z 3.10)
- Cache'owanie zdjęć
- Type hinty

## Co możesz zrobić
- Dostać listę wszystkich aktualnych obozów
- Dostać listę wszystkich aktualnych galerii
- Dostać listę wszystkich zamków z aktywną fotorelacją
- Dostać listę wszystkich psorów z opisami (bez biura i HY)
- Dostać listę wszystkich kandydatów plebiscytów od 2019
- Zagłosować w plebiscycie
- Pobrać wszystkie zdjęcia z [aktualnych](#old-galleries-deleted) galerii 
- Męczyć się debugowaniem przez 5 godzin, bo zapomniałeś dać *await* ;)

## Czego już nie możesz zrobić ;(
<a name="old-galleries-deleted"></a>
- Do początku 2022 można było zobaczyć fotorelację nawet z 2019 roku, ale już bloby zaczęły znikać.
To była główna funkcjonalność biblioteki — pobieranie starych niedostępnych na stronie zdjęć,
ale informatycy pożałowali miejscem na dysku i je usunęli. Przepraszam wszystkich którzy przyszli tutaj z nadzieją
odtworzenia swoich dawnych wspomnień. Polecam pobierać całe galerie, póki jeszcze nie zostały usunięte, na szczęście
zdążyłem pobrać zdjęcia ze swoich wszystkich starych turnusów.

## Co prawdopodobnie możesz zrobić
- Zarezerwować miejsce w inauguracji
- Zamówić książkę
- Zarezerwować miejsce na obozie
- ~~Dostać informacje o rezerwacji obozu~~
- ~~Zgłosić się o pracę~~

## Instalacja
Aktualna *chyba* działająca wersja
```shell
pip install pymondis
```
Aktualna wersja
```shell
pip install git+https://github.com/Asapros/pymondis.git
```

