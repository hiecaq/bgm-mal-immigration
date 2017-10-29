# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.tests.test_mal
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for mal.py

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import pytest

from bgmal.mal import MyAnimeList, IllegalPasswordException


@pytest.mark.usefixtures("mock_mal")
class TestMyAnimeList(object):
    def test_login_fail1(self):
        with pytest.raises(IllegalPasswordException) as e:
            MyAnimeList("hello", "wor:ld")
        assert e

    def test_login_fail2(self):
        with pytest.raises(IllegalPasswordException) as e:
            MyAnimeList("hello", "wo<rld")
        assert e

    def test_login_success(self):
        b = MyAnimeList("ACCOUNT@EXAMPLE.COM", "PASSWORD")
        assert b._account == "ACCOUNT@EXAMPLE.COM"
        assert b._password == "PASSWORD"
        assert b.username == "USERNAME"

    def test_watched_list(self):
        b = MyAnimeList("ACCOUNT@EXAMPLE.COM", "PASSWORD")
        watchlist = b.watched_list()
        assert len(watchlist) == 73

        entry = watchlist[1]
        assert entry['title'] == 'Ao no Exorcist Movie'
        assert entry['score'] == 8
