import enum
from typing import Union

from pydantic import BaseModel, Field


class Point(BaseModel):
    lat: float
    lon: float


class Element(BaseModel):
    """Base element for OpenStreetMap Elements"""

    id: int


class NodeTags(BaseModel):
    """Tags associated with OpenStreetMap nodes"""

    # TODO: Check if default value `None` is required (if field exists without it)
    highway: Union[str, None]

    name: Union[str, None]
    amenity: Union[str, None]


class Node(Element):
    """An OpenStreetMap Node element"""

    class _Type(str, enum.Enum):
        NODE = "node"

    type: _Type

    lat: float
    lon: float

    tags: NodeTags


class WayTags(BaseModel):
    """Tags associated with OpenStreetMap ways"""

    # TODO: Check if default value `None` is required (if field exists without it)
    # TODO: Check if "all optional" exists for BaseModel
    highway: Union[str, None]
    surface: Union[str, None]

    bicycle: Union[str, None]
    bridge: Union[str, None]
    tunnel: Union[str, None]


class WayBounds(BaseModel):
    """Bounds of a ways"""

    minlat: float
    minlon: float
    maxlat: float
    maxlon: float


class Way(Element):
    """An OpenStreetMap Way element

    Remark: Overpass API uses the field name `nodes` to share the node IDs. `overpass`
    explicitly uses `node_ids` to differentiate clearly from a `Node` model.
    """

    class _Type(str, enum.Enum):
        WAY = "way"

    type: _Type

    node_ids: list[int] = Field(..., alias="nodes")
    geometry: list[Point]
    tags: WayTags


class Response(BaseModel):
    version: float
    elements: list[Union[Node, Way]]
