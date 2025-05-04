from fastapi import APIRouter

from features.spec.create.schema import CreateSpecResponse
from features.spec.create import acreate_spec
from features.spec.read import aget_specs, aget_spec_comparisons
from features.spec.read.schema import SpecComparisonResponse, SpecResponse
from features.spec.update import aupdate_comparisons
from utils.schema import PageResponse


router = APIRouter(prefix="/spec", tags=["Spec"])
router.add_api_route(
    "",
    acreate_spec,
    methods=["POST"],
    summary="Create category's new spec",
    response_model=CreateSpecResponse,
)
router.add_api_route(
    "",
    aget_specs,
    methods=["GET"],
    summary="Get category's specs",
    response_model=PageResponse[SpecResponse],
)
router.add_api_route(
    "/{id}/comparisons",
    aupdate_comparisons,
    methods=["PUT"],
    summary="Update category's specs comparisons",
)
router.add_api_route(
    "/{id}/comparisons",
    aget_spec_comparisons,
    methods=["GET"],
    summary="Get spec's comparisons",
    response_model=list[SpecComparisonResponse],
)
