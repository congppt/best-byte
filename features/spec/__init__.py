from fastapi import APIRouter

from features.spec.create.schema import CreateSpecResponse
from features.spec.create import acreate_spec
from features.spec.read import aget_specs
from features.spec.read.schema import SpecResponse
from utils.schema import PageResponse


router = APIRouter(prefix="/spec", tags=["Spec"])
router.add_api_route(
    "", acreate_spec, methods=["POST"], summary="Create category's new spec", response_model=CreateSpecResponse
)
router.add_api_route(
    "", aget_specs, methods=["GET"], summary="Get category's specs", response_model=PageResponse[SpecResponse]
)
