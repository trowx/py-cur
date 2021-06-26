from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

headers = {
    'User-Agent': 'My User Agent 1.0'
}

jsx = """{
  "app": [
    {
      "groups": [
        {
          "dolar_alis": "d_alis_null",
          "dolar_satis": "d_satis_null",
        },
        {
          "euro_alis": "e_alis_null",
          "euro_satis": "e_satis_null",
        }
      ]
    }
  ]
}"""


def getDoEu(url, de):
    global jsx
    page = requests.get(
        url,
        headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    data = soup.find_all('div', class_='value2 satis')
    dat = str(data)
    dat = dat.replace('[<div class="value2 satis">SATIŞ FİYATI: <span>', '')
    dat = dat.replace('</span></div>]', '')

    data2 = soup.find_all('div', class_='value2 alis')
    dat2 = str(data2)
    dat2 = dat2.replace('[<div class="value2 alis">ALIŞ FİYATI: <span>', '')
    dat2 = dat2.replace('</span></div>]', '')

    if de:
        jsx = jsx.replace("d_satis_null", dat)
        jsx = jsx.replace("d_alis_null", dat2)
    else:
        jsx = jsx.replace("e_satis_null", dat)
        jsx = jsx.replace("e_alis_null", dat2)


@app.route('/')
def getCurrency():
    getDoEu("http://bigpara.hurriyet.com.tr/doviz/dolar-ne-kadar/", True)
    getDoEu("https://bigpara.hurriyet.com.tr/doviz/euro-ne-kadar/", False)
    return jsx
