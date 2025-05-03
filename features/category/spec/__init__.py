from fastapi import APIRouter

from features.category.spec.create import acreate_spec


router = APIRouter(prefix="/{category_id}/spec", tags=["Spec"])
router.add_api_route(
    "", acreate_spec, methods=["POST"], summary="Create category's new spec"
)
