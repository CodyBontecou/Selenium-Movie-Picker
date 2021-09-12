import os
import random
import time
import json
from imdb import IMDb
from selenium import webdriver

def scrapDirectorData():
  driver = webdriver.Chrome('chromedriver')
  driver.get('https://www.elacervo.com/directores')

  for i in range(4):
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  directors = driver.find_elements_by_css_selector("a[href*='https://www.elacervo.com/post/']")

  unique_directors = []
  for link in directors:
      if (link.get_attribute("href")) not in unique_directors:
        unique_directors.append(link.get_attribute("href"))

  names = []
  for link in unique_directors:
    slug = link.split('/')[-1]
    name = slug.replace('-', ' ').title()
    names.append({"name": name})

  with open('directors.json', 'w') as outfile:
      json.dump(names, outfile)

  driver.quit()

def getMovieLists():
  file = open('directors.json',)
  data = json.load(file)
    
  movies = []
  ia = IMDb()
  for person in data:
    try:
      director = ia.search_person(person['name'])[0]
      try: 
        films = ia.get_person_filmography(director.personID)['data']['filmography']['director']
        for film in films:
          if film['kind'] == 'movie':
            try:
              if (film['year']):
                movies.append(film)
            except KeyError:
              continue
      except AttributeError:
        continue
    except IndexError:
      continue

    return movies

def writeMovieData(movies):
  with open('movies.json', 'w') as outfile:
    json.dump([{"title": movie['title'], 'year': movie['year']} for movie in movies], outfile)

def randomlySelectMovie():
  file = open('movies.json')
  data = json.load(file)
  print(random.choice(data))

def main():
    if not os.path.exists('directors.json'):
      scrapDirectorData()
    if not os.path.exists('movies.json'):
      movies = getMovieLists()
      writeMovieData(movies)
    randomlySelectMovie()

if __name__ == "__main__":
    main()

