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
from dash.dependencies import Input, Output, State
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
import chardet


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

##########import Datasets##############
#barchart of unemployment and reduced working hours in Germany and France

kurzarbeitDE = pd.read_csv("data/kurzarbeitDE.CSV", sep=";", encoding = "ISO-8859-1")
arbeitslosigkeit_FR = pd.read_csv("data/unemplyomentFrance_rel.csv", sep=",", encoding = "ISO-8859-1")
arbeitslosigkeit_DE = pd.read_csv("data/unemployment_Ger_rel.csv", sep=";", encoding = "ISO-8859-1")
#arbeitslosigkeit_DE = arbeitslosigkeit_FR
#kurzarbeitFR =

#plot unemployment and corona in german unemplStates
corona_Ger_state_d = pd.read_csv("data/CoronaCasesPerBL_Weekly.csv", sep=",", encoding = "ISO-8859-1")
unemp_Ger_state_m = pd.read_csv("data/unempGerStates_monthly.CSV", sep=";", encoding = "ISO-8859-1")

unemp_kurzar_DE = pd.read_csv("data/unemp_Kurzarb_DE.CSV", sep=";", encoding = "ISO-8859-1")

#plot unemployment and corona in french regions
corona_fr_dep_d = pd.read_csv("data/CoronaCasesParRegion_Weekly.csv", sep=",", encoding = "ISO-8859-1")

unemp_Fr_state_q = pd.read_csv("data/UnemploymentRegionFR_quarterly.csv", sep=";", encoding='utf-8')
emppart_Fr_state_q = pd.read_csv("data/activitepartielleFrance_rel.CSV", sep=";", encoding="ISO-8859-1")


#unemp_Fr_state_q = unemp_Fr_state_q.drop(unemp_Fr_state_q.index[:-8])
unemp_Fr_state_q = unemp_Fr_state_q.drop(unemp_Fr_state_q.index[:-8])


#business failures
businessFail_FR = pd.read_csv("data/BusinessFailuresRegion_FR.csv", sep=";", encoding = "utf-8")
businessFail_FR = businessFail_FR.drop(businessFail_FR.index[:-24])
businessFail_DE = pd.read_csv("data/BusinessFailureLaender_DE.csv", sep=",", encoding = "ISO-8859-1")
businessB_F_DE = pd.read_csv("data/BusinessBirth_Failure_DE.csv", sep=",", encoding = "ISO-8859-1")



#stock Market
stock_FR = pd.read_csv("data/Stock_Fr.csv", sep=";")
stock_DE = pd.read_csv("data/Stock_De.csv", sep=";")

#household consumption
hc_DE = pd.read_csv("data/Monthly_Household_consumption_DE.csv", sep=",", encoding = "ISO-8859-1")
hc_FR = pd.read_csv("data/Monthly_Household_consumption_FR.csv", sep=",", encoding = "ISO-8859-1")

#business birts per stateDe
bb_FR = pd.read_csv("data/BusinessBirths_Regionin_FR.csv", sep=",", encoding = "ISO-8859-1")
bb_DE = pd.read_csv("data/BusinessBirths_Regionin_DE.csv", sep=",", encoding = "ISO-8859-1")


#measuresFrance
measuresFrance = pd.read_csv("data/measuresFreance.CSV", sep=";", encoding = "ISO-8859-1")
measuresGermany = pd.read_csv("data/measures_DE.CSV", sep=";", encoding = "ISO-8859-1")


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
df_GDP= pd.read_csv('data/GDP_nouveau.CSV', sep=";", encoding = "ISO-8859-1")
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
    brand="Impact of Covid-19 measures on the economy of France and Germany",
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
                    html.Label('Select Feature'),
                    html.Div(
                        dcc.Dropdown(
                            id = 'select-data-Fr',
                            options=[
                                {'label': 'CAC', 'value': 'stock', 'title':'daily closing value of CAC'},
                                {'label': 'GDP', 'value': 'gdp', 'title':'quarterly GDP'},
                                {'label': 'Unemployment', 'value': 'unemp', 'title':'monthly unemployment in percent and percentage of employees involuntarily working reduced hours'},
                                {'label': 'Consumption', 'value': 'cons', 'title':'monthly absolut houeshold consumption'},
                            ],
                            value='gdp',

                        ),
                    )
                ],width=3, className='p-2 mr-2'),


                dbc.Col(children = [html.Label('Select Indicator', style = {'padding-top': '0px'}),
                        html.Div(
                            dcc.Dropdown(
                                id = 'select-category-Fr',
                                options = [
                                {'label':'Confirmed cases', 'value':'Confirmed cases', 'title':'number of newly infected persons during previos seven days'},
                                {'label':'Death cases', 'value':'Death cases', 'title':'number of deaths during previos seven days'},
                                ],
                                value='Confirmed cases'))],
                        width=3, className='p-2 ml-2'),
            ]
        , className='my-4 justify-content-center'),

    ], style={'margin':'0px', 'height': '80px', 'padding':'0px'}
)

