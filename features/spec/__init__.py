from fastapi import APIRouter

from features.spec.create import acreate_spec
from features.spec.create.schema import CreateSpecResponse


router = APIRouter(prefix="/spec", tags=["Spec"])

router.add_api_route("/", acreate_spec, methods=["POST"], description="Tạo thông số kỹ thuật", response_model=CreateSpecResponse)