import torch
#from doctr.models import crnn_mobilenet_v3_small
from doctr.models import crnn_mobilenet_v3_large
from doctr.models.utils import export_model_to_onnx
from doctr.datasets import VOCABS

# 1. Rebuild the model with exportable=True
model = crnn_mobilenet_v3_large(pretrained=False, exportable=True, vocab=VOCABS['digits'])

# 2. Load your trained weights
state_dict = torch.load("/Users/adam.rivers/Documents/mastitisimager/data/ocr/saved_models/crnn_mobilenet_v3_large_20260112-153754.pt", map_location="cpu", weights_only=True)
model.load_state_dict(state_dict)
model.eval()

# 3. Prepare a dummy input with the same shape as training
batch_size = 1
input_shape = (3, 32, 128)  # (C, H, W)
dummy_input = torch.rand((batch_size, *input_shape), dtype=torch.float32)

# 4. Export to ONNX using docTR’s helper
model_path = export_model_to_onnx(
    model,
    model_name="crnn_mobilenet_v3_large_20260112-153754.onnx",
    dummy_input=dummy_input
)

print("Exported model saved at:", model_path)
