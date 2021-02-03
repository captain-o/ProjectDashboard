#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import csv
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
from datetime import datetime
from scipy.interpolate import interp1d
import datetime
import xlrd
import openpyxl

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

##########import Datasets##############
#barchart of unemployment and reduced working hours in Germany and France

kurzarbeitDE = pd.read_csv("kurzarbeitDE.CSV", sep=";", encoding = "ISO-8859-1")
arbeitslosigkeitFR = pd.read_csv("unemplyomentFrance_rel.csv", sep=";", encoding = "ISO-8859-1")
arbeitslosigkeitDE = pd.read_csv("ArbeitslosenzahelnDE.csv", sep=";", encoding = "ISO-8859-1")
#kurzarbeitFR =

#plot unemployment and corona in german unemplStates
corona_Ger_state_d = pd.read_csv("CoronaCasesPerBL_Weekly.csv", sep=",", encoding = "ISO-8859-1")
unemp_Ger_state_m = pd.read_csv("unempGerStates_monthly.CSV", sep=";", encoding = "ISO-8859-1")
#print(corona_Ger_state_d.head())
#print(unemp_Ger_state_m.head())

#plot unemployment and corona in french regions
corona_fr_dep_d = pd.read_csv("CoronaCasesParRegion_Weekly.csv", sep=",", encoding = "ISO-8859-1")
#print(corona_fr_dep_d.head())
unemp_Fr_state_q = pd.read_csv("UnemploymentRegionFR_quarterly.csv", sep=";", encoding = "ISO-8859-1")
unemp_Fr_state_q = unemp_Fr_state_q.drop(unemp_Fr_state_q.index[:-8])
#print(unemp_Fr_state_q.head())

#business failures
businessFail_FR = pd.read_csv("BusinessFailuresRegion_FR.csv", sep=";", encoding = "ISO-8859-1")
businessFail_FR = businessFail_FR.drop(businessFail_FR.index[:-24])
businessFail_DE = pd.read_csv("BusinessFailureLaender_DE.csv", sep=",", encoding = "ISO-8859-1")
#print(businessFail_DE)

#stock Market
stock_FR = pd.read_csv("Stock_Fr.csv", sep=";")
stock_DE = pd.read_csv("Stock_De.csv", sep=";")

#measuresFrance
measuresFrance = pd.read_csv("measuresFreance_test.CSV", sep=";", encoding = "ISO-8859-1")


def transfromDateFormat(df_us):
    for col in df_us.columns:
        if(col == "Country" or col == "Lat" or col == "Long" ):
            x=5
        else:
            eDate=datetime.datetime.strptime(col, '%m/%d/%y').strftime('%Y-%m-%d')
            df_us=df_us.rename(columns = {col:eDate})
    return df_us

# loading the dataset
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')


# droping the 'Province/State' columns as it containd null values
death_df.drop('Province/State', axis=1, inplace=True)
#death_df.drop('Lat', axis=1, inplace=True)
#death_df.drop('Long', axis=1, inplace=True)
confirmed_df.drop('Province/State', axis=1, inplace=True)
#confirmed_df.drop('Lat', axis=1, inplace=True)
#confirmed_df.drop('Long', axis=1, inplace=True)
recovered_df.drop('Province/State', axis=1, inplace=True)
country_df.drop(['People_Tested', 'People_Hospitalized'], axis=1, inplace=True)

# change columns name
death_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
confirmed_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
recovered_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
country_df.rename(columns={'Country_Region': 'Country', 'Long_': 'Long'}, inplace=True)

#transfromDateFormat
confirmed_df=transfromDateFormat(confirmed_df)
death_df=transfromDateFormat(death_df)
recovered_df=transfromDateFormat(recovered_df)
#print(confirmed_df.head())




### CREATE THE DATASET FOR GDP FOR FR AND GR
df_GDP= pd.read_csv('GDP_nouveau.CSV', sep=";", encoding = "ISO-8859-1")
#print(df_GDP.head())
df_GDP=df_GDP.loc[df_GDP['GEO (Labels)'].isin(['France', 'Germany'])]
#print(df_GDP.head())

