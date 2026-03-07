from .rules import (
    check_module_types,
    check_pipeline_consistency
)


def verify_architecture(arch):

    errors = []

    errors += check_module_types(arch)
    errors += check_pipeline_consistency(arch)

    return errors