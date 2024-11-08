"""
Module to predict when busts will occur and adjust IMPROVER data 
accordingly.

Functions:
    adjust_site_df: Adjusts site model data based on predicted busts.
    adjust_vis_cld: Changes vis or cloud data based on bust labels.
    dt_calc: For creating column with datetimes.
    get_labels: Converts predicted integer classes to string labels.
    get_ml_df: Organises data into dataframe for use with machine learning
        algorithms.
    pred_adjust: Predict busts and adjust model data based on these predictions.
"""
from datetime import datetime
import os
import numpy as np
import pandas as pd
import pickle
import warnings

import common.calculations as ca
import common.configs as co
import data_extraction.extract_sort_data as ex

# Define environment constants
ML_DIR = os.environ['ML_DIR']

# Silence warnings
warnings.filterwarnings("ignore")


def adjust_site_df(site_df):
    """
    Adjusts site model data based on predicted busts.

    Args:
        site_df (pandas.DataFrame): Site model data
    Returns:
        site_df (pandas.DataFrame): Adjusted site model data
    """
    # Get bust-predicting classifiers from pickle file (if available)
    icao = site_df.attrs['icao']
    clf_pickle = f'{ML_DIR}/clfs_data_{icao}'
    if not os.path.exists(clf_pickle):
        return site_df
    with open(clf_pickle, 'rb') as file_object:
        unpickler = pickle.Unpickler(file_object)
        _, clf_models = unpickler.load()

    # Convert data to required format for machine learning
    tdf = get_ml_df(site_df)

    # Adjust data 5 times to allow for up to 5 TAF group adjustments
    for ind in range(5):

        # Adjust model data based on predicted bust labels
        site_df = pred_adjust(site_df, tdf, clf_models, icao, 'xgboost')

        # Update ml dataframe
        tdf = get_ml_df(site_df)

    # Ensure sig wx still sensible with new visibilities - adjust if not
    site_df['sig_wx'] = site_df.apply(ex.update_sig_wx_for_new_vis, axis=1)

    return site_df


def adjust_vis_cld(site_df, row, param):
    """
    Changes vis or cloud data based on bust labels.

    Args:
        site_df (pandas.DataFrame): Site model data
        row (pandas.Series): Row of dataframe
        param (str): Weather parameter
        perc (int): Percentile
    Returns:
        site_df (pandas.DataFrame): Adjusted site model data
    """
    # Get TAF rules for airport
    rules = site_df.attrs['rules']

    # Get bust label column name from parameter
    pred_col = f'{param}_pred_labels'

    # For no bust predicted, do not adjust anything
    if row[pred_col] == 'no_bust':
        return site_df

    # Get old TAF categories for each percentile
    old_cats = []
    for perc in [30, 40, 50, 60, 70]:

        # Get df at valid time and percentile
        perc_time_df = site_df.loc[(site_df['percentile'] == perc)
                                    & (site_df['time'] == row['vdt'])]

        # Get old TAF category
        old_cat = perc_time_df[f'{param}_cat'].values[0]

        # Do not adjust any data if any of the old categories are low 
        # (i.e. low cloud/fog)
        if old_cat < 3:
            return site_df

        # Append old category to list
        old_cats.append(old_cat)

    # If not already returned, loop through percentiles again and adjust
    # data based on bust label
    for perc, old_cat in zip([30, 40, 50, 60, 70], old_cats):

        # If increased bust, increase to next category up
        if row[pred_col] == f'{param}_increase':
            new_cat = float(int(old_cat + 1))

        # If decreased bust, decrease to next category down
        elif row[pred_col] == f'{param}_decrease':
            new_cat = float(int(old_cat - 1))

        # Get new value(s) and update det_df
        if param == 'vis':
            new_vis = ca.get_vis(new_cat, rules)
            for col, val in zip(['vis', 'vis_cat'], [new_vis, new_cat]):
                site_df.loc[(site_df['percentile'] == perc)
                            & (site_df['time'] == row['vdt']), col] = val
        elif param == 'cld':
            new_cld_3, new_cld_5 = ca.get_cld(new_cat, rules)
            for col, val in zip(['cld_3', 'cld_5', 'cld_cat'],
                                [new_cld_3, new_cld_5, new_cat]):
                site_df.loc[(site_df['percentile'] == perc)
                            & (site_df['time'] == row['vdt']), col] = val

    return site_df


def dt_calc(row):
    """
    For creating column with datetimes.

    Args:
        row (pandas.Series): Row of dataframe
    Returns:
        (datetime.datetime): Date and time
    """
    return datetime(row['year'], row['month'], row['day'], row['hour'])


