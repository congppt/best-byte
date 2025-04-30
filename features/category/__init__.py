from fastapi import APIRouter

from features.category.create import acreate_category, acreate_spec
from features.category.read import aget_categories, aget_category_children
from features.category.read.schema import CategoryResponse
from utils.schema import PageResponse


router = APIRouter(prefix="/category", tags=["Category"])

router.add_api_route(
    "",
    acreate_category,
    methods=["POST"],
    summary="Create new category"
)
router.add_api_route(
    "",
    aget_categories,
    methods=["GET"],
    response_model=PageResponse[CategoryResponse],
    summary="Get all categories",
)

router.add_api_route(
    "/{id}",
    aget_category_children,
    methods=["GET"],
    response_model=PageResponse[CategoryResponse],
    summary="Get category detail",
)

spec_router = APIRouter(prefix="/{category_id}/spec", tags=["Spec"])

spec_router.add_api_route(
    "",
    acreate_spec,
    methods=["POST"],
    summary="Create category's new spec"
)
router.include_router(spec_router)
