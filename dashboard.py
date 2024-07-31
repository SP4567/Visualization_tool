import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from model_handler import load_model, predict, get_layer_outputs
from text_processing import preprocess_text
from visualization import generate_layer_visualizations, generate_prediction_visualization
from log_config import logger
import os
from flask import session


def create_dash_app(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

    dash_app.layout = html.Div([
        html.H1("Model Visualization"),
        html.Div(id='debug-info'),
        dcc.Graph(id='layer-visualizations'),
        dcc.Graph(id='prediction-visualization'),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
    ])

    @dash_app.callback(
        [Output('layer-visualizations', 'figure'),
         Output('prediction-visualization', 'figure'),
         Output('debug-info', 'children')],
        [Input('interval-component', 'n_intervals')],
        [State('layer-visualizations', 'figure'),
         State('prediction-visualization', 'figure')]
    )
    def update_visualizations(n, layer_fig, pred_fig):
        logger.info(f"Callback triggered. Session: {session}")
        debug_info = f"Session contents: {session}"

        if 'MODEL_PATH' not in session or 'TEXT_CONTENT' not in session:
            logger.warning("MODEL_PATH or TEXT_CONTENT not in session")
            return dash.no_update, dash.no_update, debug_info

        try:
            model_path = session['MODEL_PATH']
            text_content = session['TEXT_CONTENT']

            logger.info(f"Loading model from {model_path}")
            model = load_model(model_path)

            logger.info(f"Preprocessing text: {text_content[:50]}...")
            text = preprocess_text(text_content)

            logger.info("Getting layer outputs")
            layer_outputs = get_layer_outputs(model, text)

            logger.info("Making prediction")
            prediction = predict(model, text)

            logger.info("Generating visualizations")
            layer_fig = generate_layer_visualizations(layer_outputs)
            pred_fig = generate_prediction_visualization(prediction)

            debug_info += f"\nVisualization generated successfully"
            return layer_fig, pred_fig, debug_info
        except Exception as e:
            logger.error(f"Error updating visualizations: {str(e)}", exc_info=True)
            debug_info += f"\nError: {str(e)}"
            return dash.no_update, dash.no_update, debug_info

    return dash_app