df_GDP=df_GDP.rename(columns = {'GEO (Labels)':'Country'})
df_GDP=df_GDP.rename(columns = {'2019-Q1':'2019-03-31'})
df_GDP=df_GDP.rename(columns = {'2019-Q2':'2019-06-30'})
df_GDP=df_GDP.rename(columns = {'2019-Q3':'2019-09-30'})
df_GDP=df_GDP.rename(columns = {'2019-Q4':'2019-12-31'})
df_GDP=df_GDP.rename(columns = {'2020-Q1':'2020-03-31'})
df_GDP=df_GDP.rename(columns = {'2020-Q2':'2020-06-30'})
df_GDP=df_GDP.rename(columns = {'2020-Q3':'2020-09-30'})
#print(df_GDP.head())


import urllib.request, json

with urlopen('https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/2_bundeslaender/4_niedrig.geo.json') as response:
    mapgermany = json.load(response)


#with urllib.request.urlopen("https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/2_bundeslaender/4_niedrig.geo.json") as url:
    #print(url.info().get_param('charset'))
#    mapgermany = json.loads(url.read().decode('iso-8859-1'))
    #'iso-8859-1'))
with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson') as response:
    mapfrance = json.load(response)

    #url.info().get_param('charset')
#with urllib.request.urlopen("https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson") as url:
#    mapfrance = json.loads(url.read().decode('iso-8859-1'))


#################components######################
navbar = dbc.NavbarSimple(
    children=[
        #dbc.NavItem(html.A("Daily Data", href="#nav-daily-graph", style = {'color': '#fff'}), className="mr-3"),
        #dbc.NavItem(html.A("Most effected", href="#nav-top-country-graph", style = {'color': '#fff'}), className="mr-3"),
        #dbc.NavItem(html.A("Comparison", href="#nav-cr-link", style = {'color': '#fff'}), className="mr-3"),
        #dbc.NavItem(html.A("GDP & Max infection rate", href="#nav-GDP", style = {'color': '#fff'}), className="mr-3"),
        #dbc.NavItem(html.A("Stock Market", href="#nav-stock-market", style = {'color': '#fff'}), className="mr-3"),
        #dbc.NavItem(html.A("Unemployment of Germany and France", href="#nav-unemp", style = {'color': '#fff'}), className="mr-3")
    ],
    brand="Impact of Covid19 measures on economy and the pandemic",
    brand_href="/",
    color="dark",
    dark=True,
    className="p-3 fixed-top"
)

# main heading
main_heading = dbc.Container(
[
    html.H1(["Economic Impact Of The COVID-19 Pandemic"], className="my-5 pt-5 text-center"),
 ]
, className='pt-3')

