from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    description: str
    category: str
    priority: str


class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    description: str
    category: str
    priority: str


class StatusUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: str


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: str
    priority: str
    status: str
    created_by: str
    creator_id: int
    created_at: str
    updated_at: str
