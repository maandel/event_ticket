from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.checkout import CheckoutIntentRequest
from app.schemas.common import ApiResponse
from app.services.checkout_service import CheckoutService

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("/intent", summary="Create Stripe Payment Intent")
async def create_payment_intent(
    payload: CheckoutIntentRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = CheckoutService(db)
    data = await service.create_payment_intent(payload)
    return ApiResponse.ok(data=data.model_dump())
