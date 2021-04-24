from flask import Flask, jsonify
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import chart_studio.plotly as py
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
engine = create_engine('postgres://postgres:2903@localhost:5432/nobel_winners')

df = pd.read_csv("nobel_organizations.csv")

ncses_df = pd.read_csv("./ncsesdata.csv")

app = Flask(__name__)
CORS(app)


@ app.route("/api/usorgs")
def orgs():
    data = engine.execute(
        "SELECT organization, lat, lon, orgcount FROM usanobel GROUP BY organization, lat, lon, orgcount;")

    lat_list = []
    lng_list = []
    org_list = []
    orgct_list = []

    for row in data.fetchall():
        org = row[0]
        lat = row[1]
        lng = row[2]
        org_ct = row[3]
        lat_list.append(lat)
        lng_list.append(lng)
        org_list.append(org)
        orgct_list.append(org_ct)

    return {
        "org": org_list,
        "lat": lat_list,
        "lng": lng_list,
        "orgct": orgct_list
    }


@ app.route("/api/winners_state")
def winners_state():
    data = engine.execute(
        "SELECT state, COUNT(state) FROM usanobel GROUP BY state ORDER BY COUNT(state) ASC;")

    state_list = []
    count_list = []

    for state, count in data.fetchall():
        state_list.append(str(state))
        count_list.append(int(count))
    print(state_list)
    print(count_list)
    return jsonify([{
        "y": state_list,
        "x": count_list,
        "type": "bar",
        "orientation": "h"
    }])


@ app.route("/api/country")
@ cross_origin()
def country():
    df['country'] = df['country'].replace(["the Netherlands", "Canada", "Italy", "Denmark", "Belgium", "Austria", "Norway", "Israel", "Australia",
                                           "Argentina", "China", "Portugal", "Tunisia", "Finland", "Ireland", "Czech Republic", "Hungary", "Spain", "India"], 'Other')
    vc = df["country"].value_counts()
    print(vc)

    y = []
    for index in list(df["country"].value_counts().values):
        y.append(int(index))

    data = [{
        "x": list(vc.index),
        "y": y,
        "type": "bar",
    }]

    return jsonify(data)


@ app.route("/api/seslider")
@ cross_origin()
def sejobs():
    ncsesF_df = ncses_df[(ncses_df['state'] != 'DC')]
    year = 2008

    scl = [[0.0, '#ecf2f9'], [0.2, '#c6d9ec'], [0.4, '#9fbfdf'],
           [0.6, '#6699cc'], [0.8, '#336699'], [1.0, '#204060']]

    data_slider = []
    for year in ncsesF_df['year'].unique():
        df_segmented = ncsesF_df[(ncsesF_df['year'] == year)].copy()

        for col in df_segmented.columns:
            df_segmented[col] = df_segmented[col].astype(str)

        df_segmented['text'] = df_segmented['se'] + \
            ' (S&E Jobs)  ' + df_segmented['jobs'] + ' (All Jobs)'

        data_each_yr = dict(
            type='choropleth',
            locations=df_segmented['state'].tolist(),
            z=df_segmented['se_jobs'].astype(float).tolist(),
            locationmode='USA-states',
            colorscale=scl,
            text=df_segmented['text'].tolist(),
            colorbar={'title': '% S&E Jobs'})

        data_slider.append(data_each_yr)

    steps = []
    for index in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='Year {}'.format(index + 2008))
        step['args'][1][index] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(title='Science & Engineering Share of All Jobs', geo=dict(scope='usa',
                                                                            projection={'type': 'albers usa'}),
                  sliders=sliders)
    return jsonify({'data': data_slider, 'layout': layout})


@ app.route("/api/rdslider")
@ cross_origin()
def rd():
    ncsesF_df = ncses_df[(ncses_df['state'] != 'DC')]
    year = 2008

    scl = [[0.0, '#ffffff'], [0.2, '#e6f2ff'], [0.4, '#99ccff'],
           [0.6, '#4da6ff'], [0.8, '#0066cc'], [1.0, '#004080']]

    data_slider2 = []
    for year in ncsesF_df['year'].unique():
        df_segmented = ncsesF_df[(ncsesF_df['year'] == year)].copy()

        for col in df_segmented.columns:
            df_segmented[col] = df_segmented[col].astype(str)

        df_segmented['text'] = df_segmented['rd'] + \
            '(R&D)  ' + df_segmented['gdp'] + ' (GDP)'

        data_each_yr = dict(
            type='choropleth',
            locations=df_segmented['state'].tolist(),
            z=df_segmented['rd_gdp'].astype(float).tolist(),
            locationmode='USA-states',
            colorscale=scl,
            text=df_segmented['text'].tolist(),
            colorbar={'title': '% R&D'})

        data_slider2.append(data_each_yr)

    steps = []
    for index in range(len(data_slider2)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider2)],
                    label='Year {}'.format(index + 2008))
        step['args'][1][index] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(title='R&D Portion of GDP', geo=dict(scope='usa',
                                                       projection={'type': 'albers usa'}),
                  sliders=sliders)
    return jsonify({'data': data_slider2, 'layout': layout})


if __name__ == '__main__':
    app.run()
