from fastapi import APIRouter

from features.category.create import acreate_category
from features.category.create.schema import CreateCategoryResponse


router = APIRouter(prefix="/category", tags=["Category"])

router.add_api_route("/", acreate_category, methods=["POST"], description="Tạo danh mục", response_model=CreateCategoryResponse)
