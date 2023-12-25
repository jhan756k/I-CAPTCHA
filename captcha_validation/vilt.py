from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import torch

image_path = r"C:\Users\Jooney Han\Desktop\KSEF2023\서류\dataset\heart638.png"  
image = Image.open(image_path)
text = "is there a heart?"

processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

encoding = processor(image, text, return_tensors="pt")

outputs = model(**encoding)
logits = outputs.logits

probs = torch.softmax(logits, dim=-1).squeeze()
top5_probs, top5_indices = torch.topk(probs, 5)

for idx, prob in zip(top5_indices, top5_probs):
    answer = model.config.id2label[idx.item()]
    confidence = prob.item()
    print(f"Answer: {answer}, Confidence: {confidence:.4f}")