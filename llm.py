import os
import ollama
from prompts.code_generation_prompts import PYTHON_PROMPT


class LLMClient:

    def __init__(self, model="deepseek-r1:latest"):
        self.model = model
        self.PYTHON_PROMPT = PYTHON_PROMPT

    def generate(self, system_prompt, user_prompt):

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response["message"]["content"]
    
    def generate_code_from_architecture(self, yaml_file_path, py_file_path):
        """
        Generate Python code based on the architecture defined in a YAML file.
        Args:
            yaml_file_path (str): Path to the YAML file containing the architecture.
            
        Returns:
            str: Generated Python code.
            
        Raises:
            FileNotFoundError: If the YAML file does not exist.
            IOError: If the file cannot be read.
        """
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as file:
                architecture_yaml = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found: {yaml_file_path}")
        except Exception as e:
            raise IOError(f"Error reading YAML file: {e}")

        user_prompt = self.PYTHON_PROMPT.replace('{{architecture_yaml}}', architecture_yaml)
        code = self.generate("", user_prompt)

        with open(py_file_path, "w") as f:
            f.write(code)
        
        print(f'file written to {py_file_path}!')



def generate_architecture(llm, system_prompt, user_prompt, path):
    
    print('start generating!')
    output = llm.generate(system_prompt, user_prompt)
    
    with open(path, "w") as f:
        f.write(output)

    return path