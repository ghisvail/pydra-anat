from attrs import define, field
from pydra.engine.specs import SpecInfo
from pydra.tasks.fsl import fslmaths


@define(kw_only=True)
class BinarizeSpec(fslmaths.FSLMathsSpec):
    threshold: float = field(metadata={"help_string": "threshold value", "argstr": "-thr"})

    invert: bool = field(
        default=False,
        metadata={
            "help_string": "invert binarization",
            "formatter": lambda inverse: "-binv" if inverse else "-bin",
        },
    )


class Binarize(fslmaths.FSLMaths):
    input_spec = SpecInfo(name="Inputs", bases=(BinarizeSpec,))
