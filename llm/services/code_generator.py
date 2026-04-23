from llm.tasks.code_generation import build_code_prompt


class CodeGenerator:

    def __init__(self, llm):
        self.llm = llm

    def generate_from_architecture(self, arch_path: str, code_path: str):
        try:
            with open(arch_path, "r", encoding="utf-8") as f:
                architecture_yaml = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found: {arch_path}")
        except Exception as e:
            raise IOError(f"Error reading YAML file: {e}")

        prompt = build_code_prompt(architecture_yaml)

        code = self.llm.generate("", prompt)

        with open(code_path, "w") as f:
            f.write(code)

        print(f"Code written to {code_path}")

        return code