# dropdown to select country for Germany
country_dropdown_De =dbc.Container(
    [
    dbc.Row(
            [
                dbc.Col(children = [
                    html.Label('Select Feature'),
                    html.Div(
                        dcc.Dropdown(
                            id = 'select-data-De',
                            options=[
                                {'label': 'DAX', 'value': 'stock', 'title':'daily closing value of DAX'},
                                {'label': 'GDP', 'value': 'gdp', 'title':'quarterly GDP'},
                                {'label': 'Unemployment', 'value': 'unemp', 'title':'monthly unemployment in percent and percentage of employees involuntarily working reduced hours'},
                                {'label': 'Consumption', 'value': 'cons', 'title':'monthly absolut houeshold consumption'}
                            ],
                            value='gdp'
                        ), style={'margin': "0px", "padding": "0px"}
                    )
                ],width=3, className='p-2 mr-2'),



                dbc.Col(children = [
                    html.Label('Select Indicator', style = {'padding-top': '0px'}),
                        html.Div(
                            dcc.Dropdown(
                                id = 'select-category-De',
                                options = [
                                    {'label':'Confirmed cases', 'value':'Confirmed cases', 'title':'number of newly infected persons during previos seven days'},
                                    {'label':'Death cases', 'value':'Death cases', 'title':'number of deaths during previos seven days'},
                                ],
                                value='Confirmed cases'))],
                        width=3, className='p-2 ml-2'),
            ]
        , className='my-4 justify-content-center')
], style={'margin':'0px', 'height': '80px', 'padding':'0px'}
)


state_dropdown_De =dbc.Container(
    [
    dbc.Row(
            [
                dbc.Col(children = [
                    html.Label('Select Feature'),
                    html.Div(
                        dcc.Dropdown(
                            id='selDatDE',
                            options=[
                                {'label': 'Unemployment', 'value': 'unemp', 'title':'empty'},
                                {'label': 'Business failures', 'value': 'bf', 'title':'empty'},
                                {'label': 'Business birth', 'value': 'fe', 'title':'empty'}
                                    ],
                                value='unemp'
                        ), style={'margin': "0px", "padding": "0px"}
                    )
                ],width=4, className='p-2 mr-2'),



            ]
        , className='my-4 justify-content-center')
], style={'margin':'0px', 'height': '80px', 'padding':'0px'}
)
state_dropdown_Fr =dbc.Container(
    [
    dbc.Row(
            [
                dbc.Col(children = [
                    html.Label('Select Feature'),
                    html.Div(
                        dcc.Dropdown(
                            id='selDatFR',
                            options=[
                                {'label': 'Unemployment', 'value': 'unemp', 'title':'empty'},
                                {'label': 'Business failures', 'value': 'bf', 'title':'empty'},
                                {'label': 'Business birth', 'value': 'fe', 'title':'empty'}
                                    ],
                                value='unemp',
                                style = dict(



                            )
                        ), style={'margin': "0px", "padding": "0px"}
                    )
                ],width=4, className='p-2 mr-2'),



            ]
        , className='my-4 justify-content-center')
], style={'margin':'0px', 'height': '80px', 'padding':'0px'}
)



# create graph for daily report




