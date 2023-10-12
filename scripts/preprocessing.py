import pandas as pd
import numpy as np
import geopy.distance
from sklearn.base import BaseEstimator, TransformerMixin


class BathBedOutlierRemoval(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X["bath_bed_ratio"] = X["bathrooms"] / X["bedrooms"]
        X = X[~((X.bath_bed_ratio <= 0.1) | (X.bath_bed_ratio >=2))]
        return X.drop(['bath_bed_ratio'], axis=1)
    

class SqftBasement(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X.loc[:, 'sqft_basement'] = pd.to_numeric(X['sqft_basement'], errors="coerce")
        X.loc[:, "sqft_basement"] = X["sqft_living"] - X["sqft_above"]
        return X
    

class CalculateLastChange(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X['yr_renovated'] = X['yr_renovated'].fillna(0)
        X['last_known_change'] = X['yr_renovated'].where(X['yr_renovated']!=0, X['yr_built']).astype(int)
        return X.drop(['yr_renovated', 'yr_built'], axis=1)
    

class CenterDistance(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        center_location = (47.62774, -122.24194)
        X['center_distance'] = pd.Series(zip(X.lat, X.long))
        X['center_distance'] = X.center_distance.apply(lambda x: round(geopy.distance.geodesic(center_location, x).km, 2))
        return X
    
# To be done
class WaterfrontDistance(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        pass
