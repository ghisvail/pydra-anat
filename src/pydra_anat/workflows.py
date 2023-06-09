from pydra.engine.core import Result, Workflow
from pydra.engine.submitter import Submitter


def pydra_anat(**kwargs) -> Workflow:
    from pydra.tasks import fsl

    workflow = Workflow(input_spec=["input_image", "input_mask", "template_image"], **kwargs)

    workflow.add(
        fsl.FSLReorient2Std(
            name="reorient_image",
            input_image=workflow.lzin.input_image,
            output_matrix="orig2std.mat",
        )
    )

    workflow.add(
        fsl.RobustFOV(
            name="crop_image",
            input_image=workflow.reorient_image.lzout.output_image,
            output_matrix="roi2full.mat",
        )
    )

    workflow.add(
        fsl.InvertXFM(
            name="invert_roi2full",
            input_matrix=workflow.crop_image.lzout.output_matrix,
            output_matrix="full2roi.mat",
        )
    )

    workflow.add(
        fsl.ConcatXFM(
            name="concat_orig2roi",
            input_matrix=workflow.reorient_image.lzout.output_matrix,
            concat_matrix=workflow.invert_roi2full.lzout.output_matrix,
            output_matrix="orig2roi.mat",
        )
    )

    workflow.add(
        fsl.ApplyXFM(
            name="resample_mask_to_roi",
            input_image=workflow.lzin.input_mask,
            reference_image=workflow.crop_image.lzout.output_image,
            initial_matrix=workflow.concat_orig2roi.lzout.output_matrix,
            interpolation="nearestneighbour",
        )
    )

    workflow.add(
        fsl.FLIRT(
            name="register_image",
            input_image=workflow.crop_image.lzout.output_image,
            reference_image=workflow.lzin.template_image,
            # input_weights=workflow.resample_mask_to_roi.lzout.output_image,
            interpolation="spline",
            search_range_x=[-15, 15],
            search_range_y=[-15, 15],
            search_range_z=[-15, 15],
        )
    )

    workflow.add(
        fsl.ApplyXFM(
            name="resample_mask_to_tpl",
            input_image=workflow.resample_mask_to_roi.lzout.output_image,
            reference_image=workflow.lzin.template_image,
            initial_matrix=workflow.register_image.lzout.output_matrix,
            interpolation="nearestneighbour",
        )
    )

    workflow.set_output({
        "output_image": workflow.register_image.lzout.output_image,
        "output_mask": workflow.resample_mask_to_tpl.lzout.output_image,
    })

    return workflow


def run(workflow: Workflow, **kwargs) -> Result:
    with Submitter(**kwargs) as submitter:
        submitter(workflow)

    return workflow.result()
