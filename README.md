#  🐐 Goat: a Fine-tuned LLaMA that is Good at Arithmetic Tasks

<center> | [Paper](https://arxiv.org/abs/2305.14201) | [Adapter Weights](https://huggingface.co/tiedong/goat-lora-7b) | [Dataset](https://huggingface.co/datasets/tiedong/goat) | </center>


### Demo
1. Addition
<p float="left">
    <img src="imgs/gpt-4-add.png?raw=true" alt="Alt text" style="width: 49%;">
    <img src="imgs/add.png?raw=true" alt="Alt text" style="width: 49%;">
</p>
2. Subtraction
<div style="display: flex;">
    <img src="imgs/gpt-4-add.png?raw=true" alt="Alt text" style="width: 49%;">
    <img src="imgs/add.png?raw=true" alt="Alt text" style="width: 49%;">
</div>
3. Multiplication
<div style="display: flex;">
    <img src="imgs/gpt-4-add.png?raw=true" alt="Alt text" style="width: 50%;">
    <img src="imgs/add.png?raw=true" alt="Alt text" style="width: 50%;">
</div>
4. Division
<div style="display: flex;">
    <img src="imgs/gpt-4-add.png?raw=true" alt="Alt text" style="width: 50%;">
    <img src="imgs/add.png?raw=true" alt="Alt text" style="width: 50%;">
</div>



### Local Setup

   ```bash
   git clone https://github.com/liutiedong/goat.git 
   cd goat
   pip install -r requirements.txt
   ```

### Dataset (`dataset.ipynb`)
Run `dataset.ipynb` to generate `dataset.json` file, or download from HuggingFace dataset `tiedong/goat` (https://huggingface.co/datasets/tiedong/goat). Each instance in the dataset contains

- __instruction__: human instruction created by inserting an arithmetic expression to a randomly chosen template and adding some natural language noises. It serves as prompts to be fed to the model for instruction-finetuning.
- __input__: a randomly generated arithmetic expression. It can be used to replace 'instruction' for training when we want to focus on arithmetic and avoid the influence of natural language.
- __output__: the target output for the model to learn. It contains CoTs for multi-digit multiplication and division.
- __answer__: direct numerical answer to the arithmetic task. It can be used to test learnability of various sub-tasks.

Example:
```bash
{
    "instruction": "What is 94140209+73?",
    "input": "94140209 + 73",
    "output": "94140209 + 73 = 94140282",
    "answer": "94140282"
},
{
    "instruction": "Compute 8432862 - 659016175?",
    "input": "8432862 - 659016175",
    "output": "8432862 - 659016175 = -650583313",
    "answer": "-650583313"
},
{
    "instruction": "Calculate 37 times 3066",
    "input": "37 * 3066",
    "output": "37 * 3066 = 3066 * (30 + 7) = 3066 * 30 + 3066 * 7 = 91980 + 21462 = 113442",
    "answer": "113442"
},
{
    "instruction": "Determine the numerical value of 5697/47.",
    "input": "5697 / 47",
    "output": "5697 - 47 * 100 = 5697 - 4700 = 997\n997 - 47 * 20 = 997 - 940 = 57\n57 - 47 * 1 = 57 - 47 = 10\nTherefore, 5697 / 47 = 121 R 10",
    "answer": "121 R 10"
},

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


### Citation
```
@article{liu2023goat,
  title={Goat: Fine-tuned LLaMA Outperforms GPT-4 on Arithmetic Tasks},
  author={Liu, Tiedong and Low, Bryan Kian Hsiang},
  journal={arXiv preprint arXiv:2305.14201},
  year={2023}
}
```

### Acknowledgements
Our implementation is mainly based on [Alpaca-LoRA](https://github.com/tloen/alpaca-lora).