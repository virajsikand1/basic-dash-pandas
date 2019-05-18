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
app.title='Number of Individual Contributors to Presidential Campaigns'
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

###### Import a dataframe #######
df = pd.read_csv('https://raw.githubusercontent.com/virajsikand1/Data_uploads/master/all_candidates_dataset.csv')
colors_list= ['Bernie', 'Warren', 'Kamala', 'Beto', 'Trump']




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
    new_df = df[df['candidate_name'] == '{}'.format(user_input)]
    grouped_df = new_df.groupby(['candidate_name', 'contributor_state'])['contributor_name'].count()
    top_5= grouped_df.sort_values(ascending=False).head()
    top_5=pd.DataFrame(top_5)
    top_5=top_5.reset_index()
    mydata = [go.Bar(
        x=mytop5['contributor_state'],
        y=mytop5['contributor_name']
    )]

    mylayout = go.Layout(
        title='top 5 states with the most individual contributors to {} campaign'.format(user_input),
        xaxis= dict(title='Top 5 States'),
        yaxis= dict(title='Contributor count')
    )
    fig = go.Figure(data=mydata, layout=mylayout)
    return fig

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
