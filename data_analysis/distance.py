from urllib import parse, request

from geopy.distance import geodesic

# geodesic((Latitude, Longitude), (Latitude, Longitude)).m

print(geodesic((39.97, 116.33), (40.02, 116.29)).m)

print(geodesic((39.97, 116.29), (40.02, 116.29)).m)

print(geodesic((39.97, 116.33), (39.97, 116.29)).m)

print(geodesic((40.00152, 116.311859), (40.001437, 116.31225)).m)

exit(1)
url_address = "https://restapi.amap.com/v3/staticmap?"
values = {
    "location": "116.481485,39.990464",
    "zoom": "10",
    "key": "db33417f15d122a108d36ae2db1b5076"
}

data = parse.urlencode(values)
print(data)

req = url_address + '?' + data
response = request.urlopen("https://restapi.amap.com/v3/staticmap?markers=mid,0xFF0000,A:116.37359,39.92437;116.47359,39.92437&key=db33417f15d122a108d36ae2db1b5076")
print(response.status)
print(response.read())
