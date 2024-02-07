import datetime as dt
import requests


def listy_walut(lista_temp):
    waluty = []
    for el in lista_temp[0]['rates']:
        waluty.append([
            el['currency'],
            el['code'],
            (el['bid'] + el['ask']) / 2
        ])
    return waluty

def zapytanie_o_kursy(etap_dziejow):

    # funkcja wysyła zapytanie o kursy walut
    # zwraca listę (.json) z podanego dnia lub najbliższego poprzedniego

    response = requests.get(f'http://api.nbp.pl/api/exchangerates/tables/c/'
                            f'{dt.datetime.date(etap_dziejow)}/')
    i = 0
    while response.status_code != 200:

        response = requests.get(
            f'http://api.nbp.pl/api/exchangerates/tables/c/'
            f'{dt.datetime.date(etap_dziejow - dt.timedelta(days=i))}/')

        i += 1

    return response.json()


def czy_przestepny(rok):
    if rok % 4 == 0:
        if rok % 100 != 0:
            rok_przestepny = True
        elif rok % 400 == 0 and rok % 100 == 0:
            rok_przestepny = True
    return False


def czy_poprawny_dzien(dzien, miesiac, przestepny):
    if (miesiac in [1, 3, 5, 7, 8, 10, 12] and 0 < dzien <= 31) or (miesiac in [4, 6, 9, 11] and 0 < dzien < 31):
        return True

    elif miesiac == 2 and (((0 < dzien <= 29) and przestepny) or (0 < dzien < 29)):
        return True

    else:
        return False


def czy_poprawny_miesiac(miesiac):
    if 1 <= miesiac <= 12:
        return True
    else:
        return False


def poprawna_data(dzien, miesiac, rok):
    rok_przestepny = czy_przestepny(rok)
    print(rok_przestepny)
    if not czy_poprawny_miesiac(miesiac):
        print("Błędny miesiąc")
        main()
    if not czy_poprawny_dzien(dzien, miesiac, rok_przestepny):
        print("Niepoprawny dzień")
        main()

    data_faktury = dt.datetime(rok, miesiac, dzien)

    if data_faktury < dt.datetime(2002, 1, 2):
        data_faktury = dt.datetime(2002, 1, 2)
    elif data_faktury > dt.datetime.now():
        data_faktury = dt.datetime.now()

    return data_faktury


def main():
    # poprawna_data(12, 12, 2021)
    lista = zapytanie_o_kursy(dt.datetime.now())
    print(listy_walut(lista))


if __name__ == '__main__':
    main()
