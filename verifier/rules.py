def check_module_types(arch):

    errors = []

    for module in arch.modules.values():

        if module.input not in arch.types:
            errors.append(
                f"{module.name}: unknown input type {module.input}"
            )

        if module.output not in arch.types:
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

            if m1.output != m2.input:

                errors.append(
                    f"{pipeline.name}: {m1.name} -> {m2.name} type mismatch "
                    f"{m1.output} != {m2.input}"
                )

    return errors