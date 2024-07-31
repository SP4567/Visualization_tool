import tensorflow as tf
from tensorflow.keras.models import load_model as keras_load_model
import numpy as np
from log_config import logger

def load_model(model_path):
    try:
        model = keras_load_model(model_path)
        logger.info(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise ValueError(f"Error loading model: {str(e)}")

def predict(model, text):
    try:
        prediction = model.predict(np.array([text]))
        logger.info(f"Prediction made successfully: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise ValueError(f"Error making prediction: {str(e)}")

def get_layer_outputs(model, text):
    try:
        layer_outputs = [layer.output for layer in model.layers[1:]]  # Exclude input layer
        activation_model = tf.keras.models.Model(inputs=model.input, outputs=layer_outputs)

        activations = activation_model.predict(np.array([text]))

        layer_visualizations = []
        for layer_name, layer_activation in zip(model.layers[1:], activations):
            layer_visualizations.append({
                'name': layer_name.name,
                'output': layer_activation.tolist()  # Convert to list for JSON serialization
            })

        logger.info("Layer visualizations generated successfully")
        return layer_visualizations
    except Exception as e:
        logger.error(f"Error generating layer visualizations: {str(e)}")
        raise ValueError(f"Error generating layer visualizations: {str(e)}")
