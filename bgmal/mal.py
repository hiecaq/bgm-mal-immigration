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

from .api import AnimeWebsite, LoginFailedException

logger = logging.getLogger(__name__)


class IllegalPasswordException(Exception):
    pass


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
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'lxml')
        try:
            username = soup.find('username').string
        except Exception as e:
            logger.error("logging failed: %s", e)
            raise LoginFailedException()
        else:
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
