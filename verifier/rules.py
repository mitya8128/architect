def normalize_type(t: str):
    if not isinstance(t, str):
        return t
    return t.replace(" ", "")


def check_module_types(arch):

    errors = []

    normalized_types = {normalize_type(t) for t in arch.types}

    for module in arch.modules.values():

        input_type = normalize_type(module.input)
        output_type = normalize_type(module.output)

        if input_type not in normalized_types:
            errors.append(
                f"{module.name}: unknown input type {module.input}"
            )

        if output_type not in normalized_types:
            errors.append(
                f"{module.name}: unknown output type {module.output}"
            )

    return errors


def check_pipeline_consistency(arch):

    errors = []

    for pipeline in arch.pipelines.values():

        modules = pipeline.modules

        for i in range(len(modules) - 1):

            m1 = arch.modules[modules[i]]
            m2 = arch.modules[modules[i+1]]

            if normalize_type(m1.output) != normalize_type(m2.input):

                errors.append(
                    f"{pipeline.name}: {m1.name} -> {m2.name} type mismatch "
                    f"{m1.output} != {m2.input}"
                )

    return errors