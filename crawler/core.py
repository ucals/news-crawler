from jinja2 import Environment, PackageLoader, select_autoescape


def render_chapter(title, content):
    env = Environment(
        loader=PackageLoader('crawler', 'templates'),
    )
    template = env.get_template('chapter_template.html')
    return template.render(title=title, content=content)
