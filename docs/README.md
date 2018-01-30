bgm-mal-immigration
====================

Immigrate automatically between [Bangumi][bgm] and [MyAnimeList][mal].

Specification
--------------------


Due to the limitation of APIs, this scripts is highly unpredictable in that it could mark some specials instead
of the real series. So far, only `bgm2mal` is implemented.

Usage
--------------------

```bash
bgm_mal_immigration [-h] (--bgm2mal | --mal2bgm) [-f JSON]
                           [-o SAVEFILE] [-i SAVEFILE]
```

See `bgm_mal_immigration --help` for details.

Requirements
--------------------

`bgm_mal_immigration` only support `python3`, and is only tested under `python3.6`.

Installation
--------------------

```bash
git clone https://github.com/quinoa42/bgm-mal-immigration.git
cd bgm-mal-immigration
make install
```

[mal]:https://myanimelist.net/ "https://myanimelist.net/"

[bgm]:https://bgm.tv "https://bgm.tv"
