import httpx
from pydantic import BaseModel, HttpUrl, ValidationError

from overpass.models import Response


class OverpassError(Exception):
    """Base error for overpass"""


class RequestError(OverpassError):
    """Base error for overpass requests"""


class LocalConnectionError(OverpassError):
    """Raised when the connection to overpass server failed"""


class ServerError(RequestError):
    """Raised when an overpass request failed on server side"""


class ClientError(RequestError):
    """Raised when an overpass request failed on client side"""


class ParsingError(RequestError):
    """Raised when an overpass response was not parsable"""


class Config(BaseModel):
    """Configuration for overpass

    All environment variables shall be prefixed with `OVERPASS_`, e.g.:
      - OVERPASS_BASE_URL=localhost:"""

    class Config:
        env_prefix = "OVERPASS_"

    base_url: HttpUrl = "https://lz4.overpass-api.de"
    port: int = 80
    timeout: int = 60


class Client:
    def __init__(self, cfg: Config = None):
        """Self-initializing if no specific config is provided

        TODO: Add details that it connects to 'standard instance'
        """

        client_cfg = cfg or Config()
        self._overpass = httpx.Client(base_url=client_cfg.base_url)

    def query(self, query: str) -> Response:
        """Query the OpenStreetMap database with Overpass QL"""

        # TODO: Add sanity checks for query

        return self._post(query)

    def _post(self, payload: str) -> Response:
        """Perform a POST request to the interpreter

        TODO: Investigate if both (Overpass QL and XML) requests can be sent
        """

        try:
            response = self._overpass.post(url="/api/interpreter", data=payload)
        except (TimeoutError, ConnectionError) as e:
            # TODO: Check if httpx.RequestError works too
            raise LocalConnectionError(e)

        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            # TODO: Raise specific error
            # TODO: Differentiate between client and server error
            raise Exception(e)

        try:
            return Response(**response.json())
        except ValidationError as e:
            raise ParsingError(e)
