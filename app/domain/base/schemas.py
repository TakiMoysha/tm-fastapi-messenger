from pydantic import BaseModel as _BaseModel


class BaseSchema(_BaseModel):
    model_config = {"from_attributes": True}
