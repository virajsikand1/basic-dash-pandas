######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *


####### Set up your app #####
app = dash.Dash(__name__)
server = app.server
app.title='Titanic!'
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

###### Import a dataframe #######
bernie = pd.read_csv('https://raw.githubusercontent.com/virajsikand1/Data_uploads/master/bernie_condensed.csv')
ind_bernie = bernie [bernie['is_individual'] == 't']
colors_list=['contributor_state', 'contributor_city']




####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a candidate from the list:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in colors_list],
        value=colors_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value')
])


######### Interactive callbacks go here #########
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(user_input):
    results = ind_bernie.groupby(user_input)['contribution_receipt_amount'].sum().sort_values(ascending = False).head(10)
    mydata = [go.Bar(x = results.index,
                     y = results.values,
                     marker = dict(color='blue'))]
    mylayout = go.Layout(title = 'This is a cool bar chart',
                         xaxis = dict(title='this is my x-axis'),
                         yaxis = dict(title='this is my y-axis'))
    myfig = go.Figure(data=mydata, layout=mylayout)
    return myfig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
