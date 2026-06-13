from .models import AuditLog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

class AuditLogger:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_hash(self) -> str:
        stmt = select(AuditLog.current_hash).order_by(AuditLog.id.desc()).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar() or "GENESIS"

    async def log(
        self, 
        actor_id: str, 
        action: str, 
        permit: Optional[Any] = None, # Simplified for import
        target_id: Optional[str] = None, 
        amount: float = 0.0,
        payload: dict = None,
        client_ip: str = None
    ):
        prev_h = await self.get_last_hash()
        
        entry = AuditLog(
            actor_id=actor_id,
            action=action,
            target_id=target_id,
            payload=payload or {},
            client_ip=client_ip,
            timestamp=datetime.utcnow(),
            prev_hash=prev_h
        )
        
        # Calculate current hash including chain
        entry.current_hash = entry.calculate_hash(prev_h)
        
        self.session.add(entry)
        await self.session.commit()
