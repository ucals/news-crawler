import pytest
from crawler.wsj import *


def test_scrape_url():
    url = 'https://www.wsj.com/articles/only-a-fraction-of-russian-troll-accounts-have-been-made-public-by-social-med' \
          'ia-giants-1525448056'
    title = 'Much Remains Unknown About Russian-Troll Accounts on Social-Media Giants'
    assert title in scrape_url(url)


def test_render_chapter():
    pass


def test_retrieve_article_list():
    pass


def test_render_toc():
    pass


def test_render_ncx():
    pass


def test_render_opf():
    pass


def test_generate_mobi():
    pass


def test_send_to_kindle():
    pass
