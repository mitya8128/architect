from architecture.loader import load_architecture
from verifier.verifier import verify_architecture
from llm import LLMClient
from system_prompt import SYSTEM_PROMPT
from prompts.code_generation_prompts import PYTHON_PROMPT
from prompts.rebuild_arch_prompts import build_repair_prompt


ARCH_PATH = "sessions/architecture.yaml"
CODE_PATH = "sessions/generated_code.py"

MAX_ATTEMPTS = 6


def generate_architecture_loop(llm, user_prompt):

    prompt = user_prompt

    for attempt in range(MAX_ATTEMPTS):

        print(f"\n=== Architecture generation attempt {attempt+1} ===")

        response = llm.generate(SYSTEM_PROMPT, prompt)

        with open(ARCH_PATH, "w") as f:
            f.write(response)

        try:
            arch = load_architecture(ARCH_PATH)
        except Exception as e:
            print("YAML parsing error:", e)
            prompt = build_repair_prompt(prompt, [str(e)])
            continue

        errors = verify_architecture(arch)

        if not errors:
            print("Architecture verified successfully")
            return arch

        print("Verification errors:")
        for e in errors:
            print("-", e)

        prompt = build_repair_prompt(prompt, errors)

    raise RuntimeError("Failed to generate valid architecture")


def generate_code(llm):

    with open(ARCH_PATH) as f:
        arch_text = f.read()

    prompt = PYTHON_PROMPT.format(architecture=arch_text)

    code = llm.generate("", prompt)

    with open(CODE_PATH, "w") as f:
        f.write(code)

    print("Code generated:", CODE_PATH)


def main():

    llm = LLMClient()

    USER_PROMPT = """
Design a simple calendar web application backend.
Users should be able to create events and view a calendar.
"""

    arch = generate_architecture_loop(llm, USER_PROMPT)

    llm.generate_code_from_architecture(ARCH_PATH, CODE_PATH)


if __name__ == "__main__":
    main()