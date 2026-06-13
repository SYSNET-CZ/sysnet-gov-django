from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, func
from sqlalchemy.dialects.postgresql import insert
from geoalchemy2.functions import ST_AsText
from sysnet_cites_core_types.models import (
    CITESPermit, CITESPerson, CITESItem, CITESAppendix, CITESStatus, CITESMovement
)
from sysnet_cites_core_types.database import PermitDB, ItemDB, MovementDB
from .service import PermitRepository

class PostgreSQLRepository(PermitRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_permit(self, permit_id: str) -> Optional[CITESPermit]:
        stmt = select(PermitDB).options(selectinload(PermitDB.items)).where(PermitDB.permit_number == permit_id)
        result = await self.session.execute(stmt)
        db_p = result.scalar_one_or_none()
        if not db_p: return None
        exporter = CITESPerson(name=db_p.exporter_name, address="N/A", country_code=db_p.exporter_country, eori_number=db_p.exporter_eori)
        importer = CITESPerson(name=db_p.importer_name, address="N/A", country_code=db_p.importer_country, eori_number=db_p.importer_eori)
        items = [CITESItem(taxon_id=it.taxon_id, appendix=CITESAppendix(it.appendix), quantity=float(it.quantity), deducted_quantity=float(it.deducted_quantity), unit=it.unit, is_exhausted=it.is_exhausted, source_code="U", purpose_code="P") for it in db_p.items]
        return CITESPermit(permit_number=db_p.permit_number, status=CITESStatus(db_p.status), issue_date=db_p.issue_date, expiry_date=db_p.expiry_date, exporter=exporter, importer=importer, items=items, issuing_authority="N/A", version=db_p.version)

    async def save_permit(self, permit: CITESPermit) -> None:
        stmt = insert(PermitDB).values(permit_number=permit.permit_number, status=permit.status.value, issue_date=permit.issue_date, expiry_date=permit.expiry_date, version=permit.version, exporter_name=permit.exporter.name, exporter_country=permit.exporter.country_code, exporter_eori=permit.exporter.eori_number, importer_name=permit.importer.name, importer_country=permit.importer.country_code, importer_eori=permit.importer.eori_number).on_conflict_do_update(index_elements=[PermitDB.permit_number], set_={"status": permit.status.value, "version": permit.version, "updated_at": func.now()}).returning(PermitDB.id)
        res = await self.session.execute(stmt)
        db_permit_id = res.scalar_one()
        await self.session.execute(delete(ItemDB).where(ItemDB.permit_id == db_permit_id))
        for item in permit.items:
            self.session.add(ItemDB(permit_id=db_permit_id, taxon_id=item.taxon_id, appendix=item.appendix.value, quantity=item.quantity, deducted_quantity=item.deducted_quantity, unit=item.unit, is_exhausted=item.is_exhausted, description=item.description))
        await self.session.flush()

    async def log_movement(self, movement: CITESMovement) -> None:
        stmt = select(PermitDB.id).where(PermitDB.permit_number == movement.permit_id)
        res = await self.session.execute(stmt)
        db_permit_id = res.scalar_one()
        db_move = MovementDB(permit_id=db_permit_id, location=f"SRID=4326;POINT({movement.longitude} {movement.latitude})", address=movement.address, event_type=movement.event_type, remarks=movement.remarks)
        self.session.add(db_move)
        await self.session.flush()

    async def get_movements(self, permit_number: str) -> List[CITESMovement]:
        stmt = select(MovementDB, ST_AsText(MovementDB.location).label("wkt")).join(PermitDB).where(PermitDB.permit_number == permit_number).order_by(MovementDB.timestamp.desc())
        res = await self.session.execute(stmt)
        movements = []
        for db_m, wkt in res:
            # WKT format is typically "POINT(14.421 50.087)"
            cleaned = str(wkt).replace("POINT(", "").replace(")", "")
            parts = cleaned.split()
            lon, lat = float(parts[0]), float(parts[1])
            movements.append(CITESMovement(id=db_m.id, permit_id=permit_number, timestamp=db_m.timestamp, latitude=lat, longitude=lon, address=db_m.address, event_type=db_m.event_type, remarks=db_m.remarks))
        return movements
