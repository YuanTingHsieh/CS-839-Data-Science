import py_entitymatching as em
import numpy as np
import pandas as pd

import os

DATA_DIR = '../data'

imdb = em.read_csv_metadata(os.path.join(DATA_DIR, 'imdb_clean.csv'), key = 'movie_no')
tomato = em.read_csv_metadata(os.path.join(DATA_DIR, 'tomato_clean.csv'), key = 'movie_no')

# blocking phase
output_attrs = ['movie_no', 'movie_name', 'movie_year', 'movie_director', 'movie_star']

'''
  This is way too good
C = ab.block_tables(imdb, tomato, l_block_attr = 'movie_name', 
     r_block_attr = 'movie_name', l_output_attrs=output_attrs,
     r_output_attrs = output_attrs) 
'''
print "Overlap Blocking with movie name"
ob = em.OverlapBlocker()
C1 = ob.block_tables(imdb, tomato, l_overlap_attr= 'movie_name', 
     r_overlap_attr= 'movie_name', l_output_attrs=output_attrs,
     r_output_attrs = output_attrs)

bb = em.BlackBoxBlocker()
overlap_star_thres = 2
def f_star_block(ltuple, rtuple):
    if ltuple['movie_star'] == 'NoStar':
        return True
    if rtuple['movie_star'] == 'NoStar':
        return True
    l_star = ltuple['movie_star'].replace(',', '').split()
    r_star = rtuple['movie_star'].replace(',', '').split()
    overlap_star = len(set(l_star).intersection(r_star))
    if overlap_star < overlap_star_thres:
        return True
    return False
print "Blocking with movie director"
bb.set_black_box_function(f_star_block)
C2 = bb.block_candset(C1)

# block by offset of movie year
# if l.year = r.year +- offset
# then it is valid
year_offset = 2
def f_year_block(ltuple, rtuple):
    if (ltuple['movie_year'] <= rtuple['movie_year'] + year_offset) \
       and (ltuple['movie_year'] >= rtuple['movie_year'] - year_offset):
        return False
    return True

print "Blocking with year offset +- ", year_offset
bb.set_black_box_function(f_year_block)
C3 = bb.block_candset(C2)

# block by cos sim of movie name
# cos sim lower than thershold would be blocked
cos_thres = 0.4
def f_threshold_cos(ltuple, rtuple):
    l_movie_name = ltuple['movie_name'].split()
    r_movie_name = rtuple['movie_name'].split()
    cos_sim = em.cosine(l_movie_name, r_movie_name)
    if cos_sim < cos_thres:
        return True
    return False

print "Blocking with cos sim threshold ", cos_thres
bb.set_black_box_function(f_threshold_cos)
C4 = bb.block_candset(C3)

print "Saving blocking result"
C4.to_csv(os.path.join(DATA_DIR, 'block.csv'))

#print "Debugging blockers..."
#D = em.debug_blocker(C4, imdb, tomato, output_size=200)

