from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_optional_user
from app.db.session import get_db
from app.schemas.common import ApiResponse
from app.schemas.order import CreateOrderRequest, OrderListParams
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", status_code=201, summary="Confirm order after payment")
async def create_order(
    payload: CreateOrderRequest,
    current_user=Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = OrderService(db)
    user_id = current_user.id if current_user else None
    order = await service.create_order(payload, user_id=user_id)
    return ApiResponse.ok(
        data={"order": order.model_dump()},
        message="Tickets booked successfully!",
    )


@router.get("", summary="Get my tickets")
async def get_my_orders(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    params = OrderListParams(status=status, page=page, limit=limit)
    service = OrderService(db)
    data = await service.get_user_orders(current_user.id, params)
    return ApiResponse.ok(data=data)


@router.get("/{order_id}", summary="Get single order")
async def get_order(
    order_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = OrderService(db)
    order = await service.get_order(order_id, current_user.id)
    return ApiResponse.ok(data={"order": order.model_dump()})
