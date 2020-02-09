import pandas as pd
import folium
import geopandas
import geopy

locator = geopy.Nominatim(user_agent = "myGeocoder")
location = locator.geocode("Champ de-Mars, Paris, France")

print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

df = pd.read_csv('addresses.csv')
#df = pd.DataFrame(df)
print(df.head(5))
print(len(df.loc[0]))
#df.insert(10, "ADDRESS", [], True)

#df['ADDRESS'] = df.Address1 + ' ' + df.Address3 + ' ' + df.Address4 + ' ' + df.Address5
#print(df['ADDRESS'])

df['ADDRESS'] = df.apply(lambda row: row.Address1 + ' ' + row.Address3 + ' ' + row.Address4 + ' ' + row.Address5, axis = 1)

print(df.head(5))

#df.insert(11, "Latitude", [], True)
#df.insert(12, "Longitude", [], True)
a = []
b = []
locator = ""
for i in range(len(df)):
    #location = u' '.join((locator.geocode(df.loc[i, "ADDRESS"]))).encode('utf-8').strip()
    try:
        locator = geopy.Nominatim(user_agent = "myGeocoder")
        x = df.loc[i, "ADDRESS"]
        #print(x)
        location = locator.geocode(x)
        a.append(format(location.latitude))
        #print(a)
        b.append(format(location.longitude))
    except AttributeError:
        #print("lol")
        continue



df2 = pd.DataFrame(list(zip(a, b)),
               columns =['Latitude', 'Longitude'])

print(df2.head(5))

from geopy.extra.rate_limiter import RateLimiter

# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
df['location'] = df['ADDRESS'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

#df = df.drop(['Address1', 'Address3', 'Address4', 'Address5'. 'Telefon'])
