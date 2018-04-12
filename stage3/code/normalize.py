import pandas as pd
import os

DATA_DIR = '../data'

imdb = pd.read_csv(os.path.join(DATA_DIR, 'imdb.csv'))
tomato = pd.read_csv(os.path.join(DATA_DIR ,'tomato.csv'))

print "Normalizing dataframes"
# normalizing phase
print "Normalizing dataframes"
imdb['movie_year'] = imdb['movie_year'].str.extract('(\d+)', expand=False)
imdb.dropna(subset=['movie_year', 'movie_director'], inplace=True)
#imdb['movie_year'] = imdb['movie_year'].fillna(value=0)
imdb['movie_year'] = imdb['movie_year'].astype(int)
imdb['movie_star'].fillna(value = 'NoStar', inplace=True)
imdb['movie_name'] = imdb['movie_name'].str.lower()

tomato.dropna(subset=['movie_year', 'movie_director'], inplace=True)
tomato['movie_star'].fillna(value = 'NoStar', inplace=True)
tomato['movie_name'] = tomato['movie_name'].str.lower()

imdb.to_csv(os.path.join(DATA_DIR, 'imdb_clean.csv'))
tomato.to_csv(os.path.join(DATA_DIR, './tomato_clean.csv'))
