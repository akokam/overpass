import httpx
from pydantic import BaseModel, HttpUrl, ValidationError

from overpass.models import Response


class Config(BaseModel):
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

    def _post(self, payload: str) -> Response:
        """Perform a POST request to the interpreter

        TODO: Investigate if both (Overpass QL and XML) requests can be sent
        """

        try:
            response = self._overpass.post(url="/api/interpreter", data=payload)
        except (TimeoutError, ConnectionError) as e:
            # TODO: Raise specific error
            raise Exception(e)

        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            # TODO: Raise specific error
            raise Exception(e)

        try:
            return Response(**response.json())
        except ValidationError as e:
            # TODO: Raise specific error
            raise Exception(e)


c = Client()

c._post("")
