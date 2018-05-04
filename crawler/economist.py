import requests, os
from bs4 import BeautifulSoup
from crawler.pocket_api import list_urls

# Parse article
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


# Save each content in a file
base_path = '/Users/carlos/Dropbox/2018/Newsletters/week-18/economist'
for index, url in enumerate(list_urls('economist.com')):
    filename = os.path.join(base_path, 'chapter-' + str(index + 1) + '.html')
    f = open(filename, 'wb')
    content = b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' \
              b'\n<html xmlns="http://www.w3.org/1999/xhtml">' \
              b'\n<head>'
    content += b'\n<title>Chapter</title>' \
               b'\n<link rel="stylesheet" href="style.css" type="text/css" />' \
               b'\n</head>' \
               b'\n<body>'
    content += stripped_economist_article(url)
    content += b'\n<div class="pagebreak"></div>'
    content += b'\n</body>' \
               b'\n</html>'

    f.write(content)
    f.close()
    print(filename)

