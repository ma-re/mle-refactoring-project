import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from preprocessing import SqftBasement, BathBedOutlierRemoval, CalculateLastChange, CenterDistance


# Data import
housing_data = pd.read_csv("../data/King_County_House_prices_dataset.csv")
print("Data import successful")

# Columns with missing values that should be imputed with mode
column_zeros = ['view', 'waterfront']

# Pipeline with custom transformer for cleaning and engineering
cleaning_pipeline = Pipeline([
    ('center_distance', CenterDistance()),
    ('bath_bed', BathBedOutlierRemoval()),
    ('sq_basement', SqftBasement()),
    ('last_change', CalculateLastChange())
])

# Sklearn pipeline for imputing missing values with mode
missing_zero_imputation = Pipeline([
    ('missings_zero', SimpleImputer(strategy='most_frequent'))
])

column_preprocessor = ColumnTransformer([
    ('zeros', missing_zero_imputation, column_zeros), 
], remainder= 'passthrough')

# Combining preprocessing and imputing
preprocessor = Pipeline([
    ('cleaning', cleaning_pipeline),
    ('imputation', column_preprocessor)
])

# Fit and transform data
housing_data_cleaned = preprocessor.fit_transform(housing_data)

# Get feature names from preprocessor and save transformed array in data frame
feature_names = preprocessor[-1].get_feature_names_out().tolist()
feature_names_clean = [x.replace('zeros__', '').replace('remainder__', '') for x in feature_names]
housing_data_cleaned_df = pd.DataFrame(housing_data_cleaned, columns=feature_names_clean)
print("Data transformation successful")
print("Number of columns: ", housing_data_cleaned_df.shape[1])
print("Number of row: ", housing_data_cleaned_df.shape[0])

# Create small dataframe 
housing_data_small = housing_data_cleaned_df[['id', 'price', 'bedrooms', 'center_distance', 'last_known_change']]

# Save dataframe in data folder
housing_data_small.to_csv("../data/housing_data_cleaned.csv", index=False)
print("Saving data successful")