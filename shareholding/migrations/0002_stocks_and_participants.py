# Generated by Django 4.1 on 2022-08-15 00:10
from django.db import migrations

import os
import pandas as pd

from ..models import Stock
from ..models import Participant
from ..models import Shareholding

def populate(*ags, **kwargs):

    base_dir = os.path.join('shareholding', 'migrations')

    stock_df = pd.read_csv(os.path.join(base_dir, 'ListofStocks.csv'),
                            index_col = 0,
                            dtype = str)
    for id, name in zip(stock_df['stock_id'], stock_df['stock_name']):
        Stock.objects.get_or_create(id = id, name = name)

    participant_df = pd.read_csv(os.path.join(base_dir,
                                            'ListofParticipants.csv'),
                                dtype = str)
    for id, name in zip(participant_df['id'], participant_df['name']):
        Participant.objects.get_or_create(id = id, name = name)

    for folder in os.listdir(os.path.join(base_dir, "Database"))[:3]:
        for file in os.listdir(os.path.join(base_dir, "Database", folder))[:10]:
            df = pd.read_csv(
                os.path.join(base_dir, "Database", folder, file),
                dtype = str)

            df['Shareholding'] = df['Shareholding'].astype('int64')
            df['percentage'] = df['percentage'].astype(float)
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df['Date'] = df['Date'].dt.tz_convert(tz = 'Asia/Hong_Kong')

            for i, row in df.iterrows():
                Shareholding.objects.get_or_create(
                    participant = Participant.objects.get_or_create(id = row['Participant ID'])[0] ,
                    name = row['Name'],
                    address = row['Address'],
                    shareholding = row['Shareholding'],
                    date = row['Date'],
                    stock = Stock.objects.get_or_create(id = row['Stockcode'])[0] 
                )



class Migration(migrations.Migration):

    dependencies = [
        ('shareholding', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate,)
    ]
