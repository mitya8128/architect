from architecture.loader import load_architecture
from verifier.verifier import verify_architecture

arch = load_architecture("architecture.yaml")

errors = verify_architecture(arch)

if errors:
    print("Verification failed")
    for e in errors:
        print(e)
else:
    print("Architecture is valid")