def get_labels(X, clf_models, wx_type, c_name):
    """
    Converts predicted integer classes to string labels.

    Args:
        X (pandas.DataFrame): Input data
        clf_models (dict): Dictionary of classifier models
        wx_type (str): Weather parameter
        clf_type (str): Classifier type
    Returns:
        pred_labels (np.ndarray): Array of predicted labels
    """
    # If no classifier available, return all no busts
    if clf_models[f'{wx_type}_{c_name}'] is None:
        pred_labels = np.array(['no_bust'] * len(X))
        return pred_labels

    # Predict label classes (0, 1, etc)
    y_pred = clf_models[f'{wx_type}_{c_name}'].predict(X)

    # Convert class integers to labels using label dictionary
    label_dict = clf_models[f'{wx_type}_{c_name}_label_dict']
    lab_dict_inv = {val: key for key, val in label_dict.items()}
    pred_labels = np.vectorize(lab_dict_inv.get)(y_pred)

    return pred_labels


def get_ml_df(site_df, bust_labels=None):
    """
    Organises data into dataframe for use with machine learning
    algorithms.

    :param det: Deterministic BestData dataframe
    :type det: pandas.DataFrame
    :param perc: Percentiles BestData dataframe
    :type perc: pandas.DataFrame
    :param bust_labels: List of bust label dictionaries
    :type bust_labels: list

    :return: Dataframe with required data
    :rtype: pandas.DataFrame
    """
    # Rearrange site_df
    ml_df = site_df.pivot(index='time', columns='percentile')

    # Relabel columns using percentile value
    ml_df.columns = [f'{col}_{percentile}' for col, percentile in ml_df.columns]

    # Convert 'time' from index to column
    ml_df = ml_df.reset_index()

    # Add bust labels if required
    if bust_labels:
        wind_labels, dir_labels, vis_labels, cld_labels = bust_labels
        ml_df['wind_bust_label'] = ml_df['time'].map(wind_labels)
        ml_df['dir_bust_label'] = ml_df['time'].map(dir_labels)
        ml_df['vis_bust_label'] = ml_df['time'].map(vis_labels)
        ml_df['cld_bust_label'] = ml_df['time'].map(cld_labels)

    # Add columns based on date/time
    ml_df['year'] = ml_df.apply(lambda x: x['time'].year, axis=1)
    ml_df['month'] = ml_df.apply(lambda x: x['time'].month, axis=1)
    ml_df['day'] = ml_df.apply(lambda x: x['time'].day, axis=1)
    ml_df['hour'] = ml_df.apply(lambda x: x['time'].hour, axis=1)

    # Create lead time column
    t_0 = ml_df['time'].values[0]
    ml_df['lead'] = ml_df.apply(lambda x: (x['time'] 
                                - t_0).total_seconds() / 3600, axis=1)

    # Drop time column
    ml_df.drop('time', axis=1, inplace=True)

    # Make bust_labels the last columns if required
    if bust_labels:
        cols = ml_df.columns.tolist()
        for bust_label in co.BUST_COLS:
            cols.append(cols.pop(cols.index(bust_label)))
        ml_df = ml_df[cols]

    # Change NaNs to no_bust (occurs when airport opens late or similar)
    for col in ml_df.columns:
        if 'bust' in col:
            ml_df[col] = ml_df[col].fillna('no_bust')

    # Add a column to incorporate all busts if required
    if bust_labels:
        ml_df['any_bust'] = ml_df.apply(calc_bust, axis=1)

    return ml_df


def pred_adjust(site_df, tdf, clf_models, icao, c_name):
    """
    Predict busts and adjustmodel data based on these predictions

    Args:
        site_df (pandas.DataFrame): Site model data
        tdf (pandas.DataFrame): Model data
        clf_models (dict): Classifier models
        icao (str): ICAO airport identifier
        c_name (str): Classifier type
    Returns:
        site_df (pandas.DataFrame): Adjusted site model data
    """
    # Get X columns from dataframe
    X = tdf[co.PARAM_COLS]
    X = X.apply(pd.to_numeric)

    # Create bust predicts dataframe, starting with valid times
    bust_preds = pd.DataFrame({'vdt': tdf.apply(dt_calc, axis=1)})

    # Predict bust types for each weather type
    for wx_type in ['vis', 'cld']:

        # Just use best features
        X_best = X[clf_models[f'{wx_type}_{c_name}_features']]

        # Predict wx type bust labels
        pred_labels = get_labels(X_best, clf_models, wx_type, c_name)

        # Add labels to bust preds dataframe
        bust_preds[f'{wx_type}_pred_labels'] = pred_labels

    # Loop through each row of bust labels dataframe
    for _, row in bust_preds.iterrows():

        # Change data for each percentile and each parameter
        for param in ['vis', 'cld']:
            site_df = adjust_vis_cld(site_df, row, param)

    return site_df


