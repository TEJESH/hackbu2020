""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""


from flask import Flask, request, render_template, jsonify


import pandas as pd
import folium
import geopandas
import geopy
import sys
from importlib import reload
#from ipywidgets.embed import embed_minimal_html

#import statistics
#from sklearn import preprocessing
#from sklearn.model_selection import train_test_split
#from keras.layers import Input, Dense
#from keras.models import Model
import random as rd
from folium.plugins import MarkerCluster

reload(sys)
sys.setdefaultencoding('utf8')

import gmaps
import gmaps.datasets
gmaps.configure(api_key='AIzaSyCJKhTd9xAGWd3sS_kYDJrDjaeh_ycBzaE')

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app, resources={r"/api/*": {"origins": "*"}})


df = pd.read_csv('Book2.csv')

dfEmpty = df.isnull().sum()

def percentEmpty(df):
    dfEmpty=df.isnull().sum()
    totalRows=len(df)
    print("totalRows",totalRows)
    peDf = pd.DataFrame((dfEmpty/totalRows)*100, columns=['percent'])
    peDf['colName'] = peDf.index
    return peDf

percentEmpty(df)

df.dropna(subset=['CMPLNT_NUM', 'Latitude', 'Longitude'], how='any', inplace=True)

percentEmpty(df)

df.to_csv('CleanedCrimeData')

cleanData = pd.read_csv('CleanedCrimeData')
copy_cleanData = cleanData

#normalized = preprocessing.normalize(copy_cleanData, axis = 1)

df = pd.DataFrame(copy_cleanData)
'''
columns = ['LAW_CAT_CD', 'BORO_NM']

def category_onehot_multcols(multcolumns):
    df_final = df
    i=0
    for fields in multcolumns:

        df1=pd.get_dummies(df[fields],drop_first=True)

        df.drop([fields],axis=1,inplace=True)
        if i==0:
            df_final=df1.copy()
        else:

            df_final=pd.concat([df_final,df1],axis=1)
        i=i+1


    df_final=pd.concat([df,df_final],axis=1)

    return df_final

#create a copy of train data
#main_df=df.copy()
df.dropna(inplace=True)
df = category_onehot_multcols(columns)
print(df)
#feat_columns = [c for c in df.columns]
feat_columns = [df.BROOKLYN, df.MANHATTAN, df.QUEENS]
#target_column = [c for c in df.columns]
target_column = [df.MISDEMEANOR, df.VIOLATION, df.VIOLATION]

X_df, X_val, y_df, y_val = train_test_split(df[feat_columns], df[target_column], test_size=0.95)


print(X_df.shape)

#print(X_df.head())



# reduce to 10 features
encoding_dim = 10

input_df = Input(shape=(25,))
encoded = Dense(encoding_dim, activation='relu')(input_df)
decoded = Dense(25, activation='sigmoid')(encoded)

# encoder
autoencoder = Model(input_df, decoded)

# intermediate result
encoder = Model(input_df, encoded)

autoencoder.compile(optimizer='adadelta', loss='mean_squared_error')


autoencoder.fit(X_df, X_df,
                epochs=150,
                  batch_size=256,
                shuffle=True,
                validation_data=(X_val, X_val))
print(X_df)

copy_cleanData1 = X_df
'''
copy_cleanData = copy_cleanData[0:499]
#df = pd.DataFrame(df)
#print(df.head(5))
#print(len(df.loc[0]))
#df.insert(10, "ADDRESS", [], True)

#df['ADDRESS'] = df.Address1 + ' ' + df.Address3 + ' ' + df.Address4 + ' ' + df.Address5
#print(df['ADDRESS'])

#df['ADDRESS'] = df.apply(lambda row: row.Address1 + ' ' + row.Address3 + ' ' + row.Address4 + ' ' + row.Address5, axis = 1)
#df['ADDRESS'] =
#print(df.head(5))

#df.insert(11, "Latitude", [], True)
#df.insert(12, "Longitude", [], True)
'''a = []
b = []
locator = ""
for i in range(0, len(df)):
    #location = u' '.join((locator.geocode(df.loc[i, "ADDRESS"]))).encode('utf-8').strip()
    try:
        locator = geopy.Nominatim(user_agent = "myGeocoder")
        x = df.loc[i, "ADDRESS"]
        #print(x)
        location = locator.geocode(x)
        a.append(format(location.latitude).encode('utf-8'))
        #print(a)
        b.append(format(location.longitude).encode('utf-8'))
    except AttributeError:
        #print("lol")
        continue

'''

#df2 = pd.DataFrame(list(zip(a, b)),
#               columns =['Latitude', 'Longitude'])
#df2 = df2.astype(float)
locations1 = copy_cleanData[['Latitude', 'Longitude']]
locationlist = locations1.values.tolist()
print(locationlist)

#dataToShow = df[['ADDRESS']].to_dict(orient='records')

@app.route('/')
def my_form():
    return render_template('homes.html')


@app.route('/', methods=['POST'])
def my_form_post():

    #print(dataToShow)
    text = request.form['address']
    processed_text = text.upper()
    str1= processed_text
    a = []
    locator = geopy.Nominatim(user_agent = "myGeocoder")
    location = locator.geocode(str1)
    a = [format(location.latitude), format(location.longitude)]
    #print(a)

    print(a)


    map = folium.Map(location=locationlist[0], zoom_start=7)

    for each in copy_cleanData.iterrows():
        folium.Marker((each[1]['Latitude'],each[1]['Longitude'])).add_to(map)

    map_2 = folium.Map(location=[copy_cleanData['Latitude'].mean(),
                            copy_cleanData['Longitude'].mean()],
                  zoom_start=10)
    mc = MarkerCluster()

    for row in copy_cleanData.itertuples():
        offensecolor = 'blue'
        if(str(row.OFNS_DESC) == "ROBBERY" or str(row.OFNS_DESC) == "RAPE" or str(row.OFNS_DESC) == "DANGEROUS WEAPONS" or str(row.OFNS_DESC) == "BURGLARY" or str(row.OFNS_DESC) == "HARRASSMENT 2" or str(row.OFNS_DESC) == "CRIMINAL MISCHIEF & RELATED OF" or str(row.OFNS_DESC) == "SEX CRIMES"):
            offensecolor = 'red'

        mc.add_child(folium.Marker(location=[row.Latitude,row.Longitude], popup="Type of Crime: "+ str(row.OFNS_DESC)+"\n Area: "+str(row.BORO_NM),icon=folium.Icon(color= offensecolor ,icon='info-sign')))
    map_2.add_child(mc)


    return map_2._repr_html_()




if __name__ == '__main__':
    app.run(debug=True)
