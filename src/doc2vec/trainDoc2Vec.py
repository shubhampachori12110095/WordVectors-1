'''
Created on Sep 22, 2015

@author: atomar
'''
from gensim.models import doc2vec
import pickle
import logging
from random import shuffle
import time

#Set up logging configurations  
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#Load tagged cleaned up reviews
bagTaggedDocs = pickle.load(open("../../classifier/taggedDocs.pickle","rb"))

# parameter values
num_features = 300 #number of features/columns for the term-document matrix.
'''
minimum word count: any word that does not occur at least this many times
across all documents is ignored
'''
min_word_count = 40 

context = 10 # Context window size. The paper (http://arxiv.org/pdf/1405.4053v2.pdf) suggests 10 is the optimal
'''
threshold for configuring which higher-frequency words are randomly downsampled;
default is 0 (off), useful value is 1e-5
set the same as word2vec
'''
downsampling = 1e-3 

num_workers = 4  # Number of threads to run in parallel

# if sentence is not supplied, the model is left uninitialized
# otherwise the model is trained automatically
# https://www.codatlas.com/github.com/piskvorky/gensim/develop/gensim/models/doc2vec.py?line=192

'''
Needed for python 3.x, before gensim 0.13.1

def myhash(obj):
    return hash(obj) % (2 ** 32)    
    
prior to gensim 0.13, the model declaration would be

model = word2vec.Word2Vec(bagOfsentences, workers=num_workers,
                          size=num_features, min_count=min_word_count,
                          window=context, sample=downsampling,hashfxn=myhash)

python 2.x declaration would be 

python 2.x declaration would be 
model = doc2vec.Doc2Vec(size=num_features,
                        window=context, min_count=min_word_count,
                        sample=downsampling, workers=num_workers)
'''
model = doc2vec.Doc2Vec(size=num_features,
                        window=context, min_count=min_word_count,
                        sample=downsampling, workers=4)

#Build the model vocabulary (term document matrix)
model.build_vocab(bagTaggedDocs)

# If you don't plan to train the model any further, calling
# init_sims will make the model much more memory-efficient
model.init_sims(replace=False)

#Train the model for 10 epochs
for epoch in range(1,10):
    
    print("Starting Epoch ",epoch)
    
    start_time = time.time()
    
    #Shuffle the tagged cleaned up reviews in each epoch
    shuffle(bagTaggedDocs)
    
    model.train(bagTaggedDocs)
    
    print("Epoch ",epoch," took %s minutes " % ((time.time() - start_time)/60))

#Save the trained model	
model.save("../../classifier/Doc2VecTaggedDocs")
