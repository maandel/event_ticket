from pydantic import BaseModel


class CheckoutIntentRequest(BaseModel):
    eventId: str
    sectionId: str
    quantity: int
    currency: str = "usd"


class CheckoutIntentResponse(BaseModel):
    clientSecret: str
    amount: int       # in cents
    currency: str