end = html.Div(children= [
        html.H3('Sources:'),
        html.Div([html.Span('1. The data is taken from '), dcc.Link('Johns Hopkins University', href='https://github.com/CSSEGISandData/COVID-19')]),
        html.Div([html.Span('2. Build this Dashboard using '), dcc.Link('Plotly', href='https://plotly.com/python/')]),
        html.Div([html.Span('3. Get the source code from our '), dcc.Link('github repo', href='...')]),

], style = {'margin-top': '20px', 'margin-bottom': '140px'})



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
    html.Div(
    [
        dbc.Button("Our dashboard shows a different data sets that can be chosen and compared to covid cases. For further information click here.",
            id="open",),
        dbc.Modal(
            [
                dbc.ModalHeader("About this dashboard"),
                dbc.ModalBody(children=[
                    html.P("Impact of Covid-19 measures on the economy of France and Germany. Our dashboard shows a different data sets that can be chosen and compared to covid cases. For further information click here."),
                    html.H4("National Level"),
                    html.P("Here we have a portfolio of indicators that we believe are linked to the pandemic."),
                    html.Li("Stock market. The stock market reacts on all kind of information and thus consider the outbreak of the pandemic as well. We show the stock market from the beginning of march, when the pandemic developed to a hot topic.", style={'margin-left':'30px'}),
                    html.Li("GDP. The change in gross domestic product of a country is as a good indicator of the health of an economy", style={'margin-left':'30px'}),
                    html.Li("Unemployment rate is as well a good indicator on how the economy???s state. We believe it is a suitable addition to the previous two. In both countries is a strong mechanism to handle tough economical situations, called 'Kurzarbeit' and 'Activite partielle'. They have a huge impact on the unemployment rate. therefore we added them to the figure.", style={'margin-left':'30px'}),
                    html.Li("Similar to the GDP is the household consumption. If the households do not consume, the GDP drops.", style={'margin-left':'30px'}),
                    html.H4("Regional Level"),
                    html.P("We thought it might be also interesting to discover similarities and dissimilarities on a smaller scale than on the national level. This is particularly interesting for Germany, where in some states are different restrictions against the spread of the virus, whereas in France which is centrally governed, there might be some interesting dissimilarities found between the metropolitan area and the rural areas. This is up to you to discover where we provide currently 3 regional factors. To choose your region of interest select it by clicking on the map."),
                    html.Li("Unemployment rate: Similarly, to the national level, the unemployment rate is of importance to understand a countries or regions economic health, whereas there might be some different levels in between the country", style={'margin-left':'30px'}),
                    html.Li("Related to this are business failures. The more businesses close, we expect a higher unemployment rate and vice versa. Here we speak of business closings, regardless of the reasons behind it. We wanted to show insolvencies but could not find the proper data for this on the French side.", style={'margin-left':'30px'}),
                    html.Li("In contrast to business failures it could be interesting to see how the foundations of business is in comparison and how they develop during the pandemic.", style={'margin-left':'30px'}),
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal", size="lg", centered=True,
        ),
    ],  style={'textAlign': 'center'}
    ),


    html.Div([
        dbc.Row([
            dbc.Col([
                # daily report graph
                dbc.Container([
                    #FDatedaily_graph_heading_Fr,
                    country_dropdown_Fr,
                    html.Div(id='country-total'),
                    ##########, style={'margin': "0px", "padding": "0px"}
                    dcc.Graph(id='daily-graphs-Fr')
                ])
                #, style={"height": '40vh'}
            ], width=6, className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            dbc.Col([
                # daily report graph

                    #daily_graph_heading_De,
                    country_dropdown_De,
                    html.Div(id='country-total-De', style={'margin':'0px'}),
                    ##########
                    dcc.Graph(id='daily-graphs-De')

            ], width=6, className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'})


        ],style={ 'margin':'0px'})


    ]),


    html.Div([
        dbc.Row([
           dbc.Col(children = [
                html.Label('Data for the regional level in France'),
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
               state_dropdown_Fr,
               dcc.Graph(id="coronaRegionFR",style={'width': '90%'})
           ], width=4, style={'display': 'inline-block'}),

           dbc.Col(children=[
                html.Label('Data for the regional level in Germany. '),
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
               state_dropdown_De,
               dcc.Graph(id="coronaRegionDE", style={'width': '90%'})

           ], width=4, style={'display': 'inline-block'})
       ], align='center', className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'})
    ]),


    html.Div(
    [
        dbc.Button("Learn about our sources",
            id="open_end",),
        dbc.Modal(
            [
                dbc.ModalHeader("Tools and resources:"),
                dbc.ModalBody(children=[
                    html.P("This Dashboard was made using Dash and plotly"),
                    html.P("https://www.insee.fr statistical data for France"),
                    html.P("https://github.com/CSSEGISandData/COVID-19 for national Corona Data"),
                    html.P("https://github.com/kalisio/covid-19 for French Corona data"),
                    html.P("https://de.statista.com for economical data"),
                    html.P("https://fred.stlouisfed.org for monthly unemployment in France"),
                    html.P("https://ec.europa.eu/eurostat for economical data"),
                    html.P("yfinance for stock market data"),
                    html.P("https://www-genesis.destatis.de for German economic data"),
                    html.P("https://npgeo-corona-npgeo-de.hub.arcgis.com for german regional Corona data"),
                    html.P("https://de.wikipedia.org/wiki/COVID-19-Pandemie_in_Deutschland#Situation_ab_Mai_2020 "),
                    html.P("https://raw.githubusercontent.com/isellsoap/ for German map"),
                    html.P("https://raw.githubusercontent.com/gregoiredavid for French map"),




                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_end", className="ml-auto")
                ),
            ],
            id="modal_end", size="lg", centered=True,
        ),
    ],style={'marginTop': 50}
    ),


], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 20, 'marginRight' :20})



@app.callback(
    Output("coronaRegionDE", "figure"), [Input("laender_DE", "click_feature")], [Input("selDatDE", "value")])
def display_corona_cases(feature, value):
    if feature is not None:
        curState = feature['properties']['name']

        curState_raw = curState
        #writeTofile("mapData: " + curState)
        curState = curState.encode().decode('ISO-8859-1')
        #print(curState)

        #writeTofile("fixed?: " + fixedFile)

        selectedStateCorona = corona_Ger_state_d[corona_Ger_state_d["Bundesland"]==curState]


        #writeTofile("map df: " + str(selectedStateCorona.head()))
        #fig_corona_state = px.line(selectedStateUnemp, title='Corona cases in ' + stateDe, labels={'week':"Woche"})
        fig_region_DE = make_subplots(specs=[[{"secondary_y": True}]])
        fig_region_DE.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["FaelleProWoche"], name="corona cases",  line=dict(color='#f36')),
            secondary_y=False,
        )


        if (value == "unemp"):
            data = unemp_Ger_state_m
            fig_region_DE.add_trace(
                go.Scatter(x=data["date"], y= data[curState], name="unemp Data", line=dict(color='black')),
                secondary_y=True,
            )
            fig_region_DE.update_yaxes(
                title_text="unemployment in percent",
                secondary_y=True)
        elif (value == "bf"):

            selectedStateBF = businessB_F_DE[businessB_F_DE["Bundesland"]==curState_raw]

            selectedStateBF = selectedStateBF.drop(selectedStateBF.index[:-24])
            fig_region_DE.add_trace(
                go.Scatter(x=selectedStateBF["Date"], y= selectedStateBF['NumberOfBusinessClosings'], name="business failures", line=dict(color='black')),
                secondary_y=True,
            )
            fig_region_DE.update_yaxes(
                title_text="absolut buseiness failures",
                secondary_y=True)
        elif (value == "fe"):
            selectedStateFE = businessB_F_DE[businessB_F_DE["Bundesland"]==curState_raw]

            fig_region_DE.add_trace(
                go.Scatter(x=selectedStateFE["Date"], y= selectedStateFE['NumberofCompanyBirths'], name="business birts", line=dict(color='black')),
                secondary_y=True,
            )
            fig_region_DE.update_yaxes(
                title_text="absolut buseiness births",
                secondary_y=True)


        #fig_region_DE.update_xaxes(title_text="Corona and Unemployment in " + "Baden-W??rrtemberg")
        fig_region_DE.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        fig_region_DE.update_yaxes(
            title_text="Corona cases per week",
            secondary_y=False)
        fig_region_DE.update_layout(title_text=curState, height =250, margin=dict(b=0, t=25, r=0, l = 0))

        return fig_region_DE
    else:
        curState ="Bayern"
        selectedStateCorona = corona_Ger_state_d[corona_Ger_state_d["Bundesland"]==curState]
        #fig_corona_state = px.line(selectedStateUnemp, title='Corona cases in ' + stateDe, labels={'week':"Woche"})
        fig_region_DE = make_subplots(specs=[[{"secondary_y": True}]])
        fig_region_DE.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["FaelleProWoche"], name="corona cases",  line=dict(color='#f36')),
            secondary_y=False,
        )
        fig_region_DE.update_yaxes(
            title_text="Corona cases per week",
            secondary_y=False)
        fig_region_DE.update_layout(title_text=curState, height =250, margin=dict(b=0, t=25, r=0, l = 0))
        return fig_region_DE



