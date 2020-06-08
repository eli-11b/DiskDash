import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import getpass


#####################

name = "filename"
user = getpass.getuser()
UPLOAD_DIRECTORY = "~/Users/"+user+"/Documents/Data/"
path = str("~/Documents/"+name+".csv") #"C:\\Users\\"+user+"\\Documents\\"+name+".csv"
df = pd.read_csv(path)
######################

card2_amount= round(df["AVAIL"].iloc[0]/(1024**2),2)
card3_amount= round(df["USED"].iloc[0]/(1024**2),2)





if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

server = Flask(__name__)
app = dash.Dash(server=server,external_stylesheets=external_stylesheets)

card1_contents = [dbc.Card([
    html.H4("CSV Upload", className="card-title", style={"textAlign": "center",
                                                         "margin": "10px",
                                                         "background-color": "#767ecf",
                                                         "color": "white",
                                                         "font-size": "12px",
                                                         "padding": "5px",
                                                         "display": "inline-block"}),
    dbc.CardBody([
    ]),
    dcc.Upload(
        id="upload-data",
        children=html.Div(["Click/Drag & Drop"]),
        style={
            "width": "auto", #auto
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "textAlign": "center",
            "margin": "10px", #10px
            "color": "blue",
            "max-width": "autopx" #auto
        },
        multiple=True, ),
    html.H4(children="Data file list", style={"padding-left": "10px"}),
    html.Ul(id='file-list', style={"padding-left": "7px"})
],
    style={"width": "18rem"})]


card2_contents =[
    html.H4("Space Remaining",id='disk-space-remaining', className="card-title", style={"textAlign":"center",
                                                         "background-color":"#767ecf",
                                                         "color":"white",
                                                        "font-size":"10px",
                                                         "display":"inline-block"}),
    html.H2(str(card2_amount) + " GB", style={"textAlign":"center","padding-top":"10px"}),
    dbc.CardBody([


])
    ]
card3_contents=[
    html.H4("Disk Space Used", id='disk-space-used', className="card-title", style={"textAlign":"center",
                                                         "background-color":"#767ecf",
                                                         "color":"white",
                                                         "font-size":"10px",
                                                         "display":"inline-block"}),
    html.H2(str(card3_amount) + " GB", style={"textAlign":"center","padding-top":"10px"}),
    dbc.CardBody([


])
    ]
card4_contents=[
    html.H4("Chart Settings", className="card-title", style={"textAlign":"center",
                                                         "background-color":"#767ecf",
                                                         "font-size":"10px",
                                                         "color":"white",
                                                         "display":"inline-block"}),
    html.H6(children='Select a drive from the drop down', style={'textAlign':'center'}),
    dbc.CardBody([
        # dropdown component
        dcc.Dropdown(
            id='yaxis',
            options=[{'label': i, 'value': i} for i in df['FILESYSTEM'].unique()],
            style={'width': '125px','padding': '2px','height':'25px'}),
        html.Br(),
        dcc.RadioItems(
            id='sizing',
            options=[
                {'label': 'Kilobytes', 'value': 'kb'},
                {'label': 'Megabytes', 'value': 'mb'},
                {'label': 'Gigabytes', 'value': 'gb'},
                {'label': 'Terabytes', 'value': 'tb'}
            ],
            value='gb',
            labelStyle={'display': 'inline-block', 'padding': '5px'},
            style={'font-size': '10px'},
        ),
        html.H5(children="Range:"),
        html.H5(children='From: '+df['TIMESTAMP'].min(),style={'textAlign': 'center'}),
        html.H5(children='To: '+df['TIMESTAMP'].max(),style={'textAlign': 'center'}),
]),
    ]


card1 = dbc.Card(card1_contents, color="Primary",outline=True)
card2 = dbc.Card(card2_contents,color="Primary",outline=True)
card3 = dbc.Card(card3_contents,color="Primary",outline=True)
card4 = dbc.Card(card4_contents,color="Primary",outline=True)



app.layout = html.Div([
    dbc.NavbarSimple(children=[
        dbc.NavItem(dbc.NavLink("Disk Utilization Report", href="#"),style={"font-size":"16px","color":"white","padding-top":"10px"}),
        dbc.NavItem(dbc.NavLink("File System Report", href="#"),style={"font-size":"16px","color":"white","padding-top":"10px"}),
    ],
    brand="Xtivia Reporting Dash",
    brand_href="#",
    color="#767ecf",
    dark=True),
    html.Br(),

    html.Div(children=[card1],style={"padding":"5px", "width":"14%", "display":"inline-block","box-shadow":"5px 5px 5px grey"}),
    html.Div(children=[card4],style={"padding":"10px", "width":"14%", "display":"block","box-shadow":"5px 5px 5px grey"}),
    html.Div(children=[card2],style={"padding":"10px", "width":"14%", "display":"block","box-shadow":"5px 5px 5px grey","height":"5%"}),
    html.Div(children=[card3],style={"padding":"10px", "width":"14%", "display":"block","box-shadow":"5px 5px 5px grey"}),
    html.Div([
     dcc.Graph(
         id='scatter',
          figure={'data': [go.Scatter()],
                  'layout': go.Layout(
                     title='Please Pick a Disk from the dropdown',
                     xaxis={'title': 'TIMESTAMP'},
                     yaxis={'title': 'USED GB'}
                 )

                 }
  )
    ],
        style={'position':'relative','left':'300px','bottom':'700px','max-width':'75%'} #600px bottom
            )

    ])



########################## Controller ###########################################
### to parse data file regardless if it is xlsx, csv, or txt
def parse_data(content, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
        # Assume that the user uploaded a csv or text file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
        #assume that hte user uplaoded an excel file
            df=pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
        #assume that the user uploaded a txt file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimeter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div(["Error in processing this file"])
    return df


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

    
@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@app.callback(
    Output("file-list", "children"),
    #[Output("disk-space-used", card2_amount), 
    #Output("disk-space-remaining",card3_amount)],
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)


def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

@app.callback(
    Output('scatter','figure'),
    [Input('yaxis','value')])

def update_graphics(value):
    filtered_df = df[df['FILESYSTEM'] == value]
    max_disk_space = round(filtered_df.KBYTES.max()/(1024**2),2)
    card3_amount=round(filtered_df.USED)/1048576
    #card3_amount= round(df["USED"].iloc[0]/(1024**2),2)
    card2_amount=round(filtered_df.AVAIL)/1048576
    #card2_amount= round(df["AVAIL"].iloc[0]/(1024**2),2)
    report_title='Disk ' + str(value)+'<br>'+ 'MAX disk space: '+str(max_disk_space) +' GB ' + '<br>'+ 'Instance: '+ df['MAIL_ID'].iloc[0] 
    return {
    'data': [go.Scatter(
        x=filtered_df.TIMESTAMP,
        y=filtered_df.USED/1048576, #to convert into GB
        mode='lines',
        )],
            'layout': go.Layout(
                height=600,
                title=report_title,
                xaxis={'title':'TIMESTAMP'},
                #xaxis_tickformat = '%d %B (%a)%Y',
                yaxis={
                    'title':'USED GB',
                    'ticksuffix':' GB',
                    'tickmode':'auto',
                    'automargin':True,
                    'range':[0,(filtered_df.KBYTES.max())/(1024*1024)]
                    #'rangemode':'tozero'

                    }, 

                ), 

    }


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)
