from llm.services.repository_generator import RepositoryGenerator
from analyzer.repo_pipeline import analyze_repository_generation
from verifier.module_verifier import verify_module
from analyzer.semantic_summary import extract_semantic_summary
from prompts.module_repair_prompt import build_module_repair_prompt
from utils.code_utils import extract_code


def generate_and_refine_repository(llm,semantic_model, 
                                   output_dir,max_iters=3):

    generator = RepositoryGenerator(llm)
    state = generator.generate_repository(semantic_model, output_dir)

    for iteration in range(max_iters):
        print(
            f"\\n=== Repository refinement iteration {iteration+1} ==="
        )
        errors_found = False

        for module_name, module_path in (
            state.generated_modules.items()
        ):
            print(f"\\nChecking module: {module_name}")

            with open(module_path) as f:
                code = f.read()

            summary = extract_semantic_summary(code)
            node = semantic_model.nodes[module_name]

            errors = verify_module(node, summary)

            if not errors:
                continue

            errors_found = True

            print("Errors:")

            for e in errors:
                print("-", e)

            repair_prompt = build_module_repair_prompt( code, errors)

            raw_output = llm.generate( "", repair_prompt)

            repaired_code = extract_code(raw_output)

            with open(module_path, "w") as f:
                f.write(repaired_code)

        if not errors_found:
            print("\\n✅ Repository passed verification")

            return state

    print("\\n⚠️ Max repository refinement iterations reached")

    return state