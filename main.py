import argparse

from analyzer.main_pipeline import analyze_code
from architecture.loader import load_architecture
from verifier.verifier import verify_architecture
from llm.factory import get_llm
from llm.services.code_generator import CodeGenerator
from system_prompt import SYSTEM_PROMPT
from prompts.rebuild_arch_prompts import build_repair_prompt
from prompts.rebuild_code_generation_prompts import build_code_repair_prompt
from utils.yaml_utils import extract_yaml, normalize_yaml


DEFAULT_ARCH_PATH = "sessions/architecture.yaml"
DEFAULT_CODE_PATH = "sessions/generated_code.py"


def safe_normalize_yaml(text: str) -> str:
    try:
        return normalize_yaml(text)
    except Exception:
        return text


def analyze_generated_code(arch_path, code_path):

    print("\n=== Running Code Analyzer ===")

    try:
        with open(code_path) as f:
            code = f.read()

        arch = None
        if arch_path is not None:
            try:
                arch = load_architecture(arch_path)
            except Exception:
                print("⚠️ Failed to load architecture, continuing without it")

        result = analyze_code(code, arch)

        print("\n=== ANALYSIS RESULT ===")
        print("Score:", result.get("score"))

        print("\nErrors:")
        for e in result.get("errors", []):
            print("-", e)

        print("\nWarnings:")
        for w in result.get("warnings", []):
            print("-", w)

        print("\nMetrics:")
        for k, v in result.get("metrics", {}).items():
            print(f"{k}: {v}")

    except Exception as e:
        print("Analyzer failed:", e)
    
    return result


def generate_and_refine_code(llm, arch_path, code_path, max_iters=3):

    generator = CodeGenerator(llm)

    # initial generation
    generator.generate_from_architecture(arch_path, code_path)

    for i in range(max_iters):

        print(f"\n=== Code analysis iteration {i+1} ===")

        result = analyze_generated_code(arch_path, code_path)

        errors = result.get("errors", [])
        warnings = result.get("warnings", [])

        if not errors:
            print("✅ Code passed analysis")
            return

        print(f"❌ Found {len(errors)} errors, regenerating...")

        with open(code_path) as f:
            code = f.read()

        repair_prompt = build_code_repair_prompt(code, errors, warnings)

        new_code = llm.generate("", repair_prompt)

        with open(code_path, "w") as f:
            f.write(new_code)

    print("⚠️ Max refinement iterations reached")


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

    parser.add_argument("--prompt", type=str)
    parser.add_argument("--model", type=str, default="gemma3:latest")
    parser.add_argument("--provider", type=str, default="ollama")

    parser.add_argument("--arch", type=str, default=DEFAULT_ARCH_PATH)
    parser.add_argument("--code", type=str, default=DEFAULT_CODE_PATH)

    parser.add_argument("--no-code", action="store_true")
    parser.add_argument("--no-analyze", action="store_true")

    parser.add_argument("--from-arch", action="store_true",
                        help="Skip architecture generation, use existing YAML")

    parser.add_argument("--analyze-only", action="store_true",
                        help="Analyze only code (no architecture required)")

    parser.add_argument("--max-attempts", type=int, default=6)

    args = parser.parse_args()

    llm = get_llm(args.provider, args.model)

    arch = None

    # === MODE 3: analyze only code ===
    if args.analyze_only:
        analyze_generated_code(None, args.code)
        return

    # === MODE 2: use existing architecture ===
    if args.from_arch:
        arch = load_architecture(args.arch)

    # === MODE 1: generate architecture ===
    else:
        if not args.prompt:
            raise ValueError("Prompt is required unless --from-arch or --analyze-only is used")

        arch = generate_architecture_loop(
            llm,
            args.prompt,
            args.arch,
            args.max_attempts
        )

    # === code generation ===
    if not args.no_code:
        generate_and_refine_code(llm, args.arch, args.code,max_iters=3)
    
    # === analysis ===
    elif not args.no_analyze:
        analyze_generated_code(args.arch, args.code)


if __name__ == "__main__":
    main()