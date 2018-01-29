# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.mal
    ~~~~~~~~~~~~~~~~~~~~~~~

    Deal with the MAL APIs

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import json
import logging

import requests
from bs4 import BeautifulSoup

from .api import AnimeItem, AnimeWebsite, LoginFailedException

logger = logging.getLogger(__name__)


class IllegalPasswordException(Exception):
    pass


def _search(title):
    """Search and return an ``AnimeItem`` object representing the result.

    :param str title: the title user wish to search.
    :returns: an dict contains interesting informations.

    """
    r = requests.get(
        'https://myanimelist.net/search/prefix.json',
        params={
            'type': 'anime',
            'keyword': title
        }
    )
    r.raise_for_status()
    data = json.loads(r.text)
    # assume the first one is the closest result
    return data['categories'][0]['items'][0]


class MyAnimeList(AnimeWebsite):
    """Manipulate the MAL api"""

    def __init__(self, account, password):
        """Construct a MyAnimeList object with given account and password

        :param str account: user's email address
        :param str password: user's password

        """
        self._account = account
        if (':' in password or '<' in password):
            raise IllegalPasswordException(
                "Error: password with ':' or '<' "
                "cannot be used for API authentation."
            )
        self._password = password
        self.username = self._get_username()

    def _get_username(self):
        """Get the username of this user.
        :returns: username
        :rtype: str

        """
        url = 'https://myanimelist.net/api/account/verify_credentials.xml'
        r = requests.get(url, auth=(self._account, self._password))
        soup = BeautifulSoup(r.content, 'lxml')
        try:
            r.raise_for_status()
        except Exception as e:
            logger.error("logging failed: %s", e)
            raise LoginFailedException()
        else:
            username = soup.find('username').string
            return username

    def watched_list(self):
        """Return the watched list of anime

        :returns: a list of anime entries, described in dict of name and score

        """
        r = requests.get(
            "https://myanimelist.net/animelist"
            "/{0}?status=2".format(self.username)
        )
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'lxml')
        items = soup.find(class_='list-table')['data-items']
        data = json.loads(items)
        return [{
            'title': entry['anime_title'],
            'score': entry['score']
        } for entry in data]

    def search(self, title):
        """Search and return an ``AnimeItem`` object representing the result.

        :param str title: the title user wish to search.
        :returns: an ``AnimeItem`` object representing the search result.
        :rtype: AnimeItem

        """
        item = _search(title)
        return AnimeItem(
            title=MyAnimeList._get_japanese_name(item['url']),
            score=float(item['payload']['score']),
            userscore=None
        )

    @classmethod
    def _get_japanese_name(cls, url):
        """Get the japanese name of the anime in this url.

        :param str url: The given url of this anime.
        :returns: the name of this anime.
        :rtype: str

        """

        def is_japanese_name(x):
            target = x.find('span', class_='dark_text')
            return target is not None and target.string == "Japanese:"

        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")
        jpname = list(
            filter(is_japanese_name, soup.find_all(class_='spaceit_pad'))
        )
        return (
            jpname[-1].contents[-1].strip() if len(jpname) > 0 else
            soup.find('span', attrs={
                'itemprop': 'name'
            }).string
        )

    def mark_as_watched(self, anime_item):
        """Mark the given anime as watched with the given score, return true
        if this call succeeds.

        :param AnimeItem title: an AnimeItem that the user want to mark
        as watched.
        :returns: true or false
        :rtype: bool

        """
        anime_item.title
