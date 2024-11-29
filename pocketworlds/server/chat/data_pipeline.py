"""
Author: Adam Loeckle
Date: 11/26/2024

"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Optional

COLLECTION_PATTERN = re.compile(r'https://support\.highrise\.game/en/collections/\d+-[\w-]+')
ARTICLE_PATTERN = re.compile(r'https://support\.highrise\.game/en/articles/\d+-[\w-]+')

class DataPipeline:

    def __init__(self) -> None:
        """
        Initializes the DataPipeline class.
        
        Creates a session object for managing HTTP requests.
        """
        self.session = requests.Session()
    
    def _get_collection_urls(self) -> List[str]:
        """
        Fetches collection URLs from the main Highrise support page.

        This function sends an HTTP GET request to the Highrise support home page, 
        parses the HTML for all anchor tags, and filters the links using the 
        COLLECTION_PATTERN regex.

        :return: A list of unique collection URLs matching the COLLECTION_PATTERN.
        :raises: Prints an error message if the request fails or an unexpected error occurs.
        """
        try:
            response = self.session.get("https://support.highrise.game/en/")
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            collection_urls = set()
            links = soup.find_all('a', href=True)

            for link in links:
                href = link["href"]

                if COLLECTION_PATTERN.match(href):
                    collection_urls.add(href)
            
            return list(collection_urls)

        except requests.RequestException as e:
            print(f"Failed to fetch collection urls: {str(e)}")
        except Exception as e:
            print(f"Unexpeceted error: {str(e)}")


    def _get_article_urls(self, collection_url: str) -> List[str]:
        """
        Fetches article URLs from a given collection URL.

        This function sends an HTTP GET request to the specified collection page, 
        parses the HTML for anchor tags, and filters the links using the 
        ARTICLE_PATTERN regex.

        :param collection_url: The URL of a specific collection page.
        :return: A list of unique article URLs matching the ARTICLE_PATTERN.
        :raises: Prints an error message if the request fails or an unexpected error occurs.
        """
        try:
            response = self.session.get(collection_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            article_urls = set()
            links = soup.find_all('a', href=True)

            for link in links:
                href = link["href"]
                if ARTICLE_PATTERN.match(href):
                    article_urls.add(href)
            
            return list(article_urls)

        except requests.RequestException as e:
            print(f"Failed to fetch article urls: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

    def get_urls(self) -> List[str]:
        """
        Fetches all article URLs from the Highrise support website.

        This function first retrieves all collection URLs using `_get_collection_urls`, 
        then iterates through each collection URL to fetch the corresponding article URLs.

        :return: A combined list of all article URLs found across all collections.
        """
        collection_urls = self._get_collection_urls()
        all_article_urls = []
        for collection_url in collection_urls:
            all_article_urls.extend(self._get_article_urls(collection_url=collection_url))
            
        return all_article_urls