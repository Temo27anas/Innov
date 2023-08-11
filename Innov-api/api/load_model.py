import torch

def load_model(model_name: str):
    """
    Load model from path
    :param model_name: name of the model to load
    :return: model
    """
    
    model_path = "models/" + model_name + ".pth"
    model = torch.load(model_path, map_location=torch.device('cpu'))
    model.to('cpu')

    return model