from typing import Protocol, runtime_checkable, Any
from sysnet_cites_core_types.models import CITESPermit

@runtime_checkable
class NationalPlugin(Protocol):
    """
    Protocol for national extensions.
    Implements ADR-0016: Decorator pattern for legislative specifics.
    """
    def augment_permit(self, permit: CITESPermit) -> CITESPermit: ...
    def validate_custom_rules(self, permit: CITESPermit) -> bool: ...
    def get_national_metadata(self) -> dict[str, Any]: ...
