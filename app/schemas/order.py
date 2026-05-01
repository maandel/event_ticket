from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class ContactInfoSchema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    countryCode: str


class CreateOrderRequest(BaseModel):
    eventId: str
    sectionId: str
    quantity: int
    totalAmount: float
    paymentMethod: str
    stripePaymentIntentId: str
    contactInfo: ContactInfoSchema

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        return v

    @field_validator("paymentMethod")
    @classmethod
    def validate_payment_method(cls, v: str) -> str:
        allowed = {"card", "apple_pay", "google_pay"}
        if v not in allowed:
            raise ValueError(f"paymentMethod must be one of {allowed}")
        return v


class OrderSectionSnapshot(BaseModel):
    id: str
    name: str
    row: str
    price: float
    currency: str


class OrderEventSnapshot(BaseModel):
    id: str
    title: str
    tournament: str
    stage: str
    date: str
    time: str
    venue: str
    city: str
    country: str
    image: str | None
    teams: list[dict]


class OrderOut(BaseModel):
    id: str
    userId: str | None
    event: dict
    section: dict
    quantity: int
    contactInfo: ContactInfoSchema
    totalAmount: float
    paymentMethod: str
    stripePaymentIntentId: str
    status: str
    createdAt: datetime

    @classmethod
    def from_orm_model(cls, order) -> "OrderOut":
        return cls(
            id=order.id,
            userId=order.user_id,
            event=order.event_snapshot,
            section=order.section_snapshot,
            quantity=order.quantity,
            contactInfo=ContactInfoSchema(**order.contact_info),
            totalAmount=order.total_amount,
            paymentMethod=order.payment_method,
            stripePaymentIntentId=order.stripe_payment_intent_id,
            status=order.status,
            createdAt=order.created_at,
        )


class OrderListParams(BaseModel):
    status: str | None = None
    eventId: str | None = None
    page: int = 1
    limit: int = 20

    @field_validator("page")
    @classmethod
    def page_positive(cls, v: int) -> int:
        return max(1, v)

    @field_validator("limit")
    @classmethod
    def limit_range(cls, v: int) -> int:
        return min(max(1, v), 100)
