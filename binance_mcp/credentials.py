"""Static credential backend that tolerates missing headers so public tools work without keys."""

from typing import Literal

from fastmcp_credentials import (
    CredentialBackend,
    HeaderCredentialBackend,
    MissingCredentialHeaderError,
    ResolvedCredential,
)


class OptionalStaticBackend(CredentialBackend):
    def __init__(self) -> None:
        self._headers = HeaderCredentialBackend()

    async def resolve(self, credential_type: Literal["static", "oauth"]) -> ResolvedCredential:
        try:
            return await self._headers.resolve("static")
        except MissingCredentialHeaderError:
            return ResolvedCredential(type="static")
