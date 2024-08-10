import requests
import pandas as pd


url = 'http://127.0.0.1:5000/standings?season=2017/2018'

response = requests.get(url)


if response.status_code == 200:

    response_json = response.json()

    dataframe = pd.DataFrame(response_json)

    print(dataframe)
else:
    print('URL status not 200.')

