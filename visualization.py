import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np


def generate_layer_visualizations(layer_outputs):
    fig = make_subplots(rows=len(layer_outputs), cols=1, subplot_titles=[layer['name'] for layer in layer_outputs])

    for i, layer in enumerate(layer_outputs, start=1):
        output = np.array(layer['output'])
        if len(output.shape) == 3:  # For 2D outputs (e.g., conv layers)
            heatmap = go.Heatmap(z=output[0])
            fig.add_trace(heatmap, row=i, col=1)
        elif len(output.shape) == 2:  # For 1D outputs (e.g., dense layers)
            bar = go.Bar(y=output[0])
            fig.add_trace(bar, row=i, col=1)
        elif len(output.shape) == 1:  # For scalar outputs
            bar = go.Bar(y=[output[0]])
            fig.add_trace(bar, row=i, col=1)

    fig.update_layout(height=300 * len(layer_outputs), title_text="Layer Visualizations")
    return fig


def generate_prediction_visualization(prediction):
    if len(prediction.shape) > 1 and prediction.shape[1] > 1:
        # Multi-class classification
        labels = [f"Class {i}" for i in range(prediction.shape[1])]
        fig = go.Figure(data=[go.Bar(x=labels, y=prediction[0])])
    else:
        # Binary classification
        fig = go.Figure(data=[go.Bar(x=['Negative', 'Positive'], y=[1 - prediction[0], prediction[0]])])

    fig.update_layout(title_text="Prediction Probabilities")
    return fig
