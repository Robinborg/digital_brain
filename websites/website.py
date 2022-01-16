if __name__ == "__main__" and __package__ is None:
    import sys
    from os import path
    path_name = path.dirname(path.abspath(__file__)) + "/.."
    sys.path.append(path_name)
from database.connection import connect_database
from utils.insert_database import insert_db
from bs4 import BeautifulSoup
import requests
from typing import List

class WebSearch:
    def __init__(self):
        self.website_connection = connect_database(websites = True)

    def open_website(self, insert_link: str) -> BeautifulSoup:
        site = requests.get(insert_link)
        soup = BeautifulSoup(site.content, "html.parser")
        return soup.prettify()

    def get_all_links(self,
                      website_prettified: BeautifulSoup)-> List[str]:
        all_links = [a["href"]
                     for a in website_prettified('a')
                     if a.hast_attr("href")]
        return all_links

    def insert_database(self, enter_mode: int):
        if enter_mode == 1:
            website_name = input("Enter website:\n")
            cleaned_website = self.open_website(website_name)
            sweep_links = self.get_all_links(cleaned_website)
            insert_website = insert_db(write=website_name,
                                       review=sweep_links)
            push_db = self.website_connection.insert_one(insert_website)
            return print(f"Inserted one: {push_db.inserted_id}")
        if enter_mode == 2:
            website_name = input("Enter website\n")
            insert_website = insert_db(write=website_name)
            push_db = self.website_connection.insert_one(insert_website)
            return print(f"Inserted one: {push_db.inserted_id}")


        

        

