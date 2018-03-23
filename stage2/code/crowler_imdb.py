
# coding: utf-8

# In[2]:




import csv
import requests
from bs4 import BeautifulSoup
import re

def spider(page_no, movie_no_initial, debug_en):
    
    url = "https://www.imdb.com/search/title?title_type=feature&sort=moviemeter,asc&page={}".format(page_no)
    print "** page {} starts **".format(page_no)
    print url

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser") 
    
    content = soup.find_all('div', 'lister-item mode-advanced')
    movie_no = movie_no_initial
    for c1 in content:
        movie_table.append([])
        movie_no = movie_no + 1
        
        # 1st part of the webpage
        c2 = c1.find_all('h3', 'lister-item-header')
        for c3 in c2:
            movie_name = c3.find('a').text.encode('ascii','ignore')
            movie_year = c3.find('span', 'lister-item-year').text.replace('(', '').replace(')', '').encode('ascii','ignore')

            movie_table[movie_no].append(movie_no)
            movie_table[movie_no].append(movie_name)
            movie_table[movie_no].append(movie_year)

        # 2nd part of the webpage
        c2 = c1.find_all('p', 'text-muted')
        movie_cert_no = 0
        movie_runtime_no = 0
        movie_genre_no = 0
        for c3 in c2:
            movie_cert_tmp = c3.find('span', 'certificate')
            movie_runtime_tmp = c3.find('span', 'runtime')
            movie_genre_tmp = c3.find('span', 'genre')

            if movie_cert_tmp != None:
                movie_cert_no = movie_cert_no + 1
                movie_cert = movie_cert_tmp
                
            if movie_runtime_tmp != None:
                movie_runtime_no = movie_runtime_no + 1
                movie_runtime = movie_runtime_tmp
                
            if movie_genre_tmp != None:
                movie_genre_no = movie_genre_no + 1
                movie_genre = movie_genre_tmp

        if movie_cert_no == 1:
            movie_table[movie_no].append(movie_cert.text.encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_cert_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
            
        if movie_runtime_no == 1:
            movie_table[movie_no].append(movie_runtime.text.encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_runtime_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
            
        if movie_genre_no == 1:
            movie_table[movie_no].append(movie_genre.text.replace('\n', '').strip().encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_genre_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
            
        # 3rd part of the webpage
        c2 = c1.find_all('div', 'ratings-bar')
        movie_rating_no = 0
        for c3 in c2:
            movie_rating_tmp = c3.find('strong')

            if movie_rating_tmp != None:
                movie_rating_no = movie_rating_no + 1
                movie_rating = movie_rating_tmp

        if movie_rating_no == 1:
            movie_table[movie_no].append(movie_rating.text.encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_rating_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
                
        # 4th part of the webpage
        c2 = c1.find_all('p', "sort-num_votes-visible")
        movie_gross_no = 0
        for c3 in c2:
            movie_gross_cap = c3.find_all('span')[-2]
            movie_gross_tmp = c3.find_all('span')[-1]
            
            if movie_gross_cap.text == 'Gross:':
                movie_gross_no = movie_gross_no + 1
                movie_gross = movie_gross_tmp

        if movie_gross_no == 1:
            movie_table[movie_no].append(movie_gross.text.encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_gross_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
 
        # 5th part of the webpage
        c2 = c1.find_all('p', "")
        movie_director_no = 0
        movie_star_no = 0
        for c3 in c2:
            match1 = re.search(r'(Director:)([\w\W]*)(Stars:)', c3.text)
            match2 = re.search(r'(Directors:)([\w\W]*)(Stars:)', c3.text)
            
            match_star = re.search(r'(Stars:)([\w\W]*)', c3.text)
            
            if match1 != None:
                movie_director = match1.group(2).strip().replace('|', '').replace('\n', '')
                movie_director_no = movie_director_no + 1
            elif match2 != None:
                movie_director = match2.group(2).strip().replace('|', '').replace('\n', '')
                movie_director_no = movie_director_no + 1
                
            if match_star != None:
                movie_star = match_star.group(2).strip().replace('\n', '')
                movie_star_no = movie_star_no + 1
        
        if movie_director_no == 1:
            movie_table[movie_no].append(movie_director.encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_director_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
            
        if movie_star_no == 1:
            movie_table[movie_no].append(movie_star.encode('ascii','ignore'))
        else:
            if debug_en == 1:
                print('{}: movie_star_no != 1'.format(movie_no))
            movie_table[movie_no].append('')
            
movie_table = []
with open('imdb.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['movie_no', 'movie_name', 'movie_year', 'movie_certificate',                      'movie_runtime', 'movie_genre', 'movie_score', 'movie_gross',                      'movie_director', 'movie_star', 'movie_writer', 'tomatoter', 'audience'])
        
    for idx in range(60):
        page_no = idx + 1
        movie_no_initial = 50*idx - 1
        debug_en = 0
        spider(page_no, movie_no_initial, debug_en)

    writer.writerows(movie_table)

