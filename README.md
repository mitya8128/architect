# AI Architecture Compiler

**AI Architecture Compiler** is a prototype system for generating, verifying, and implementing software architectures using LLMs and formal methods.

Instead of directly generating code from prompts, the system introduces an intermediate **Architecture DSL**, enabling:

* Structural validation
* Type checking
* Iterative refinement
* Future formal verification



## 🧠 Core Idea

"Traditional" approach:

```
prompt → code
```

This project:

```
prompt → architecture (DSL) → verification → code
```

This enables **more reliable, interpretable, and verifiable software generation**.



## 📦 Project Structure

```
analyzer/
    code_metrics.py
    main_pipeline.py
    matching.py
    parser.py
    side_effects.py

architecture/
    loader.py
    model.py

llm/
    __init__.py
    base.py
    claude_client.py
    factory.py
    ollama_client.py
    openai_client.py

prompts/
    code_generation_prompts.py
    rebuild_arch_prompts.py

utils/
    yaml_utils.py

verifier/
    rules.py
    verifier.py

sessions/
    architecture.yaml
    generated_code.py
    
README.md
llm.py
main.py
requirements.txt
system.prompt
```



## ⚙️ Architecture DSL

Example:

```yaml
system:
  name: calendar_app

types:
  - Date
  - Event

modules:
  create_event:
    input: Event
    output: Event

  format_date:
    input: Date
    output: Date

pipelines:
  event_pipeline:
    - create_event
```



## ✅ Verification

The verifier ensures:

* All types are declared
* Module I/O types are consistent
* Pipelines are type-correct



## 🚀 Usage

### Run the system

```bash
python main.py  -h  

example with ollama:
python main.py \
  --provider ollama \
  --model deepseek-r1 \
  --prompt "calendar backend"
```

This will:

1. Generate architecture via LLM
2. Normalize YAML
3. Verify architecture
4. Repair if needed
5. Generate Python code



## 🔁 Iterative Repair Loop

The system automatically:

```
generate → verify → repair → repeat
```

until a valid architecture is produced.



## 🤖 LLM Integration

Currently supported:

* Ollama (local models)

Planned:

* OpenAI API
* Anthropic
* Multi-model pipelines



## 🧪 Code Verification (WIP)

The system includes an AST-based verifier:

* Extracts functions from generated code
* Checks consistency with architecture



## 📍 Roadmap

* [ ] CLI interface (argparse)
* [ ] logs of all erros during architecture generation step to feed into model  
* [ ] multi-model abstraction layer
* [ ] AST-level code verification
* [ ] architecture → tests (TDD loop)
* [ ] architecture critic (LLM-based)
* [ ] graph-based verification (networkx)
* [ ] constraint system (DSL-level rules)



## 🔬 Research Direction

This project explores:

* Architecture as IR (Intermediate Representation)
* AI-assisted software design
* Formal verification + LLMs
* Autonomous system design loops

  

## 🧩 Long-term Vision

```
prompt → architecture IR → verification → optimization → code
```

A full **compiler pipeline for software systems**.



## 👨‍💻 Author

Dmitriy Akhmediyev


## 📄 License  
TBD
