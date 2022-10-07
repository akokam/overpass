from pydantic import BaseModel


class Element(BaseModel):
    id: int
    type: str  # TODO: use Enum
    nodes: list[int]


class Response(BaseModel):
    version: float
    elements: list[Element]
