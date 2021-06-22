import lxml.html
import requests


class Krisa:

    _headers = {
        'authority': 'krisha.kz',
        'sec-ch-ua': '"Opera";v="77", "Chromium";v="91", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'referer': 'https://krisha.kz/',
        'accept-language': 'ru-ru,ru;q=0.8,en-us;q=0.6,en;q=0.4',
    }

    def __init__(self) -> None:
        self._session = requests.session()

    def get_haty(self, search_url: str) -> list:
        response = self._session.get(search_url, headers=self._headers, timeout=120)
        code_of_the_page = response.text

        dom = lxml.html.fromstring(code_of_the_page)
        items = dom.xpath('/html/body/main/section[3]/div/section[1]/div')

        result = []
        for item in items:
            try:
                href = item.xpath('div/div/div[1]/div[1]/div[1]/a')[0].attrib['href']
            except IndexError:
                pass
            else:
                result.append('https://krisha.kz' + href)

        return result
