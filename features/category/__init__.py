from fastapi import APIRouter

from features.category.create import acreate_category
from features.category.create.schema import CreateCategoryResponse
from features.category.list import aget_categories
from features.category.list.schema import BaseCategoryResponse
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
    response_model=PageResponse[BaseCategoryResponse],
    summary="Get all categories",
)
