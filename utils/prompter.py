from typing import Union


class Prompter(object):
    
    def generate_prompt(
        self,
        instruction: str,
        label: Union[None, str] = None,
    ) -> str:     

        res = f"{instruction}\nAnswer: "
               
        if label:
            res = f"{res}{label}"
         
        return res


    def get_response(self, output: str) -> str:
        return output.split("Answer:")[1].strip().replace("/", "\u00F7").replace("*", "\u00D7")
        # return output