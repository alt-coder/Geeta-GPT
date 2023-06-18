import requests , os ,re
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://www.holy-bhagavad-gita.org'
chapter_number = 1
verse = 1
def write_to_file(filename, content):
    currdir = os.path.dirname(filename) if  len(os.path.dirname(filename)) > 0 else './'
    os.makedirs( currdir ,exist_ok=True)
    with open(filename,'w') as f:
        f.write(content)
def get_total_verse(chapter):

    result = dict()
    url = BASE_URL+'/chapter/'+str(chapter)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    verses = soup.find_all('span', class_='verseSmall')
    # urls = []

    for verse in verses:
        link = verse.find('a').get('href')
        result[verse.text.strip()] = BASE_URL+link
    st = json.dumps(result, indent=4)

    write_to_file(f'chapter{chapter}.json',st)
    return result

def get_by_id(soup,id,chapter='',verse=''):
    try:
        transliteration_element = soup.find('div', id=id)
        text= transliteration_element.text.strip()
    except:
        print(f'error occoured at chapter{chapter} verse {verse}')
        text=''
    return text
def write_chapter(chapter):
    
    urls = get_total_verse(chapter=chapter)

    for verse,url in urls.items():
        # try:
            content = requests.get(url).content
            soup = BeautifulSoup(content, "html.parser")
            transliteration=get_by_id(soup,"transliteration",chapter,verse)
            translation = get_by_id(soup,"translation",chapter,verse)
            commentary = get_by_id(soup,'commentary',chapter,verse)
            final_text=f'Transliteration:\n{transliteration}\n\nTranslation:\n{translation}\n\nCommentary:\n{commentary}'
            write_to_file(os.path.join('Book',f'chapter{chapter}',f'{verse}.txt'),final_text)
            
        # except:
            # print(f'error occoured at chapter{chapter} verse {verse}')


if __name__ == "__main__":
    for i in range(1,19):
        write_chapter(i)
    # print()   
    