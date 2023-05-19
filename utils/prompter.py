"""
A dedicated helper to manage templates and prompt building.
"""

import json
import os.path as osp
import random
from typing import Union


class Prompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
        if not template_name:
            # Enforce the default here, so the constructor can be called with '' and will not break.
            template_name = "goat"
        file_name = osp.join("templates", f"{template_name}.json")
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )

    def generate_prompt_simplified(
        self,
        instruction: str,
        label: Union[None, str] = None,
    ) -> str:

        res = f"{instruction}"
        if label:
            res = f"{res}{label}"
        if self._verbose:
            print(res)
        return res
    
    
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
        return prompt

    def generate_prompt_inference(
        self,
        instruction: str,
        label: Union[None, str] = None,
    ) -> str:
        
        res = f"{instruction}\nAnswer: "
            
               
        if label:
            # res = f"{res}{instruction}{label}"
            res = f"{res}{label}"
        if self._verbose:
            print(res)
        return res

    def get_response(self, output: str) -> str:
        # return output.split("Answer:")[1].strip()
        return output