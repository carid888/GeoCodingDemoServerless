import json
# Importing Libraries
from glob import glob
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
import time
import boto3


s3 = boto3.client('s3')
  
def longlatstate(event, context):
    # loading states and counties geodataframes
    lon = float(event['pathParameters']['lon']) #-098.371784
    lat = float(event['pathParameters']['lat'])#38.595944
    display = True
    point_index = 0

    obj = s3.get_object(Bucket='augurisk-geocoding-search',Key='cb_2018_us_state_20m.zip')
    #put  to 'temp.bin'
    print('=================')
    print(obj.keys())

    print(obj['ContentLength'])
    f=open('temp.shp','w+b')
    f.write(obj['Body'].read())
    f.close()

  
    gdp_states = gpd.read_file('temp.shp')
    point=Point(lon,lat)
    for i in range(len(gdp_states)):
        if point.within(gdp_states['geometry'].iloc[i]):
            if display==True:
                # print(gdp_states['NAME'].iloc[i])
                b=gdp_states.iloc[i:i+1].plot(figsize=(2**3,2**3))
                point_index = i

    body = {
        "message": "Index found " + str(point_index)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response