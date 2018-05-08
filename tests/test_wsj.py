import pytest
from crawler.wsj import *
from crawler.core import *
import crawler.pocket_api
import json, pickle
from pathlib import Path
import time


@pytest.mark.skip(reason="to speed up development")
def test_scrape_url():
    url = 'https://www.wsj.com/articles/only-a-fraction-of-russian-troll-accounts-have-been-made-public-by-social-med' \
          'ia-giants-1525448056'
    content = scrape_url(url)
    assert type(content) is str
    assert 'article' in content


@pytest.mark.skip(reason="to speed up development")
def test_render_chapter():
    title = 'Chapter test'
    content = '<article>Hello world</article>'
    html = render_chapter(title, content)
    assert '<title>Chapter test</title>' in html
    assert '<article>Hello world</article>' in html


@pytest.mark.skip(reason="to speed up development")
def test_retrieve_article_list(monkeypatch):
    def mock_pocket_data():
        with open('pocket_mock_data.json', 'r') as fp:
            return json.load(fp)

    monkeypatch.setattr(crawler.pocket_api, 'get_pocket_data', mock_pocket_data)

    with open('expected_article_list.pkl', 'rb') as fp:
        expected_list = pickle.load(fp)

    assert crawler.pocket_api.list_urls('wsj.com') == expected_list


@pytest.mark.skip(reason="to speed up development")
def test_save_article_list():
    filename = os.path.join(str(Path.home()), 'Downloads', 'pocket_data.json')
    os.remove(filename)
    crawler.pocket_api.get_pocket_data(save=True)
    assert os.path.getmtime(filename) < time.time()


@pytest.mark.skip(reason="to speed up development")
def test_render_toc(monkeypatch):
    def mock_pocket_data():
        with open('pocket_mock_data.json', 'r') as fp:
            return json.load(fp)

    monkeypatch.setattr(crawler.pocket_api, 'get_pocket_data', mock_pocket_data)

    title = 'Chapter test'
    data = crawler.pocket_api.get_domain_data('wsj.com')
    html = render_toc(title, data)
    with open('expected_toc.html', 'r') as fp:
        expected_content = fp.read()

    assert html in expected_content


def test_render_ncx():
    pass


def test_render_opf():
    pass


def test_assemble_ebook():
    pass


def test_generate_mobi():
    pass


def test_send_to_kindle():
    pass
