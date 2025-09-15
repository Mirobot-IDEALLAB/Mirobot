import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# 구체적인 에러 메세지를 위해 활성화
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'

model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

# 4bit 양자화 설정
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,    # 더 안정적인 양자화
    bnb_4bit_quant_type="nf4",         # 추천: nf4 또는 fp4
    bnb_4bit_compute_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config,
)

def chat(prompt, max_new_tokens=256):
    inputs = tokenizer(
        prompt,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
        ).to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_p=0.9
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print(torch.version.cuda)
print(torch.__version__)
print(torch.cuda.is_available())
print("-----------------")

prompt = input()
print(chat(prompt))

