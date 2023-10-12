import pandas as pd
import numpy as np
import geopy.distance

# Cleaning functions
def bath_bed_ratio_outlier(df):
    df = df.copy()
    df["bath_bed_ratio"] = df["bathrooms"] / df["bedrooms"]
    df[~((df.bath_bed_ratio <= 0.1) | (df.bath_bed_ratio >=2))]
    return df


def sqft_basement(df):
    df = df.copy()
    df['sqft_basement'] = pd.to_numeric(df['sqft_basement'], errors="coerce")
    df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]
    return df

def calculate_last_change(df):
    df = df.copy()
    df['yr_renovated'] = df['yr_renovated'].fillna(0)
    df['yr_renovated'] = df['yr_renovated'].where(df['yr_renovated']!=0, df['yr_built']).astype(int)
    df = df.rename(columns={'yr_renovated':  'last_known_change'})
    return df

def fill_missing_view_wf(df):
    df.copy()
    df["view"] = df["view"].fillna(0)
    df["waterfront"] = df["waterfront"].fillna(0)
    return df


# Feature engineering functions
# Distance between center and property
def center_distance(df):
    df = df.copy()
    center_location = (47.62774, -122.24194)
    df['center_distance'] = pd.Series(zip(df.lat, df.long))
    df['center_distance'] = df.center_distance.apply(lambda x: round(geopy.distance.geodesic(center_location, x).km, 2))
    return df


# Distance between water and property
def waterfront_distance(df):
    df = df.copy()

    def dist(long, lat, ref_long, ref_lat):
        '''dist computes the distance in km to a reference location. Input: long and lat of 
        the location of interest and ref_long and ref_lat as the long and lat of the reference location'''
        delta_long = long - ref_long
        delta_lat = lat - ref_lat
        delta_long_corr = delta_long * np.cos(np.radians(ref_lat))
        return ((delta_long_corr)**2 +(delta_lat)**2)**(1/2)*2*np.pi*6378/360

    water_houses = df.query('waterfront == 1')
    water_distance = []
    # For each row in our data frame we now calculate the distance to the seafront
    for idx, lat in df.lat.items():
        ref_list = []
        for x,y in zip(list(water_houses.long), list(water_houses.lat)):
            ref_list.append(dist(df.long[idx], df.lat[idx], x, y).min())
        water_distance.append(min(ref_list))

    df['water_distance'] = water_distance
    return df