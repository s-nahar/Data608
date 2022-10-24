import pandas as pd
import numpy as np
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
trees.head(10)

trees.shape

firstfive_url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5&$offset=0'
firstfive_trees = pd.read_json(firstfive_url)
firstfive_trees


nextfive_url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5&$offset=5'
nextfive_trees = pd.read_json(nextfive_url)
nextfive_trees

boro = 'Bronx'
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,count(tree_id)' +\
        '&$where=boroname=\'Bronx\'' +\
        '&$group=spc_common').replace(' ', '%20')
soql_trees = pd.read_json(soql_url)

soql_trees

'https://api-url.com/?query with spaces'.replace(' ', '%20')

new_url = "https://data.cityofnewyork.us/resource/uvpi-gqnh.json"
select = ["spc_common", "boroname", "steward", "health", "count(health)"]
group = ["spc_common", "boroname", "steward", "health"]
limit = 9999 

trees_url =new_url + "?$select="+",".join(select) + "&$group="+",".join(group) +\
            "&$limit=" + str(limit) 

nyc = pd.read_json(trees_url)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash('HW4', external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(dcc.Dropdown(
                options=nyc['spc_common'][nyc['spc_common'].notnull()].tolist(), 
                value='red maple', 
                id='tree-dropdown',
                className="four columns"
                ),className="row"),
    html.Div(id='plot'),
])

@app.callback(Output('plot','children'),[Input('tree-dropdown', 'value')])
def callback(value):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname,health,count(*)' +\
        '&$where=spc_common=\''+value+'\'' +\
        '&$group=boroname,health' +\
        '&$order=boroname,health').replace(' ', '%20')
    print(soql_url)
    soql_trees = pd.read_json(soql_url)
    

    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
            '$select=boroname,health,steward,count(*)' +\
            '&$where=spc_common=\''+value+'\'' +\
            '&$group=boroname,health,steward' +\
            '&$order=boroname,health,steward').replace(' ', '%20')
    soql_trees2 = pd.read_json(soql_url)
    
    return generate_div(soql_trees, soql_trees2)

def generate_div (soql_trees, soql_trees2) :
    fig_health = px.bar(
        soql_trees, 
        x="health",
        y="count", 
        color="health", 
        facet_col="boroname",
        barmode="group",
        category_orders={
            "health": ["Good", "Fair", "Poor"]
        },
        color_discrete_map={
            'Good': '#00CC96',
            'Fair': '#636EFA',
            'Poor': '#EF553B'
        }
    )
    fig_health.update_traces(width=0.8)

    fig_steward = px.bar(
        soql_trees2,
        x="health",
        y="count",
        color="steward",
        facet_col="boroname",
        barmode="group",
        category_orders={
            "health": ["Good","Fair","Poor"],
            "steward": ["None","1or2","3or4","4orMore"]
        },
        color_discrete_map={
            'None': 'rgb(102,102,102)',
            '1or2': 'rgb(166,118,29)',
            '3or4': 'rgb(230,171,2)',
            '4orMore': 'rgb(102,166,30)',
        }
    )

     return html.Div(
        children=[
            # 1st Row
            html.Div([
                html.H3(children='Health'),

                dcc.Graph(
                    id='health',
                    figure=fig_health
                ),
            ], className='row'),
            # 2nd Row
            html.Div([
                html.H3(children='Steward'),

                dcc.Graph(
                    id='steward',
                    figure=fig_steward
                ),  
            ], className='row'),
    ])  

if __name__ == '__main__':
    app.run_server(debug=True, mode="external")

























