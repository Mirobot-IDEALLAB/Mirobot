import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

# 4bit 양자화 설정 (메모리 절약)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",          # GPU 자동 할당
    quantization_config=bnb_config
)


    # user_cmd = input()
system_prompt = (
"You are a Python code generator for controlling the WLKATA Mirobot.\n"
"Always respond with ONLY valid Python code.\n"
"Do NOT include explanations, markdown, triple backticks, or text.\n"
"Always define a single function named `policy()`.\n"
"The output must start with 'def policy():' and contain nothing else."
)

prompt = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "왼쪽으로 5만큼 갔다가 다시 원위치"}
]

# if user_cmd == "exit":
#     print("bye!")
#     break

inputs = tokenizer.apply_chat_template(prompt, return_tensors="pt", add_generation_prompt=True).to(model.device)
# outputs = model.generate(inputs, max_new_tokens=200)
# generate
outputs = model.generate(
    inputs,
    max_new_tokens=200,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
    do_sample=False
)
generated = tokenizer.decode(outputs[0], skip_special_tokens=True)

# code 블럭만 추출
matches = re.findall(r"'''python(.*?)'''", generated, re.DOTALL)
if matches:
    code_only = matches[0].strip()
else:
    print("fail!!!!!!!!!!!!!!!!!!1")
    code_only = generated.strip()
print(code_only)