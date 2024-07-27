import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from model_handler import load_model
from text_processing import preprocess_text
from visualization import generate_3d_embedding_visualization
import base64
import os

def create_dash_app(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
    dash_app.layout = html.Div([
        dcc.Upload(id='upload-model', children=html.Button('Upload Model')),
        dcc.Upload(id='upload-text', children=html.Button('Upload Text')),
        html.Div(id='output-visualization'),
    ])

    @dash_app.callback(
        Output('output-visualization', 'children'),
        [Input('upload-model', 'contents'), Input('upload-text', 'contents')],
        [State('upload-model', 'filename'), State('upload-text', 'filename')]
    )
    def update_output(model_content, text_content, model_filename, text_filename):
        if model_content and text_content:
            try:
                # Decode base64 content
                model_content_type, model_base64 = model_content.split(',')
                text_content_type, text_base64 = text_content.split(',')

                # Save files
                model_path = f'models/{model_filename}'
                text_path = f'models/{text_filename}'

                with open(model_path, 'wb') as f:
                    f.write(base64.b64decode(model_base64))
                with open(text_path, 'wb') as f:
                    f.write(base64.b64decode(text_base64))

                # Load model and preprocess text
                model = load_model(model_path)
                processed_text = preprocess_text(open(text_path, 'r').read())

                # Generate visualization
                fig = generate_3d_embedding_visualization(model, processed_text)
                return dcc.Graph(figure=fig)

            except Exception as e:
                print(f"Error: {str(e)}")
                return html.Div([html.H5(f"Error: {str(e)}")])
        return html.Div([html.H5('Upload a model and text to visualize.')])

    return dash_app
