from datasets import load_dataset
from transformers import LlamaTokenizer, AutoTokenizer
from typing import Union

# # tokenizer = LlamaTokenizer.from_pretrained(
# #     "decapoda-research/llama-7b-hf", add_eos_token=True
# # )

# tokenizer = AutoTokenizer.from_pretrained('databricks/dolly-v2-7b',add_eos_token=True)

# tokenizer.pad_token = tokenizer.eos_token
# tokenizer.pad_token_id = tokenizer.eos_token_id

# data = load_dataset("json", data_files="test_sub_8digit_1000.json")


# def generate_prompt(data_point):
#     # sorry about the formatting disaster gotta move fast
#     return f"""{data_point["instruction"]}{data_point["output"]}"""




# data = data.map(
#     lambda data_point: {"prompt": tokenizer(generate_prompt(data_point))}
# )

# import matplotlib.pyplot as plt

# lens = [len(x["prompt"]["input_ids"]) for x in data["train"]]
# print(max(lens))
# plt.hist(lens, bins=100)
# plt.title("Distribution of prompt lengths")
# plt.axvline(256, color="red")

# plt.savefig('length.png')from datasets import load_dataset
from transformers import LlamaTokenizer, AutoTokenizer
import os.path as osp
import json
import random
import matplotlib.pyplot as plt

# tokenizer = LlamaTokenizer.from_pretrained(
#     "decapoda-research/llama-7b-hf", add_eos_token=True
# )

tokenizer = LlamaTokenizer.from_pretrained('hf-internal-testing/llama-tokenizer')

tokenizer.pad_token = tokenizer.eos_token
tokenizer.pad_token_id = tokenizer.eos_token_id

data = load_dataset("json", data_files="test_final_0519.json")


# def generate_prompt(data_point):
#     # sorry about the formatting disaster gotta move fast
#     return f"""{data_point["instruction"]}{data_point["cot"]}"""



template_name = "goat"
file_name = osp.join("templates", f"{template_name}.json")
if not osp.exists(file_name):
    raise ValueError(f"Can't read {file_name}")
with open(file_name) as fp:
    template = json.load(fp)
    
def generate_prompt_q(data_point) -> str:
    # returns the full prompt from instruction and optional input
    # if a label (=response, =output) is provided, it's also appended.

    num = random.randint(1,300)

    res = template[str(num)].format(
        instruction=data_point["instruction"]
    )
    # print(res + data_point["cot"])
    return res + data_point["cot"]

def generate_prompt(
    self,
    instruction: str,
    label: Union[None, str] = None,
) -> str:

    if random.random()<0.5:
        instruction = instruction.replace("*", "x")
    
    if random.random()<0.1:
        instruction=instruction.replace("+", "plus").replace("-", "minus").replace("x", "times").replace("*", "multiplied by").replace("/", "divided by")    

    num = random.randint(1,500)
    if random.random()<0.6:
        res = self.template[str(num)].format(
            arithmetic=instruction.replace(" = ", "")
        )
    else:
        res = self.template[str(num)].format(
            arithmetic=instruction.replace("=", "").replace(" ", "")
        )


    prompt = f"{res}\nAnswer: "
        
           
    if label:
        # res = f"{res}{instruction}{label}"
        prompt = f"{prompt}{label}"
    
    if self._verbose:
        print(prompt)
    print(prompt)
    return prompt

data = data.map(
    lambda data_point: {"prompt": tokenizer(generate_prompt(data_point))}
)



lens = [len(x["prompt"]["input_ids"]) for x in data["train"]]
print(max(lens))
plt.hist(lens, bins=100)
plt.title("Distribution of prompt lengths")
plt.axvline(256, color="red")

plt.savefig('length.png')
