from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class CITESStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CONFISCATED = "confiscated" # Resolves Gap Analysis Finding 4 (Legislation § 25 CZ)

class AuditAction(str, Enum):
    CREATED = "created"
    STATUS_CHANGED = "status_changed"
    QUANTITY_DEDUCTED = "quantity_deducted"
    METADATA_UPDATED = "metadata_updated"

class AuditRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    actor_id: str
    action: AuditAction
    target_id: str
    changes: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None

class CITESAppendix(str, Enum):
    # UN Convention Appendices
    APPENDIX_I = "I"
    APPENDIX_II = "II"
    APPENDIX_III = "III"
    
    # EU Regulation Annexes (Resolves Gap Analysis Finding 1.2)
    ANNEX_A = "A"
    ANNEX_B = "B"
    ANNEX_C = "C"
    ANNEX_D = "D"

def map_annex_to_appendix(annex: str) -> str:
    """Helper to maintain UN compliance while using EU Annexes."""
    mapping = {
        "A": "I",
        "B": "II",
        "C": "III",
        "D": "III"
    }
    return mapping.get(annex, "III")

class PersonType(str, Enum):
    NATURAL = "natural"
    LEGAL = "legal"

class CITESPerson(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    address: str
    country_code: str = Field(..., min_length=2, max_length=2)
    person_type: PersonType = PersonType.NATURAL
    external_id: Optional[str] = None
    eori_number: Optional[str] = None

class CITESItem(BaseModel):
    taxon_id: str = Field(..., description="Species+ UUID or standardized name")
    common_name: Optional[str] = None
    appendix: CITESAppendix
    quantity: float
    unit: str = "PCE"
    description: Optional[str] = None
    source_code: str = Field(..., max_length=1)
    purpose_code: str = Field(..., max_length=1)
    hs_code: Optional[str] = Field(None, description="Customs Harmonized System Code")
    deducted_quantity: float = 0.0
    is_exhausted: bool = False

    def deduct(self, amount: float) -> None:
        """Deduct quantity for customs clearance."""
        if self.is_exhausted:
            raise ValueError("Item is already exhausted")
        if self.deducted_quantity + amount > self.quantity:
            remaining = self.quantity - self.deducted_quantity
            raise ValueError(f"Insufficient quantity: remaining {remaining}, requested {amount}")
        self.deducted_quantity += amount
        if self.deducted_quantity >= self.quantity:
            self.is_exhausted = True

class CITESPermit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    permit_number: str = Field(..., description="Unique permit identifier")
    status: CITESStatus = CITESStatus.PENDING
    issue_date: datetime
    expiry_date: Optional[datetime] = None
    exporter: CITESPerson
    importer: CITESPerson
    items: List[CITESItem]
    issuing_authority: str
    security_stamp: Optional[str] = None
    version: int = 1
    extension_data: Dict[str, Any] = Field(default_factory=dict)

class LedgerEntry(BaseModel):
    """Atomic transactional record of a quantity deduction."""
    entry_id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    permit_number: str
    taxon_id: str
    amount: float
    officer_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    previous_balance: float
    new_balance: float
    mrn_number: Optional[str] = None # Fixed from mrd_number

class CITESMovement(BaseModel):
    id: Optional[int] = None
    permit_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    latitude: float
    longitude: float
    address: Optional[str] = None
    event_type: str
    remarks: Optional[str] = None
    """Atomic transactional record of a quantity deduction."""
    entry_id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    permit_number: str
    taxon_id: str
    amount: float
    officer_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    previous_balance: float
    new_balance: float

class CITESAttachment(BaseModel):
    """Reference to an external file stored in the attachments microservice."""
    attachment_id: UUID
    filename: str
    file_type: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    url: Optional[str] = None

class CITESQuota(BaseModel):
    """National or global export quota for a specific taxon and year."""
    taxon_id: str
    year: int
    total_limit: float
    current_usage: float = 0.0
    unit: str = "PCE"

    @property
    def remaining(self) -> float:
        return self.total_limit - self.current_usage
