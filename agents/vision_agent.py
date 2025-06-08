from vision.vision_models import encode_board_image
from PIL import Image
import numpy as np
from transformers import CLIPProcessor, CLIPModel

# def vision_agent_process_board(image: Image.Image) -> np.ndarray:
#     """Encodes the board image into a feature vector."""
#     embedding = encode_board_image(image)
#     return embedding

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def vision_agent_process_board(image: Image.Image) -> np.ndarray:
    inputs = clip_processor(images=image, return_tensors="pt")
    outputs = clip_model.get_image_features(**inputs)
    return outputs[0].detach().numpy()
