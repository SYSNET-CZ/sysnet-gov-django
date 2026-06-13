from datetime import datetime
import hashlib
from typing import Any, Dict, Optional
from sqlalchemy import Column, String, DateTime, JSON, BigInteger, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    # TimescaleDB requires a timestamp as part of the primary key or unique index
    # but for simple hypertable, standard PK on id + hypertable create is enough
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    actor_id = Column(String(128), index=True) # Keycloak 'sub'
    action = Column(String(64), index=True)    # ACCESS, CREATE, DEDUCT, etc.
    target_id = Column(String(128), index=True) # Permit/Item ID
    client_ip = Column(String(45))
    
    # Payload for detailed changes/context
    payload = Column(JSON, default=dict)
    
    # Immutability Chain (Resolves Gap Analysis Finding 1.1)
    prev_hash = Column(String(64), nullable=True) # Hash of the previous record
    current_hash = Column(String(64), unique=True) # SHA-256 of all fields + prev_hash
    
    def calculate_hash(self, previous_hash: str) -> str:
        data = f"{self.timestamp}|{self.actor_id}|{self.action}|{self.target_id}|{previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

    def __repr__(self):
        return f"<AuditLog(action={self.action}, actor={self.actor_id})>"

async def setup_timescaledb(engine):
    """
    Ensures the audit_log table is converted to a hypertable.
    TimescaleDB chunks data by time for performance at scale.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Check if Timescale extension exists and create hypertable
        try:
            await conn.execute(text("SELECT create_hypertable('audit_log', 'timestamp', if_not_exists => TRUE);"))
        except Exception as e:
            print(f"Warning: Could not create hypertable (perhaps not a TimescaleDB instance): {e}")