###https://plotly.com/python/multiple-axes/

@app.callback(
    Output("coronaRegionFR", "figure"),[Input("region_FR", "click_feature")],[Input("selDatFR", "value")])
def capital_click(feature, value):
    if feature is not None:
        curState = feature['properties']['nom']
        print(curState)
        curState_raw = curState
        #writeTofile("mapData: " + curState)
        #curState = curState.encode().decode('ISO-8859-1')
        #print(curState)
        selectedStateCorona = corona_fr_dep_d[corona_fr_dep_d["Region"]==curState]
        '''
        fig_coronaRegionFR = px.line(selectedStateCorona, x = selectedStateCorona["Date"], y =selectedStateCorona["Cases"])
        '''
        #print(corona_fr_dep_d[corona_fr_dep_d["Region"]==curState].head())
        fig_coronaRegionFR = make_subplots(specs=[[{"secondary_y": True}]])
        fig_coronaRegionFR.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["PosCasesPerWeek"], name = "Corona cases",  line=dict(color='#f36')),
            secondary_y=False,
        )

        if (value == "unemp"):

            data = unemp_Fr_state_q
            fig_coronaRegionFR.add_trace(
                go.Scatter(x=data["date"], y= data[curState_raw], name="unemp Data", line=dict(color='black')),
                secondary_y=True,
            )
        elif (value == "bf"):
            data = businessFail_FR

            fig_coronaRegionFR.add_trace(
                go.Scatter(x=data["date"], y= data[curState], name="business failues", line=dict(color='black')),
                secondary_y=True,
            )
        elif (value == "fe"):
            selectedStateFE = bb_FR.iloc[:4]
            fig_coronaRegionFR.add_trace(
                go.Scatter(x=selectedStateFE["Date"], y= selectedStateFE[curState], name="business births", line=dict(color='black')),
                secondary_y=True,
            )



        #fig_coronaRegionFR.update_layout(hovermode='x')

        fig_coronaRegionFR.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        #measuresFrance


        fig_coronaRegionFR.update_yaxes(
            title_text="Corona cases per week",
            secondary_y=False)
        fig_coronaRegionFR.update_layout(title_text=curState, height =250, margin=dict(b=0, t=25, r=0, l = 0))
        #, width = 700
        return fig_coronaRegionFR


    else:
        curState = "Normandie"
        selectedStateCorona = corona_fr_dep_d[corona_fr_dep_d["Region"]==curState]

        fig_coronaRegionFR = make_subplots(specs=[[{"secondary_y": True}]])
        fig_coronaRegionFR.add_trace(
            go.Scatter(x = selectedStateCorona["week"], y =selectedStateCorona["PosCasesPerWeek"], name = "corona cases",  line=dict(color='#f36')),
            secondary_y=False,
        )




        fig_coronaRegionFR.update_yaxes(title_text="Corona cases per week", secondary_y=False)
        fig_coronaRegionFR.update_layout(title_text=curState, height =250, margin=dict(b=0, t=25, r=0, l = 0))
        return fig_coronaRegionFR