# what is covid-19
what_is_covid = dbc.Container(
    [
        html.Div([
            html.H3('What is COVID-19?'),
            html.P("Coronavirus disease 2019 (COVID-19) is a contagious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The first case was identified in Wuhan, China, in December 2019. It has since spread worldwide, leading to an ongoing pandemic."),
            html.P("COVID-19 is caused by infection with the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) virus strain."),
            html.Span('More information '),
            dcc.Link('here', href = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019')
        ])
    ]
, className="mb-5")

world_tally = dbc.Container(
    [
        html.H2('World Data', style = {'text-align': 'center'}),
        dbc.Row(
            [
                dbc.Col(children = [html.H4('Confirmed'),
                        html.Div(country_df['Confirmed'].sum(), className='text-info', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                dbc.Col(children = [html.H4('Recovered', style = {'padding-top': '0px'}),
                        html.Div(country_df['Recovered'].sum(), className='text-success', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                dbc.Col(children = [html.H4('Death', style = {'padding-top': '0px'}),
                        html.Div(country_df['Deaths'].sum(), className='text-danger', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                dbc.Col(children = [html.H4('Active'),
                        html.Div(country_df['Active'].sum(),className='text-warning', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
        , className='my-4 shadow justify-content-center'),
    ]
)

# ploting world map
# fixing the size of circle to plot in the map

margin = country_df['Confirmed'].values.tolist()
circel_range = interp1d([1, max(margin)], [0.2,12])
circle_radius = circel_range(margin)

# global map heading
global_map_heading = html.H2(children='World map view', className='mt-5 py-4 pb-3 text-center')
# ploting the map
map_fig = px.scatter_mapbox(country_df, lat="Lat", lon="Long", hover_name="Country", hover_data=["Confirmed", "Deaths"],
                        color_discrete_sequence=["#EF553B"], zoom=2, height=500, size_max=50, size=circle_radius)
map_fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0}, height=520)
#link for change color: https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express
#link for change mapbox style: https://plotly.com/python/mapbox-layers/

# daily data heading
daily_graph_heading_Fr = html.H2(id='nav-daily-graph-Fr', children='COVID-19 daily data and Total cases ', className='mt-5 pb-3 text-center')
daily_graph_heading_De = html.H2(id='nav-daily-graph-De', children='COVID-19 daily data and Total cases ', className='mt-5 pb-3 text-center')
daily_country = confirmed_df['Country'].unique().tolist()
daily_country_list = []

my_df_type = ['Confirmed cases', 'Death cases']
my_df_type_list = []

for i in daily_country:
    daily_country_list.append({'label': i, 'value': i})

for i in my_df_type:
    my_df_type_list.append({'label': i, 'value': i})

# dropdown to select country for France
country_dropdown_Fr = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [
                    html.Label('Select Country'),
                    html.Div(
                        dcc.Dropdown(
                            id = 'select-data-Fr',
                            options=[
                                {'label': 'stock market', 'value': 'stock'},
                                {'label': 'GDP', 'value': 'gdp'},
                                {'label': 'unemployment', 'value': 'unemp'},
                                {'label': 'consumption', 'value': 'cons'}
                            ],
                            value='gdp'
                        )
                    )
                ],width=3, className='p-2 mr-2'),

                dbc.Col(children = [html.Label('Drage to choose no of Days', style = {'padding-top': '0px'}),
                        html.Div(dcc.Slider( id = 'select-date-Fr',
                                            min=10,
                                            max=len(death_df.columns[3:]),
                                            step=1,
                                            value=365
                                        ,className='p-0'), className='mt-3')],
                        width=3, className='p-2 mx-2'),

                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}),
                        html.Div(dcc.Dropdown(id = 'select-category-Fr', options = my_df_type_list, value='Confirmed cases'))],
                        width=3, className='p-2 ml-2'),
            ]
        , className='my-4 justify-content-center'),

    ]
)

# dropdown to select country for Germany
country_dropdown_De = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [
                    html.Label('Select Country'),
                    html.Div(
                        dcc.Dropdown(
                            id = 'select-data-De',
                            options=[
                                {'label': 'stock market', 'value': 'stock'},
                                {'label': 'GDP', 'value': 'gdp'},
                                {'label': 'unemployment', 'value': 'unemp'},
                                {'label': 'consumption', 'value': 'cons'}
                            ],
                            value='gdp'
                        )
                    )
                ],width=3, className='p-2 mr-2'),

                dbc.Col(children = [html.Label('Drage to choose no of Days', style = {'padding-top': '0px'}),
                        html.Div(dcc.Slider( id = 'select-date-De',
                                            min=10,
                                            max=len(death_df.columns[3:]),
                                            step=1,
                                            value=365
                                        ,className='p-0'), className='mt-3')],
                        width=3, className='p-2 mx-2'),

                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}),
                        html.Div(dcc.Dropdown(id = 'select-category-De', options = my_df_type_list, value='Confirmed cases'))],
                        width=3, className='p-2 ml-2'),
            ]
        , className='my-4 justify-content-center'),

    ]
)



# create graph for daily report




end = html.Div(children= [
        html.H3('Sources:'),
        html.Div([html.Span('1. The data is taken from '), dcc.Link('Johns Hopkins University', href='https://github.com/CSSEGISandData/COVID-19')]),
        html.Div([html.Span('2. Build this Dashboard using '), dcc.Link('Plotly', href='https://plotly.com/python/')]),
        html.Div([html.Span('3. Get the source code from our '), dcc.Link('github repo', href='...')]),
        html.H5('Note: Will be updating this Dashboard with more features and better visualization.', style = {'margin-top': '20px', 'margin-bottom': '140px'})
])

