from bs4 import BeautifulSoup as BS

html = """<ul class='my_class'>
          <li>thing one</li>
          <li>thing two</li>
          </ul>"""


soup = BS(html, "html.parser")
print(soup.prettify())
for ultag in soup.find_all('ul', {'class': 'my_class'}):
    for litag in ultag.find_all('li'):
        print(litag.text)
