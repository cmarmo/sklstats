# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

filename = '../data/issues.json'

with open(filename) as f:
    istr = f.read()

ijson = json.loads(istr)
ntot = len(ijson)

number = [ ijson[i]["node"]["number"] for i in range(0, ntot) ]
creatDate = [ ijson[i]["node"]["createdAt"] for i in range(0, ntot) ]
closDate = [ ijson[i]["node"]["closedAt"] for i in range(0, ntot) ]
state = [ ijson[i]["node"]["state"] for i in range(0, ntot) ]
author = []
firstcommentedBy = []
firstcommentedAt = []
for i in range(0, ntot):
    auth = ijson[i]["node"]["author"]
    if (auth != None):
        author.append(auth["login"])
    else:
        author.append("")
    comments = ijson[i]["node"]["comments"]["edges"]
    if (len(comments) > 0):
        if (comments[0]["node"]["author"] != None):
            firstcommentedBy.append(comments[0]["node"]["author"]["login"])
        else:
            firstcommentedBy.append("")
        firstcommentedAt.append(comments[0]["node"]["createdAt"])
    else:    
        firstcommentedBy.append("")
        firstcommentedAt.append("")


crdate = []
cldate = []
answdate = []
duration = []
reaction = []
delta = timedelta(days=1)

for i in range(0, ntot):
    crdate.append(pd.to_datetime(creatDate[i], format='%Y-%m-%dT%H:%M:%SZ'))
    cldate.append(pd.to_datetime(closDate[i], format='%Y-%m-%dT%H:%M:%SZ'))
    if closDate[i] != None:
        duration.append(pd.Timedelta.to_pytimedelta(cldate[i] -
                                                    crdate[i]) / delta )
    else:
        duration.append(None)
    try:
        answdate.append(pd.to_datetime(firstcommentedAt[i],
                                       format='%Y-%m-%dT%H:%M:%SZ'))
        reaction.append(pd.Timedelta.to_pytimedelta(answdate[i] -
                                                    crdate[i]) / delta )
    except:
        answdate.append(None)
        reaction.append(None)

idata = { "Number" : number, "Author" : author, "CreatedAt" : crdate,
            "ClosedAt" : cldate,
            "Duration" : duration, "FcommAuthor" : firstcommentedBy,
            "FcommDate" : answdate, "AnswerTime" : reaction }
df = pd.DataFrame(idata)


app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                dict(
                    x=df[df['Author'] == i]['CreatedAt'],
                    y=df[df['Author'] == i]['ClosedAt'],
                    text=df[df['Author'] == i]['Author'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.Author.unique()
            ],
            'layout': dict(
                xaxis={'title': 'Time of Creation'},
                yaxis={'title': 'Time of closing'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
