import pandas as pd
import os
import py_entitymatching as em
import numpy as np

datasets_dir = os.getcwd() + os.sep

pathA = datasets_dir + "/data/imdb_clean.csv"
pathB = datasets_dir + "/data/tomato_clean.csv"
pathC = datasets_dir + "/data/block.csv"

A = pd.read_csv(pathA)
B = pd.read_csv(pathB)
# Rename first empty attr 
# df.rename(columns={"Unnamed: 0": "id"},  inplace=True)

p_A = A[['movie_no', 'movie_name', 'movie_year', 'movie_director', 'movie_star']]
p_B = B[['movie_no', 'movie_name', 'movie_year', 'movie_director', 'movie_star']]

em.set_key(p_A, 'movie_no')
em.set_key(p_B, 'movie_no')

pathS = datasets_dir + "/data/labeled_data.csv"

S = em.read_csv_metadata(pathS, 
                         key='_id',
                         ltable=p_A, rtable=p_B, 
                         fk_ltable='ltable_movie_no', fk_rtable='rtable_movie_no')

IJ = em.split_train_test(S, train_proportion=0.7, random_state=0)
I = IJ['train']
J = IJ['test']

# Classifier
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NB')

# Feature generation
F = em.get_features_for_matching(p_A, p_B, validate_inferred_attr_types=False)

H = em.extract_feature_vecs(I, 
                            feature_table=F, 
                            attrs_after='label',
                            show_progress=False)

# Missing value
H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_movie_no', 'rtable_movie_no', 'label'],
                strategy='mean')

# Corss Validation 
result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_movie_no', 'rtable_movie_no', 'label'],
        k=5, # Num of fold
        target_attr='label', metric_to_select_matcher='f1', random_state=0)


# C is the blokced data 
C = em.read_csv_metadata(pathC,
                        key='_id',
                        ltable=p_A, rtable=p_B,
                        fk_ltable='ltable_movie_no', fk_rtable='rtable_movie_no')

cl = result['selected_matcher']

L = em.extract_feature_vecs(C, feature_table=F,
                            show_progress=False)


predictions = cl.predict(table=L, exclude_attrs=['_id', 'ltable_movie_no', 'rtable_movie_no'], 
              append=True, target_attr='predicted', probs_attr='score', return_probs = True, inplace=False)

# Tuple predicted as match
tn = predictions[(predictions['predicted'] == 1)]
C[C['_id'].isin(tn['_id'])]

# Duplicate detect
dup_A = tn[tn["ltable_movie_no"].duplicated(keep=False)]
dup_B = tn[tn["rtable_movie_no"].duplicated(keep=False)]
dup_T = pd.merge(dup_A, dup_B, how='outer', on=['_id','ltable_movie_no', 'rtable_movie_no'])

# Remove duplicate
clean_dup_A = tn[~(tn["ltable_movie_no"].isin(dup_T['ltable_movie_no']))]
clean_dup_B = tn[~(tn["rtable_movie_no"].isin(dup_T['rtable_movie_no']))]

# Remove all matched from A and B (A' and B')
new_A = A[(~A['movie_no'].isin(clean_dup_A['ltable_movie_no']))]
new_B = B[(~B['movie_no'].isin(clean_dup_B['rtable_movie_no']))]

# Select one pair of duplicate pairs
dict_A = {}
dict_B = {}

res = []
s_A = []
s_B = []
for index, row in dup_T.iterrows():
    if (row['ltable_movie_no'] not in dict_A) and (row['rtable_movie_no'] not in dict_B):
        dict_A[row['ltable_movie_no']] = 1
        dict_B[row['rtable_movie_no']] = 1
        s_A.append(row['ltable_movie_no'])
        s_B.append(row['rtable_movie_no'])
        res.append(row['_id'])

dict_RA = {}    
dict_RB = {}
for index, row in dup_T.iterrows():
    if (row['ltable_movie_no'] not in dict_A):
        dict_RA[row['ltable_movie_no']] = 1;
    if (row['rtable_movie_no'] not in dict_B):
        dict_RB[row['rtable_movie_no']] = 1;

rem_B = B[B['movie_no'].isin(dict_RB)]
rem_A = A[A['movie_no'].isin(dict_RA)]

# Merge Matching Set T
m_A = A[(A['movie_no'].isin(clean_dup_A['ltable_movie_no']))]
m_B = B[(B['movie_no'].isin(clean_dup_B['rtable_movie_no']))]

clean_dup_A.rename(columns={"ltable_movie_no": "movie_no"}, inplace = True)
clean_dup_B.rename(columns={"rtable_movie_no": "movie_no"}, inplace = True)

m_B = pd.merge(m_B, clean_dup_B[['_id', 'movie_no']], how = 'left', on = 'movie_no')
m_A = pd.merge(m_A, clean_dup_A[['_id', 'movie_no']], how = 'left', on = 'movie_no')
m_F = pd.merge(m_A[['_id','movie_no', 'movie_name', 'movie_year', 'movie_certificate', 'movie_runtime', 
                   'movie_genre', 'movie_score', 'movie_gross', 'movie_director', 'movie_star']],
               m_B[['_id','movie_writer', 'tomatoter', 'audience']], how = 'left', on = '_id')

# Merge Duplicative set D
m_Dl = tn[tn["_id"].isin(res)]
m_Dr = m_Dl.copy()
m_Dl.rename(columns={"ltable_movie_no": "movie_no"}, inplace = True)
m_Dr.rename(columns={"rtable_movie_no": "movie_no"}, inplace = True)

m_DA = A[(A['movie_no'].isin(s_A))]
m_DB = B[(B['movie_no'].isin(s_B))]

m_DB = pd.merge(m_DB, m_Dr[['_id', 'movie_no']], how = 'left', on = 'movie_no')
m_DA = pd.merge(m_DA, m_Dl[['_id', 'movie_no']], how = 'left', on = 'movie_no')
m_DF = pd.merge(m_DA[['_id','movie_no', 'movie_name', 'movie_year', 'movie_certificate', 'movie_runtime', 
                   'movie_genre', 'movie_score', 'movie_gross', 'movie_director', 'movie_star']],
               m_DB[['_id','movie_writer', 'tomatoter', 'audience']], how = 'left', on = '_id')

# Clean schema
new_A = new_A.drop(['Unnamed: 0', 'movie_no'], axis = 1)
new_B = new_B.drop(['Unnamed: 0', 'movie_no'], axis = 1)
rem_A = rem_A.drop(['Unnamed: 0', 'movie_no'], axis = 1)
rem_B = rem_B.drop(['Unnamed: 0', 'movie_no'], axis = 1)
m_F = m_F.drop(['_id', 'movie_no'], axis=1)
m_DF = m_DF.drop(['_id', 'movie_no'], axis=1)

# Combine data
frames = [new_A, rem_A, new_B, rem_B, m_F, m_DF]
result = pd.concat(frames, ignore_index=True)
# result.to_csv("merge_table.csv", encoding='utf-8')