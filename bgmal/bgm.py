# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.bgm
    ~~~~~~~~~~~~~~~~~~~~~~~

    Deal with the bangumi APIs

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import logging
import time

import requests
from bs4 import BeautifulSoup

from .api import AnimeWebsite, LoginFailedException

logger = logging.getLogger(__name__)


class Bangumi(AnimeWebsite):
    """Manipulate the bgm api"""

    def __init__(self, account, password):
        """Construct a bangumi object with given account and password

        :param str account: user's email address
        :param str password: user's password
        :returns: a ``Bangumi`` object

        """
        data = {
            'password': password,
            'username': account,
            'auth': 0,
            'sysuid': 0,
            'sysusername': 0
        }
        url = 'https://api.bgm.tv/auth?source=onAir'
        r = requests.post(url, data=data)
        r.raise_for_status()

        output = r.json()

        try:
            self._uid = output['username']
            self._auth = output['auth']
        except Exception as e:
            logger.error("logging failed: %s", e)
            raise LoginFailedException()

    def watched_list(self):
        """Return the watched list of anime

        :returns: a list of anime entries, described in dict of name and score

        """
        url = 'https://bgm.tv/anime/list/{0}/collect'.format(self._uid)
        page = 1
        watched = []
        while True:
            r = requests.get(url, params={'page': page})
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'lxml')
            items = soup.find_all('li', class_='item')
            for item in items:
                anime = Bgmanime(item)
                watched.append({'title': anime.title, 'score': anime.score})
            if not Bangumi._has_next_page(soup):
                break
            page += 1
            time.sleep(1)

        return watched

    @classmethod
    def _has_next_page(cls, soup):
        """Return if this page have a next page.

        :param BeautifulSoup soup: the soup of the given page
        :returns: True or False

        """
        pages = soup.find(class_='page_inner')
        return pages.find_all(class_='p')[-1].string == '››'


class Bgmanime(object):
    """One entry for one anime from Bangumi"""

    def __init__(self, item):
        """

        :type tag: bs4.element.Tag
        :returns: a ``Bgmanime`` object

        """
        self._item = item

    @property
    def score(self):
        """Return the user's score of this anime
        :returns: score
        :rtype: int

        """
        starsinfo = self._item.find(class_='starsinfo')['class']
        stars = (
            starsinfo[0] if starsinfo[0] != 'starsinfo' else starsinfo[-1]
        )
        return int(stars[6:])

    @property
    def title(self):
        """Return the title of this anime
        :returns: title of this anime
        :rtype: str

        """
        return (
            self._item.find(class_='grey').string
            if self._item.find(class_='grey') is not None else
            self._item.find(class_='l').string
        )
