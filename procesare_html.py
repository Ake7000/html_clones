from bs4 import BeautifulSoup

def parse_html(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    #removing not relevant elements that are not visible
    for tag in soup(["script", "style", "nonscript"]):
        tag.extract()

    #extracting visible text
    text = soup.get_text(separator = " ", strip = True)
    return text