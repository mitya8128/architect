import argparse

from architecture.loader import load_architecture
from verifier.verifier import verify_architecture
from llm.factory import get_llm
from llm.services.code_generator import CodeGenerator
from system_prompt import SYSTEM_PROMPT
from prompts.rebuild_arch_prompts import build_repair_prompt
from utils.yaml_utils import extract_yaml, normalize_yaml


DEFAULT_ARCH_PATH = "sessions/architecture.yaml"
DEFAULT_CODE_PATH = "sessions/generated_code.py"


def safe_normalize_yaml(text: str) -> str:
    try:
        return normalize_yaml(text)
    except Exception:
        return text


def generate_architecture_loop(llm, user_prompt, arch_path, max_attempts):

    prompt = user_prompt

    best_arch = None
    best_errors = None
    best_yaml_text = None

    for attempt in range(max_attempts):

        print(f"\n=== Architecture generation attempt {attempt+1} ===")

        response = llm.generate(SYSTEM_PROMPT, prompt)

        yaml_text = extract_yaml(response)
        yaml_text = safe_normalize_yaml(yaml_text)

        with open(arch_path, "w") as f:
            f.write(yaml_text)

        try:
            arch = load_architecture(arch_path)
        except Exception as e:
            print("YAML parsing error:", e)
            prompt = build_repair_prompt(prompt, [str(e)])
            continue

        errors = verify_architecture(arch)

        if best_errors is None or len(errors) < len(best_errors):
            best_arch = arch
            best_errors = errors
            best_yaml_text = yaml_text

        if not errors:
            print("Architecture verified successfully")
            return arch

        print("Verification errors:")
        for e in errors:
            print("-", e)

        prompt = build_repair_prompt(prompt, errors)

    print("\n⚠️ Max attempts reached")

    if best_arch is not None:
        print(f"Using best candidate with {len(best_errors)} errors")

        with open(arch_path, "w") as f:
            f.write(best_yaml_text)

        return best_arch

    raise RuntimeError("Failed to generate any architecture")


def main():

    parser = argparse.ArgumentParser(
        description="AI Architecture Compiler CLI"
    )

    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--model", type=str, default="gemma3:latest")
    parser.add_argument("--provider", type=str, default="ollama")

    parser.add_argument("--arch", type=str, default=DEFAULT_ARCH_PATH)
    parser.add_argument("--code", type=str, default=DEFAULT_CODE_PATH)

    parser.add_argument("--no-code", action="store_true")

    parser.add_argument("--max-attempts", type=int, default=6)

    args = parser.parse_args()

    llm = get_llm(args.provider, args.model)

    arch = generate_architecture_loop(
        llm,
        args.prompt,
        args.arch,
        args.max_attempts
    )

    if not args.no_code:
        generator = CodeGenerator(llm)
        generator.generate_from_architecture(args.arch, args.code)


if __name__ == "__main__":
    main()