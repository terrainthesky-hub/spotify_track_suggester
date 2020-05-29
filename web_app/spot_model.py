# START RELATIONAL EMBEDDING MODEL
import pandas as pd
import numpy as np
from keras.layers import Input, Embedding, Dot, Reshape, Dense
from keras.models import Model
import random


spot = pd.read_csv('spotify_data3.csv')

#spot = spot[0:40000]       # uncomment if it cant run with the whole dataset
spot.head()

# indexing
name_index = {name: idx for idx, name in enumerate(spot.name)}
index_names = {idx: name for name, idx in name_index.items()}

energy_index = {energy: idx for idx, energy in enumerate(spot.energy)}
index_energy = {idx: energy for energy, idx in energy_index.items()}

# cleaning
spot['acoustic'] = spot.acousticness
spot['dance'] = spot.danceability
spot['instrumental'] = spot.instrumentalness
spot = spot.drop(columns=['acousticness','danceability','instrumentalness'])
spot['speech'] = spot.speechiness
spot = spot.drop(columns='speechiness')
spot['live'] = spot.liveness
spot = spot.drop(columns='liveness')

# set input
y = spot['energy'].values


def embedding_model(embedding_size = 20, classification = False):
    """Model to embed books and wikilinks using the functional API.
       Trained to discern if a link is present in a article"""
    
    # Both inputs are 1-dimensional
    name = Input(name = 'name', shape = [1])
    energy = Input(name = 'energy', shape = [1])
    
    # Embedding the book (shape will be (None, 1, 50))
    name_embed = Embedding(name = 'name_embed',
                input_dim = len(y),
                output_dim = embedding_size)(name)
    
    energy_embed = Embedding(name = 'energy_embed',
                input_dim = len(y),
                output_dim = embedding_size)(energy)


    # Merge the layers with a dot product along the second axis (shape will be (None, 1, 1))
    merged = Dot(name = 'dot_product', normalize = True, axes = 2)([name_embed,energy_embed
                                                                    ])
    
    # Reshape to be a single number (shape will be (None, 1))
    merged = Reshape(target_shape = [1])(merged)
    
    # If classifcation, add extra layer and loss function is binary cross entropy
    if classification:
        merged = Dense(1, activation = 'sigmoid')(merged)
        model = Model(inputs = [name, energy], outputs = merged)
        model.compile(optimizer = 'Adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    # Otherwise loss function is mean squared error
    else:
        model = Model(inputs = [name, energy], outputs = merged)
        model.compile(optimizer = 'Adam', loss = 'mse')
    
    return model

model = embedding_model()

target = np.array([1]*len(y))

#create incorrect targets
for x in range(len(target),len(target)+800,1):
  target = np.append(target,-1)

i = np.array(spot.index)

#create incorrect index
for x in range(len(i),len(i)+800,1):
  i = np.append(i,x)

# create incorrect energy 
random.seed(100)

for x in range(len(y),len(y)+800,1):
  y = np.append(y,random.uniform(np.max(y),np.min(y)))

results = model.fit([i,y],target, epochs=20)

name_layer = model.get_layer('name_embed')
name_weights = name_layer.get_weights()[0]

name_weights = name_weights / np.linalg.norm(name_weights, axis = 1).reshape((-1, 1))

# Visualization

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 15

def find_similar(name, weights, index_name = 'name', n = 10, least = False, return_dist = False, plot = False):
    """Find n most similar items (or least) to name based on embeddings. Option to also plot the results"""
    
    # Select index and reverse index
    if index_name == 'name':
        index = name_index
        rindex = index_names
    elif index_name == 'acoustic':
        index = energy_index
        rindex = index_energy
    
    # Check to make sure `name` is in index
    try:
        # Calculate dot product between book and all others     %%%%%%%%%
        dists = np.dot(weights, weights[index[name]])
    except KeyError:
        print(f'{name} Not Found.')
        return
    
    # Sort distance indexes from smallest to largest
    sorted_dists = np.argsort(dists)
    
    # Plot results if specified
    if plot:
        
        # Find furthest and closest items
        furthest = sorted_dists[:(n // 2)]
        closest = sorted_dists[-n-1: len(dists) - 1]
        items = [rindex[c] for c in furthest]
        items.extend(rindex[c] for c in closest)
        
        # Find furthest and closets distances
        distances = [dists[c] for c in furthest]
        distances.extend(dists[c] for c in closest)
        
        colors = ['r' for _ in range(n //2)]
        colors.extend('g' for _ in range(n))
        
        data = pd.DataFrame({'distance': distances}, index = items)
            
        # Horizontal bar chart
        data['distance'].plot.barh(color = colors, figsize = (10, 8),
                                   edgecolor = 'k', linewidth = 2)
        plt.xlabel('Cosine Similarity');
        plt.axvline(x = 0, color = 'k');
        
        # Formatting for italicized title
        name_str = f'{index_name.capitalize()}s Most and Least Similar to'
        for word in name.split():
            # Title uses latex for italize
            name_str += ' $\it{' + word + '}$'
        plt.title(name_str, x = 0.2, size = 28, y = 1.05)
        
        return None
    
    # If specified, find the least similar
    if least:
        # Take the first n from sorted distances
        closest = sorted_dists[:n]
         
        print(f'{index_name.capitalize()}s furthest from {name}.\n')
        
    # Otherwise find the most similar
    else:
        # Take the last n sorted distances
        closest = sorted_dists[-n:]
        
        # Need distances later on
        if return_dist:
            return dists, closest
        
        
        print(f'{index_name.capitalize()}s closest to {name}.\n')
        
    # Need distances later on
    if return_dist:
        return dists, closest

    
    
    # Print formatting
    max_width = max([len(rindex[c]) for c in closest])
    
    # Print the most similar and distances
    for c in reversed(closest):
        print(f'{index_name.capitalize()}: {rindex[c]:{12 + 2}} Similarity: {dists[c]:.{2}}')


# - - - THIS IS THE RECOMMENDATION FUNCTION - - -
find_similar('INSERT SONG HERE', name_weights)


# - - - VISUALIZATION - - -
from sklearn import preprocessing
import plotly.graph_objects as go

features = ['acoustic','dance','energy','instrumental','live','speech','tempo','valence']
x = spot[features].values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
x_scaled.shape

names = []
for name in features:
  names.append(name.upper())

categories = names

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=x_scaled[0],
      theta=categories,
      fill='toself',
      name='Song A'
))
# fig.add_trace(go.Scatterpolar(
#       r=x_scaled[1],
#       theta=categories,
#       fill='toself',
#       name='Product B'
# ))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=False,
      range=[0, 1]
    )),
  showlegend=False
)

fig.show()