#barchart of unemployment and reduced working hours in Germany and France
unempBarFig = go.Figure(
    data=[
        go.Bar(
            name="Unemployment France",
            x=arbeitslosigkeitFR["date"],
            y=arbeitslosigkeitFR["rel"],
            offsetgroup=0,
        ),
        go.Bar(
            name="Unemployment Germany",
            x=arbeitslosigkeitDE["date"],
            y=arbeitslosigkeitDE["rel"],
            offsetgroup=1,
        ),
        go.Bar(
            name="Kurzarbeit Germany",
            x=kurzarbeitDE["date"],
            y=kurzarbeitDE["rel"],
            offsetgroup=1,
            base=arbeitslosigkeitDE["rel"],
        )
    ],
    layout=go.Layout(
        title="Unemploymentand Kurzarbeit in Germany and France",
        yaxis_title="Percentage of unemployment"
    )
)

# ploting world map
# fixing the size of circle to plot in the map
margin = country_df['Confirmed'].values.tolist()
circel_range = interp1d([1, max(margin)], [0.2,12])
circle_radius = circel_range(margin)




app.layout = html.Div(children=[
    navbar,
    #main_heading,
    #what_is_covid,
    ############
    world_tally,


    html.Div([
        dbc.Row([
            dbc.Col([
                # daily report graph
                dbc.Container([
                    daily_graph_heading_Fr,
                    country_dropdown_Fr,
                    html.Div(id='country-total'),
                    ##########
                    dcc.Graph(id='daily-graphs-Fr' )
                ])
            ], width=6),
            dbc.Col([
                # daily report graph
                dbc.Container([
                    daily_graph_heading_De,
                    country_dropdown_De,
                    html.Div(id='country-total-De'),
                    ##########
                    dcc.Graph(id='daily-graphs-De' )
                ])
            ], width=6)


        ])


    ]),


    html.Div([
        dbc.Row([
           dbc.Col(children = [

                dl.Map(center=[47, 2], zoom=4, children=[
                   dl.TileLayer(),
                   #dl.GeoJSON(url='https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/2_bundeslaender/4_niedrig.geo.json', id="capitals",
                   dl.GeoJSON(data = mapfrance, id="region_FR",
                   #url='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson'
                   #url='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson'
                        hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),  # geojson resource (faster than in-memory)
                        ], style={'width': '28vh', 'height': '35vh', 'margin': "auto", "display": "block"}, id="mapFR"
                )
           ], width=2),
           dbc.Col(children = [
               dcc.RadioItems(
                   id='selDatFR',
                   options=[
                       {'label': 'unemployment', 'value': 'unemp'},
                       {'label': 'business failures', 'value': 'bf'},
                       {'label': 'foundation of enterprises', 'value': 'fe'}
                           ],
                       value='unemp',
                       labelStyle={'display': 'inline-block'}
               ),
               dcc.Graph(id="coronaRegionFR",style={'width': '90%'})
           ], width=4, style={'display': 'inline-block', "border":"2px black solid"}),

           dbc.Col(children=[

                dl.Map(center=[51, 10], zoom=5, children=[
                   dl.TileLayer(),
                   dl.GeoJSON(data = mapgermany, id="laender_DE",
                   #url='https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/2_bundeslaender/4_niedrig.geo.json'
                   #dl.GeoJSON(url='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson', id="capitals",
                        hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),  # geojson resource (faster than in-memory)
                        ], style={'width': '28vh', 'height': '35vh', 'margin': "auto", "display": "block"}, id="mapDE")
                #html.Div(id="selectedStateDE"),
                #dcc.Graph(id="coronaRegionDE")
           ], width=2, style={'vertical-align': 'bottom'}),
           dbc.Col(children = [
               dcc.RadioItems(
                   id='selDatDE',
                   options=[
                       {'label': 'unemployment', 'value': 'unemp'},
                       {'label': 'business failures', 'value': 'bf'},
                       {'label': 'foundation of enterprises', 'value': 'fe'}
                           ],
                       value='unemp',
                       labelStyle={'display': 'inline-block'}
               ),
               dcc.Graph(id="coronaRegionDE", style={'width': '90%'})

           ], width=4, style={'display': 'inline-block', "border":"2px black solid"})
       ], align='center')
    ], style={"border":"2px black solid"}),

    # global map
    html.Div(children = [global_map_heading,
        dcc.Graph(
            id='global_graph',
            figure=map_fig
        )
    ]),





    dcc.Graph(
        id='unempGerFra',
        figure=unempBarFig
    )
], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 20, 'marginRight' :20})



