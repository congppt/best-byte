from fastapi import APIRouter

from features.category.create import acreate_category, acreate_spec
from features.category.create.schema import CreateCategoryResponse, CreateSpecResponse
from features.category.read import aget_categories, aget_category_children
from features.category.read.schema import CategoryResponse
from utils.schema import PageResponse


router = APIRouter(prefix="/category", tags=["Category"])

router.add_api_route(
    "/",
    acreate_category,
    methods=["POST"],
    summary="Create new category",
    response_model=CreateCategoryResponse,
)
router.add_api_route(
    "/",
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


router.add_api_route(
    "/{category_id}/spec",
    acreate_spec,
    methods=["POST"],
    summary="Create category's new spec",
    response_model=CreateSpecResponse,
)
