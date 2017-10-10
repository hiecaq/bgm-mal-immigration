# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.api
    ~~~~~~~~~~~~~~~~~~~~~~~

    Defines ABCs for bgm and mal module

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from abc import ABC, abstractmethod


class AnimeWebsite(ABC):
    """AnimeWebsite is an ABC defined generally for potentially all
    shared features among Bangumi, MyAnimeList, etc
    """

    @abstractmethod
    def __init__(self, account, password):
        """Construct an AnimeWebsite object with given account and password

        :param str account: user's account
        :param str password: user's password

        """
        pass

    @abstractmethod
    def watched_list(self):
        """Return the watched list of anime

        :returns: A list of dict, with field str `title` and int `score`

        """
        pass