@app.callback(
    Output("coronaRegionDE", "figure"), [Input("laender_DE", "click_feature")], [Input("selDatDE", "value")])
def display_corona_cases(feature, value):
    if feature is not None:
        curState = feature['properties']['name']
        print(curState)

        #writeTofile("mapData: " + curState)
        curState = curState.encode().decode('ISO-8859-1')
        #print(curState)

        #writeTofile("fixed?: " + fixedFile)
        selectedStateBF = businessFail_DE[businessFail_DE["Bundesland"]==curState]
        selectedStateCorona = corona_Ger_state_d[corona_Ger_state_d["Bundesland"]==curState]


        #writeTofile("map df: " + str(selectedStateCorona.head()))
        #fig_corona_state = px.line(selectedStateUnemp, title='Corona cases in ' + stateDe, labels={'week':"Woche"})
        fig_region_DE = make_subplots(specs=[[{"secondary_y": True}]])
        fig_region_DE.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["FaelleProWoche"], name="corona cases"),
            secondary_y=False,
        )


        if (value == "unemp"):
            data = unemp_Ger_state_m
            fig_region_DE.add_trace(
                go.Scatter(x=data["date"], y= data[curState], name="unemp Data"),
                secondary_y=True,
            )
        elif (value == "bf"):
            print(curState)

            #print(selectedStateBF.head())
            selectedStateBF = selectedStateBF.drop(selectedStateBF.index[:-24])
            fig_region_DE.add_trace(
                go.Scatter(x=selectedStateBF["date"], y= selectedStateBF['SumOfBankrupcies'], name="business failures"),
                secondary_y=True,
            )



        fig_region_DE.update_xaxes(title_text="Corona and Unemployment in " + curState)
        fig_region_DE.update_yaxes(
            title_text="unemployment in percent",
            secondary_y=True)

        fig_region_DE.update_yaxes(
            title_text="Corona cases per day",
            secondary_y=False)
        fig_region_DE.update_layout(title_text=curState)
        return fig_region_DE
    else:
        curState ="Bayern"
        selectedStateCorona = corona_Ger_state_d[corona_Ger_state_d["Bundesland"]==curState]
        #fig_corona_state = px.line(selectedStateUnemp, title='Corona cases in ' + stateDe, labels={'week':"Woche"})
        fig_region_DE = make_subplots(specs=[[{"secondary_y": True}]])
        fig_region_DE.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["FaelleProWoche"], name="corona cases"),
            secondary_y=False,
        )
        fig_region_DE.update_yaxes(
            title_text="Corona cases per day",
            secondary_y=False)
        fig_region_DE.update_layout(title_text=curState)
        return fig_region_DE



###https://plotly.com/python/multiple-axes/

@app.callback(
    Output("coronaRegionFR", "figure"),[Input("region_FR", "click_feature")],[Input("selDatFR", "value")])
