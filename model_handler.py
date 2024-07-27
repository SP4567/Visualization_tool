from tensorflow.keras.models import load_model as keras_load_model

def load_model(model_path):
    try:
        model = keras_load_model(model_path)
        return model
    except Exception as e:
        raise ValueError(f"Error loading model: {str(e)}")