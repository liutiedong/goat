import os
import sys
import json
import pandas as pd

import fire
import gradio as gr
import torch
import transformers
from peft import PeftModel
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer

from utils.prompter import Prompter

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

try:
    if torch.backends.mps.is_available():
        device = "mps"
except:  # noqa: E722
    pass


def main(
    load_8bit: bool = True,
    base_model: str = "",
    lora_weights: str = "train_ablation_200000",
    prompt_template: str = "goat",  # The prompt template to use, will default to alpaca.
    server_name: str = "0.0.0.0",  # Allows to listen on all interfaces by providing '0.
    share_gradio: bool = True,
):
    base_model = base_model or os.environ.get("BASE_MODEL", "")
    assert (
        base_model
    ), "Please specify a --base_model, e.g. --base_model='decapoda-research/llama-7b-hf'"

    prompter = Prompter(prompt_template)
    tokenizer = LlamaTokenizer.from_pretrained('hf-internal-testing/llama-tokenizer')
    if device == "cuda":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            torch_dtype=torch.float16,
            device_map={'': 0},
        )
    elif device == "mps":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
    else:
        model = LlamaForCausalLM.from_pretrained(
            base_model, device_map={"": device}, low_cpu_mem_usage=True
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
        )

    # unwind broken decapoda-research config
    # model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
    # model.config.bos_token_id = 1
    # model.config.eos_token_id = 2
    
    # tokenizer.bos_token_id = 1
    # tokenizer.eos_token_id = 2

    if not load_8bit:
        model.half()  # seems to fix bugs for some users.

    model.eval()
    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)

    def evaluate(
        instruction,
        temperature=0.9,
        top_p=0.75,
        top_k=40,
        num_beams=4,
        max_new_tokens=320,
        **kwargs,
    ):
        prompt = prompter.generate_prompt_simplified(instruction)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            **kwargs,
        )
        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences[0]
        # print(s)
        output = tokenizer.decode(s, skip_special_tokens=True).strip()
        return output
    
    
    
    with open("train_ablation_200000.json","rb") as test_file:
        test_data = json.load(test_file)
        
    output_dict = {}
    index = 0
    correct = 0
    accuracy = 1
    with open("output_train_ablation_200000.jsonl",'a') as output_file:
        for obj in test_data:
            index += 1
            if index>0:
                # print(str(index))#,": ",obj['instruction']
                output_dict["instruction"] = obj['instruction']           
                output_dict["result"] = evaluate(obj['instruction'])
                print(output_dict["result"])
                # print("",obj['instruction'],obj['cot'])
                print(obj['instruction'] + obj['output'])
                # print(obj['instruction'] + obj['cot'])
                # output_dict["cot"] = obj['cot']    
                output_dict["output"] = obj['output']
                if output_dict["result"].split()[-1] == obj['output'].split()[-1]:
                    correct = correct + 1
                else: 
                    print("Wrong!!!")
                accuracy = correct/index
                    
                print("------", correct, index, accuracy,"------")
                json_string = json.dumps(output_dict)
                output_file.write(json_string+'\n')



if __name__ == "__main__":
    fire.Fire(main)
