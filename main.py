from architecture.loader import load_architecture
from verifier.verifier import verify_architecture
from llm import LLMClient, generate_architecture
from system_prompt import SYSTEM_PROMPT
from prompts.code_generation_prompts import PYTHON_PROMPT


llm = LLMClient()

USER_PROMPT = ''

# generate_architecture(SYSTEM_PROMPT, USER_PROMPT, 'session/architecture.yaml')
arch = load_architecture("sessions/architecture.yaml")

errors = verify_architecture(arch)

if errors:
    print("Verification failed")
    for e in errors:
        print(e)
else:
    print("Architecture is valid")
    llm.generate_code_from_architecture("sessions/architecture.yaml", 
                                        "sessions/generated_code.py")