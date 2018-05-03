import requests
from bs4 import BeautifulSoup
from pocket_api import list_urls


def stripped_economist_article(url):
    page = requests.get(url)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    article = soup.find('article')

    # Removing non-content
    for val in article.select('.blog-post__asideable-wrapper'):
        val.decompose()
    for val in article.select('.newsletter-form.newsletter-form--inline'):
        val.decompose()
    for val in article.select('.latest-updates-panel__container.latest-updates-panel__container--blog-post'):
        val.decompose()
    for val in article.select('.blog-post__bottom-panel'):
        val.decompose()
    for val in article.select('.ad-panel__container--block'):
        val.decompose()

    # Formatting headers
    for val in article.select('.blog-post__rubric'):
        new_tag = soup.new_tag('h3')
        new_tag.string = val.get_text()
        val.replace_with(new_tag)

    for val in article.select('.xhead'):
        new_tag = soup.new_tag('h4')
        new_tag.string = val.get_text()
        val.replace_with(new_tag)

    # Format hero image
    for val in article.select('.component-image__img.blog-post__image-block'):
        new_tag = soup.new_tag('img')
        new_tag.attrs['src'] = val.attrs['src']
        val.replace_with(new_tag)

    return article.prettify("latin-1")


large_file = '/Users/carlos/Downloads/economist_articles.html'
f = open(large_file, 'wb')
for url in list_urls('economist.com'):
    content = stripped_economist_article(url)
    content += b"\n<hr>"
    f.write(content)

f.close()
