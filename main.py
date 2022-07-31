from fastapi import FastAPI
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup as bs


class Scraper:

    def __init__(self, url):
        self.url = url


    async def scrape(self):

        session = AsyncHTMLSession()
        response = await session.get(self.url)

        await response.html.arender(timeout=10)
        page = response.html.html

        soup = bs(page, 'html.parser')
        ions = soup.find_all('ion-label', {"class": "LastPrice sc-ion-label-md-h sc-ion-label-md-s ion-color ion-color-success md hydrated"})

        response_data = {
            index: {
                "name": ion["title"].split("Last Price = ")[0],
                "price": ion["title"].split("Last Price = ")[1]
            } for index, ion in enumerate(ions)
        }

        return response_data


app = FastAPI()
scraper = Scraper("https://www.qe.com.qa/wp/mws/tabs/tab1")


@app.get("/")
async def stocks():
    response_data = await scraper.scrape()
    return {"data": response_data}
            

import uvicorn

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