def capital_click(feature, value):
    if feature is not None:
        curState = feature['properties']['nom']
        print(curState)
        #print(value)
        selectedStateCorona = corona_fr_dep_d[corona_fr_dep_d["Region"]==curState]
        '''
        fig_coronaRegionFR = px.line(selectedStateCorona, x = selectedStateCorona["Date"], y =selectedStateCorona["Cases"])
        '''
        #print(corona_fr_dep_d[corona_fr_dep_d["Region"]==curState].head())
        fig_coronaRegionFR = make_subplots(specs=[[{"secondary_y": True}]])
        fig_coronaRegionFR.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["PosCasesPerWeek"], name = "Corona cases"),
            secondary_y=False,
        )

        if (value == "unemp"):
            data = unemp_Fr_state_q
            fig_coronaRegionFR.add_trace(
                go.Scatter(x=data["date"], y= data[curState], name="unemp Data"),
                secondary_y=True,
            )
        elif (value == "bf"):
            data = businessFail_FR

            fig_coronaRegionFR.add_trace(
                go.Scatter(x=data["date"], y= data[curState], name="business failues"),
                secondary_y=True,
            )
            '''
        fig_coronaRegionFR['layout'].update(annotations=[dict(
                                            x="2020-08-30",  # annotation point
                                            xref='x1',
                                            yref='y1',
                                            text='dict Text',
                                            showarrow=True,
                                            arrowhead=7,
                                            ax=10,
                                            ay=70
        )])

        fig_coronaRegionFR.add_vline(x="2020-08-30", line_width=3, line_dash="dash", line_color="black", opacity = 0.5)
        '''
        #, hovertext = "bla"
        #, annotation_text="blabla"
        fig_coronaRegionFR.update_yaxes(
            title_text="Corona cases per day",
            secondary_y=False)
        fig_coronaRegionFR.update_layout(title_text=curState)
        return fig_coronaRegionFR
    else:
        curState = "Normandie"
        selectedStateCorona = corona_fr_dep_d[corona_fr_dep_d["Region"]==curState]

        fig_coronaRegionFR = make_subplots(specs=[[{"secondary_y": True}]])
        fig_coronaRegionFR.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["PosCasesPerWeek"], name = "corona cases"),
            secondary_y=False,
        )

        for label, content in measuresFrance.iteritems():
            measures = ""
            for row in content:
                measures = measures + str(row) + "<br>"
            fig_coronaRegionFR.add_trace(go.Scatter(x=[label, label], y=[-1,12000], mode="lines", line_color = "black", opacity=0.1, name="Lockdown", hoverinfo = "text", text = measures + label))

        #measuresFrance
        fig_coronaRegionFR.update_layout(hovermode='x')


        fig_coronaRegionFR.update_yaxes(title_text="Corona cases per day", secondary_y=False)
        fig_coronaRegionFR.update_layout(title_text=curState)
        return fig_coronaRegionFR




