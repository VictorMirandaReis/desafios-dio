from pydantic import AwareDatetime, BaseModel, PositiveFloat


class AccountIn(BaseModel):
    user_id: int
    balance: PositiveFloat


class AccountUpdateIn(BaseModel):
    user_id: int | None = None
    balance: PositiveFloat | None = None
    created_at: AwareDatetime | None = None
    activated: bool | None = None
