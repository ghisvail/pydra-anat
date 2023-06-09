from attrs import define, field
from pydra.engine.specs import SpecInfo
from pydra.tasks.fsl import fslmaths


class Binarize(fslmaths.FSLMaths):
    @define(kw_only=True)
    class BinarizeSpec(fslmaths.FSLMathsSpec):
        threshold: float = field(metadata={"help_string": "threshold value", "argstr": "-thr"})

        inverse: bool = field(
            default=False,
            metadata={
                "help_string": "invert binarization",
                "formatter": lambda inverse: "-binv" if inverse else "-bin",
            },
        )

    input_spec = SpecInfo(name="Inputs", bases=(BinarizeSpec,))


class Mask(fslmaths.FSLMaths):
    @define(kw_only=True)
    class MaskSpec(fslmaths.FSLMathsSpec):
        mask_image: bool = field(metadata={"help_string": "mask image", "mandatory": True, "argstr": "-mas"})

    input_spec = SpecInfo(name="Inputs", bases=(MaskSpec,))
