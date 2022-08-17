# Generated by Django 4.1 on 2022-08-15 00:10
from django.db import migrations

import os
import pandas as pd

from ..models import Stock
from ..models import Participant
from ..models import ShareholdingInfo

def populate(*ags, **kwargs):

    base_dir = os.path.join('media')

    direc = os.path.join(base_dir, 'ListofStocks.csv')
    stock_df = pd.read_csv(direc, index_col = 0, dtype = str)
    for id, name in zip(stock_df['stock_id'], stock_df['stock_name']):
        Stock.objects.get_or_create(id = id, name = name)

    direc = os.path.join(base_dir,'ListofParticipants.csv')
    participant_df = pd.read_csv(direc, dtype = str)
    for id, name in zip(participant_df['id'], participant_df['name']):
        Participant.objects.get_or_create(id = id, name = name)

    for folder in os.listdir(os.path.join(base_dir, "Database"))[:3]:
        print (folder)
        all_files = sorted (os.listdir(os.path.join(base_dir, "Database", folder)))[:]

        for file, yesterday_file in zip(all_files[:-1], all_files[1:]):

            file_dir = os.path.join(base_dir, "Database", folder, file)
            df = _open_csv_files(file_dir)

            yesterday_file_dir = os.path.join(base_dir, "Database", folder, yesterday_file)
            yesterday_df = _open_csv_files(yesterday_file_dir)

            for participant_id in set(
                list(df['Participant ID'].values) + list(yesterday_df['Participant ID'].values)
            ):

                participant_dict_of_info = _get_diff_values(
                    df,
                    yesterday_df,
                    participant_id
                )

                ShareholdingInfo.objects.get_or_create(
                    participant = Participant.objects.get_or_create(
                        id = participant_dict_of_info['Participant ID']
                        )[0],
                    name = participant_dict_of_info['Name'],
                    address = participant_dict_of_info['Address'],
                    percentage = participant_dict_of_info['percentage'],
                    shareholding = participant_dict_of_info['Shareholding'],
                    date = participant_dict_of_info['Date'],
                    stock = Stock.objects.get_or_create(
                        id = participant_dict_of_info['Stockcode']
                        )[0],
                    absolute_difference = participant_dict_of_info['absolute_difference'],
                    difference_percentage = participant_dict_of_info['difference_percentage'],
                )

class Migration(migrations.Migration):

    dependencies = [
        ('shareholding', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate,)
    ]

############################################################################
######### Functions for helping the populate function ######################

def _open_csv_files(file_dir):

    df = pd.read_csv(file_dir, dtype = str)

    df['Shareholding'] = df['Shareholding'].astype('int64')
    df['percentage'] = df['percentage'].astype(float)
    df['Date'] = pd.to_datetime(df['Date'])

    map_of_nan_ids = df[df['Participant ID'].isna()].index

    df.loc[map_of_nan_ids, 'Participant ID'] = \
        df.loc[map_of_nan_ids, 'Name'].map(_generate_id)

    return df

def _generate_id(name):
    name = name.split(" ")
    id = ""
    for word in name:
        id += word[:2]
    return id


def _get_diff_values(today_df, yesterday_df, participant_id):

    today_dict = today_df[(today_df['Participant ID'] == participant_id)].to_dict('records')
    yesterday_dict = yesterday_df[(yesterday_df['Participant ID'] == participant_id)].to_dict('records')

    if len(today_dict) == 1 and len(yesterday_dict) == 1:
        today_dict = today_dict[0]
        yesterday_dict = yesterday_dict[0]
        today_dict['absolute_difference'] = \
            today_dict['Shareholding'] - yesterday_dict['Shareholding']
        today_dict['difference_percentage'] = \
            today_dict['absolute_difference'] / yesterday_dict['Shareholding'] * 100

        return today_dict

    elif len(today_dict) == 1 and len(yesterday_dict) == 0:
        today_dict = today_dict[0]
        today_dict['absolute_difference'] = today_dict['Shareholding']
        today_dict['difference_percentage'] = 100

        return today_dict

    elif len(today_dict) == 0 and len(yesterday_dict) == 1:
        yesterday_dict = yesterday_dict[0]
        yesterday_dict['absolute_difference'] = -yesterday_dict['Shareholding']
        yesterday_dict['difference_percentage'] = -100

        return yesterday_dict

    else:
        print (participant_id)
        print (yesterday_dict)
        print (today_dict)
        raise ValueError ("Something happened")