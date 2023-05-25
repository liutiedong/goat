#  🐐 Goat: a Fine-tuned LLaMA that is Good at Arithmetic Tasks

Our implementation is based on [Alpaca-LoRA](https://github.com/tloen/alpaca-lora).

Checkout our paper (https://arxiv.org/abs/2305.14201).

### Local Setup

   ```bash
   git clone https://github.com/liutiedong/goat.git 
   cd goat
   pip install -r requirements.txt
   ```

### Dataset (`dataset.ipynb`)
Run `dataset.ipynb` to generate dataset file. Each instance in the dataset contains

- __instruction__: human instruction in natural language created by inserting an arithmetic expression to the template. It serves as prompt to be fed to the model.
- __input__: a randomly generated arithmetic expression. It can be used to replace 'instruction' when we want to focus on arithmetic and avoid the influence of natural language.
- __output__: the target for the model to learn. It contains CoTs for multi-digit multiplication and division.
- __answer__: direct numerical answer to the arithmetic task. It can be used to test learnability of the sub-tasks.

Example:
```bash
{
    "instruction": "What is 94140209+73?",
    "input": "94140209 + 73",
    "output": "94140209 + 73 = 94140282",
    "answer": "94140282"
},
{
    "instruction": "Calculate 37 times 3066",
    "input": "37 * 3066",
    "output": "37 * 3066 = 3066 * (30 + 7) = 3066 * 30 + 3066 * 7 = 91980 + 21462 = 113442",
    "answer": "113442"
}
```
It is good to start with a simple sub-task, say 8-digit by 8-digit addition, which only takes less than 2 hours to achieve near-perfect accuracy (100000 training samples on A10 GPU). Modify `dataset.ipynb` to create your own data.

### Template (`goat.json`)
`template.txt` contains several hundred natural language instructions. Instructions that are more commonly used are duplicated more times to increase their chances of being sampled. Instructions that are generated using ChatGPT are listed behind without duplication. Note that some instructions may not be coherent or grammatical correct after inserting arithmetic expressions, but it should not be a problem if we do not train on input. 

To add more instructions for training, put new instructions in `template.txt` under `templates` folder. Then run `python convert_txt_to_json.py` to convert to `goat.json` file, which is used by `dataset.ipynb` to generate dataset for fine-tuning.




### Training (`finetune.py`)

Example usage:

```bash
python finetune.py \
    --base_model 'decapoda-research/llama-7b-hf' \
    --data_path 'dataset.json' \
    --output_dir './weights'
```

We train our model using the following command:

```bash
python finetune.py \
    --base_model 'decapoda-research/llama-7b-hf' \
    --data_path 'dataset.json' \
    --output_dir './weights' \
    --batch_size 128 \
    --micro_batch_size 16 \
    --num_epochs 1 \
    --learning_rate 1e-4 \
    --cutoff_len 512 \
    --val_set_size 0 \
    --lora_r 64 \
    --lora_alpha 64 \
    --lora_dropout 0.05 \
    --lora_target_modules '[q_proj,v_proj,k_proj,o_proj]' \
```

### Inference (`app.py`)

This file downloads LoRA weights from HuggingFace `tiedong/goat-lora-7b`, and runs a Gradio interface for inference.

Example usage:

```bash
python app.py \
    --base_model 'decapoda-research/llama-7b-hf' \
    --lora_weights 'tiedong/goat-lora-7b'
```


