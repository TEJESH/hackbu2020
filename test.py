from gmaps import Geocoding
api = Geocoding(api_key="AIzaSyCJKhTd9xAGWd3sS_kYDJrDjaeh_ycBzaE")

#gmaps.configure(api_key="AIzaSyCJKhTd9xAGWd3sS_kYDJrDjaeh_ycBzaE")

api.geocode("somewhere")
api.reverse(51.123, 21.123)
