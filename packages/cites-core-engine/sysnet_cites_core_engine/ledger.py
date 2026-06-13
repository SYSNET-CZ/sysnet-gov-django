from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class LedgerEntry(BaseModel):
    """
    Transactional quantity depletion entry.
    Implements double-entry-like auditing for customs clearance.
    """
    id: Optional[str] = Field(None, description="Internal entry UUID")
    permit_id: str
    item_id: str
    operation: str = Field(..., description="DEBIT (clearance) or CREDIT (reversal)")
    amount: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.now)
    officer_id: Optional[str] = None
    customs_office: Optional[str] = None
    mrd_number: Optional[str] = Field(None, description="Master Reference Number from Customs")

class LedgerService:
    """Service for handling quantity depletions and reversals."""
    def __init__(self):
        self._entries: List[LedgerEntry] = []

    def log_operation(self, entry: LedgerEntry) -> None:
        self._entries.append(entry)

ledger = LedgerService()
