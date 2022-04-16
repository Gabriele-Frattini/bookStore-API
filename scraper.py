from http.client import HTTPException
import bs4
from bs4 import BeautifulSoup
import requests
import time
from fastapi import status, HTTPException


class Scraper:

    def __init__(self, isbn, bookTitle):
        self.isbn = isbn
        self.bookTitle = bookTitle

    def studentapan(self):
        # studentapan
        url = f"https://www.studentapan.se/kurslitteratur/{self.bookTitle}-{self.isbn}?"
        htmldata = requests.get(url).text
        soup = BeautifulSoup(htmldata, "html.parser")

        price = soup.find('span', {'class': 'Textbook__price__main'})

        if price is not None:
            price = int(price.text.split(" ")[0])
            return {'price': price, 'url': url}

        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def campusbokhandeln(self):

        url = f"https://campusbokhandeln.se/b/{self.isbn}/{self.bookTitle}?"
        htmldata = requests.get(url).text
        soup = BeautifulSoup(htmldata, "html.parser")

        price_list = []
        child_soup = soup.find('div', {'id': 'interaction'})

        if child_soup is not None:
            for child in child_soup.find_all('span', {'class': 'p'}):
                try:
                    price = eval(child.text.split(" ")[0])
                    price_list.append(price)
                except:
                    pass
            price = min(price_list)

            return {'price': price, 'url': url}

        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def cheapestBook(self):
        studentapan = self.studentapan()
        campusbokhandeln = self.campusbokhandeln()

        price = min(studentapan["price"], campusbokhandeln["price"])

        if price == studentapan["price"]:
            url = studentapan["url"]
            company = "studentapan"

        url = campusbokhandeln["url"]
        company = "campusbokhandeln"

        data = {
            'isbn': self.isbn,
            'bookTitle': self.bookTitle,
            'company': company,
            'price': price,
            'url': url
        }

        return data


#data = Scraper(isbn="9789147138227", bookTitle="civilratt")