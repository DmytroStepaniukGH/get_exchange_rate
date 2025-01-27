import requests
from datetime import datetime, timedelta

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

def get_current_exchange_rate():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()

        usd_rate = None
        eur_rate = None

        for currency in data:
            if currency['cc'] == 'USD':
                usd_rate = currency['rate']
            elif currency['cc'] == 'EUR':
                eur_rate = currency['rate']

        print(f'Курс долара: {usd_rate} грн')
        print(f'Курс євро: {eur_rate} грн')

    else:
        print(f'Помилка запиту: {response.status_code}')


def get_average_exchange_rate():

    today = datetime.today()
    three_days_ago = today - timedelta(days=3)


    start_date = three_days_ago.strftime('%Y%m%d')
    end_date = (today - timedelta(days=1)).strftime('%Y%m%d')

    url_usd = (f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={start_date}'
               f'&end={end_date}&valcode=usd&sort=exchangedate&order=desc&json')

    url_eur = (f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={start_date}'
               f'&end={end_date}&valcode=eur&sort=exchangedate&order=desc&json')

    response_usd = requests.get(url_usd, headers=HEADERS)
    response_eur = requests.get(url_eur, headers=HEADERS)

    if response_usd.status_code == 200 and response_eur.status_code == 200:
        data_usd = response_usd.json()
        data_eur = response_eur.json()

        if data_usd and data_eur:
            usd_rates = [entry['rate'] for entry in data_usd]
            eur_rates = [entry['rate'] for entry in data_eur]

            avg_usd_rate = sum(usd_rates) / len(usd_rates)
            avg_eur_rate = sum(eur_rates) / len(eur_rates)

            print(f'Середній курс долара за останні 3 дні: {avg_usd_rate:.4f} грн')
            print(f'Середній курс євро за останні 3 дні: {avg_eur_rate:.4f} грн')
        else:
            print('Не знайдено даних для обох валют.')
    else:
        print(f'Помилка запиту: {response_usd.status_code}, {response_eur.status_code}')

if __name__ == '__main__':
    get_current_exchange_rate()
    print('\n')
    get_average_exchange_rate()