def daily_graph_gen_Fr(new_df, category, data):

    #print(new_df.loc[new_df['Date']== "2020-12-31"])
    #cut data after 31.12.2020
    new_df = new_df[:334]
    daily_data = make_subplots(specs=[[{"secondary_y": True}]])
    daily_data.add_trace(
        go.Scatter(x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 daily report", line=dict(color='#f36')),
        secondary_y=False,
    )
    daily_data.update_layout(height=450,  title = category +'  in ' + new_df['Country'].values[0], )
    daily_data.update_xaxes(title_text="Date", title='Date', title_font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
    )

    if (data == 'gdp'):
        df_data = df_GDP.copy(deep=True)
        df_data = (df_data.transpose())
        df_data = df_data.drop(["Country"])

        daily_data.add_trace(
            go.Scatter(x=df_data.index, y=df_data[13], name="GDP", line=dict(color='black')),
            secondary_y=True,
        )
    elif(data == 'stock'):
        #print(stock_DE.head())
        daily_data.add_trace(
            go.Scatter(x=stock_FR['Date'], y=stock_FR['Close'], name="CAC", line=dict(color='black')),
            secondary_y=True,
        )
    elif(data == 'unemp'):
        df = 'unemp'
    elif(date == 'cons'):
        df = 'consumption'

    return daily_data


def daily_graph_gen_De(new_df, category, data):
    daily_data = make_subplots(specs=[[{"secondary_y": True}]])
    ###########################################################################


    #cut data after 31.12.2020
    new_df = new_df[:334]

    ###########################################################################

    daily_data.add_trace(
        go.Scatter(x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 daily report", line=dict(color='#f36')),
        secondary_y=False,
    )
    daily_data.update_layout(height=450,  title = category +'  in ' + new_df['Country'].values[0], )
    daily_data.update_xaxes(title_text="Date", title='Date', title_font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
    )

    if (data == 'gdp'):
        df_data = df_GDP.copy(deep=True)
        df_data = (df_data.transpose())
        df_data = df_data.drop(["Country"])
        #print(df_data.head())
        daily_data.add_trace(
            go.Scatter(x=df_data.index, y=df_data[8], name="GDP", line=dict(color='black')),
            secondary_y=True,
        )
    elif(data == 'stock'):
        #print(stock_DE.head())
        daily_data.add_trace(
            go.Scatter(x=stock_DE['Date'], y=stock_DE['Close'], name="DAX", line=dict(color='black')),
            secondary_y=True,
        )
    elif(data == 'unemp'):
        df = 'unemp'
    elif(date == 'cons'):
        df = 'consumption'

    return daily_data


@app.callback(
     Output('daily-graphs-De', 'figure'),
     [Input('select-data-De', 'value'),
      Input('select-category-De', 'value'),
      Input('select-date-De', 'value')]
)

def country_wise(data, df_type, number):
    country_name = 'Germany'
    # on select of category copy the dataframe to group by country
    if df_type == 'Confirmed cases':
        df_type = confirmed_df.copy(deep=True)
        category = 'COVID-19 confirmed cases'

    elif df_type == 'Death cases':
        df_type = death_df.copy(deep=True)
        category = 'COVID-19 Death rate'

    # group by country name
    country = df_type.groupby('Country')

    # select the given country
    country = country.get_group(country_name)


    # store daily death rate along with the date
    daily_cases = []
    case_date = []

    # iterate over each row
    for i, cols in enumerate(country):
        if i > 3:
            # take the sum of each column if there are multiple columns
            daily_cases.append(country[cols].sum())
            case_date.append(cols)
            zip_all_list = zip(case_date, daily_cases)

            # creata a data frame
            new_df = pd.DataFrame(data = zip_all_list, columns=['Date','coronavirus'])

    # append the country to the data frame
    new_df['Country'] = country['Country'].values[0]

    # get the daily death rate
    new_df2 = new_df.copy(deep=True)
    for i in range(len(new_df) -1):
        new_df.iloc[i+1, 1] = new_df.iloc[1+i, 1] - new_df2.iloc[i, 1]
        if new_df.iloc[i+1, 1] < 0:
            new_df.iloc[i+1, 1] = 0



    new_df = new_df.iloc[-number:]
    return (daily_graph_gen_De(new_df, category, data))

@app.callback(
     Output('daily-graphs-Fr', 'figure'),
     [Input('select-data-Fr', 'value'),
      Input('select-category-Fr', 'value'),
      Input('select-date-Fr', 'value')]
)

def country_wise(data, df_type, number):
    country_name = 'France'
    # on select of category copy the dataframe to group by country
    if df_type == 'Confirmed cases':
        df_type = confirmed_df.copy(deep=True)
        category = 'COVID-19 confirmed cases'

    elif df_type == 'Death cases':
        df_type = death_df.copy(deep=True)
        category = 'COVID-19 Death rate'
    '''
    else:
        df_type = df_GDP.copy(deep=True)
        category = 'GDP'
        '''
    #else:
        #df_type = recovered_df.copy(deep=True)
        #category = 'COVID-19 recovered cases'


    # group by country name
    country = df_type.groupby('Country')

    # select the given country
    country = country.get_group(country_name)
    #print(country.head())

    # store daily death rate along with the date
    daily_cases = []
    case_date = []

    # iterate over each row
    for i, cols in enumerate(country):
        if i > 3:
            # take the sum of each column if there are multiple columns
            daily_cases.append(country[cols].sum())
            case_date.append(cols)
            zip_all_list = zip(case_date, daily_cases)

            # creata a data frame
            new_df = pd.DataFrame(data = zip_all_list, columns=['Date','coronavirus'])

    # append the country to the data frame
    new_df['Country'] = country['Country'].values[0]

    # get the daily death rate
    new_df2 = new_df.copy(deep=True)
    for i in range(len(new_df) -1):
        new_df.iloc[i+1, 1] = new_df.iloc[1+i, 1] - new_df2.iloc[i, 1]
        if new_df.iloc[i+1, 1] < 0:
            new_df.iloc[i+1, 1] = 0

    new_df = new_df.iloc[-number:]


    return (daily_graph_gen_Fr(new_df, category, data))

if __name__ == '__main__':
    app.run_server(debug=True)