def daily_graph_gen_Fr(new_df, category, data):

    #print(new_df.loc[new_df['Date']== "2020-12-27"])
    #cut data after 31.12.2020
    new_df = new_df[:50]
    daily_data = make_subplots(specs=[[{"secondary_y": True}]])
    daily_data.add_trace(
        go.Scatter(x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 weekly infections", line=dict(color='#f36')),
        secondary_y=False,
    )
    daily_data.update_layout(height=400, margin=dict(b=0, t=50) )
    #daily_data.update_xaxes(title_text="Date", title='Date', title_font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'))
    daily_data.update_layout(title = category +'  in France with ' + data)

    if (data == 'gdp'):
        df_data = df_GDP.copy(deep=True)
        df_data = (df_data.transpose())
        df_data = df_data.drop(["Country"])

        daily_data.add_trace(
            go.Scatter(x=df_data.index, y=df_data[13], name="GDP", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in France with GDP')
    elif(data == 'stock'):
        #print(stock_DE.head())
        daily_data.add_trace(
            go.Scatter(x=stock_FR['Date'], y=stock_FR['Close'], name="CAC", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in France with CAC')
    elif(data == 'unemp'):
        arbeitslosigkeit_FR_20 = arbeitslosigkeit_FR.iloc[-11:]
        daily_data.add_trace(
            go.Scatter(x=arbeitslosigkeit_FR_20['Date'], y=arbeitslosigkeit_FR_20['rel'], name="rel unemployment", line=dict(color='black')),
            secondary_y=True,
        )
        kurzarbeit_FR_20 = emppart_Fr_state_q.iloc[:4]
        daily_data.add_trace(
            go.Scatter(x=kurzarbeit_FR_20['Date'], y=kurzarbeit_FR_20['relPartielle']*100, name="rel reduced working", line=dict(color='green')),
            secondary_y=True,
        )

        daily_data.update_layout(title = category +'  in France with unemployment quota')
    elif(data == 'cons'):
        hc_FR_20 = hc_FR.iloc[-10:]
        daily_data.add_trace(
            go.Scatter(x=hc_FR_20['Date'], y=hc_FR_20['TotalConsumption'], name="consumption", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in France with household consumption')
    height = new_df['coronavirus'].max()
    for index, row in measuresFrance.iterrows():
        date = row['Date']
        measure = row['Measures']

        daily_data.add_trace(go.Scatter(x=[date, date], y=[-1,height], mode="lines", line_color = "black", opacity=0.2,showlegend=False, hoverinfo = "text", text = measure))

    daily_data.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))



    return daily_data


def daily_graph_gen_De(new_df, category, data):
    daily_data = make_subplots(specs=[[{"secondary_y": True}]])
    #cut data after 31.12.2020
    new_df = new_df[:50]
    #print(new_df.head(60))

    daily_data.add_trace(
        go.Scatter(x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 weekly infections", line=dict(color='#f36')),
        secondary_y=False,
    )
    daily_data.update_layout(height=400,  title = category +'  in Germany with ' + data, margin=dict(b=0, t=50))
    #daily_data.update_xaxes(title_text="Date", title='Date', title_font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'))

    if (data == 'gdp'):
        df_data = df_GDP.copy(deep=True)
        df_data = (df_data.transpose())
        df_data = df_data.drop(["Country"])
        #print(df_data.head())
        daily_data.add_trace(
            go.Scatter(x=df_data.index, y=df_data[8], name="GDP", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in Germany with GDP')
    elif(data == 'stock'):
        #print(stock_DE.head())
        daily_data.add_trace(
            go.Scatter(x=stock_DE['Date'], y=stock_DE['Close'], name="DAX", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in Germany with DAX')
    elif(data == 'unemp'):
        #arbeitslosigkeit_DE_20 = arbeitslosigkeit_DE.iloc[-12:]
        #unemp_kurzar_DE
        daily_data.add_trace(
            go.Scatter(x=unemp_kurzar_DE['Date'], y=unemp_kurzar_DE['relUnemp']*100, name="rel unemployment", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.add_trace(
            go.Scatter(x=unemp_kurzar_DE['Date'], y=unemp_kurzar_DE['relKruzarb']*100, name="rel reduced working", line=dict(color='green')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in Germany with unemployment quota')
    elif(data == 'cons'):
        hc_DE_20 = hc_DE.iloc[-3:]
        daily_data.add_trace(
            go.Scatter(x=hc_DE_20['Date'], y=hc_DE_20['VerbraucherAusgaben'], name="consumption", line=dict(color='black')),
            secondary_y=True,
        )
        daily_data.update_layout(title = category +'  in Germany with household consumption')
    height = new_df['coronavirus'].max()
    for index, row in measuresGermany.iterrows():
        date = row['Date']
        measure = row['Measures']
        daily_data.add_trace(go.Scatter(x=[date, date], y=[-1,height], mode="lines", line_color = "black", opacity=0.2, showlegend=False, hoverinfo = "text", text = measure))

    daily_data.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return daily_data


@app.callback(
     Output('daily-graphs-De', 'figure'),
     [Input('select-data-De', 'value'),
      Input('select-category-De', 'value')]
)

def country_wise(data, df_type):
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


    new_df['Date'] = new_df['Date'].astype('datetime64[ns]')
    new_df = new_df.resample('W-SUN', label='left', on = 'Date').sum().reset_index()

    #new_df = new_df.iloc[-number:]
    return (daily_graph_gen_De(new_df, category, data))

@app.callback(
     Output('daily-graphs-Fr', 'figure'),
     [Input('select-data-Fr', 'value'),
      Input('select-category-Fr', 'value')]
)

def country_wise(data, df_type):
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

    #new_df = new_df.iloc[-number:]
    new_df['Date'] = new_df['Date'].astype('datetime64[ns]')
    new_df = new_df.resample('W-SUN', label='left', on = 'Date').sum().reset_index()


    return (daily_graph_gen_Fr(new_df, category, data))

@app.callback(
Output("modal", "is_open"),
[Input("open", "n_clicks"), Input("close", "n_clicks")],
[State("modal", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
@app.callback(
Output("modal_end", "is_open"),
[Input("open_end", "n_clicks"), Input("close_end", "n_clicks")],
[State("modal_end", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
