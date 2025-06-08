from PIL import Image
import torch
import clip  # pip install git+https://github.com/openai/CLIP.git

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def encode_board_image(image: Image.Image) -> torch.Tensor:
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy()
