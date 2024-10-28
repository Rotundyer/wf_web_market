from sqlalchemy.ext.asyncio import AsyncSession
from market_analysis.db.models import ArcaneLocation, ArcaneLocationCreate
from sqlmodel import select


class ArcaneLocationDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_location(self, location: ArcaneLocationCreate):
        query = select(ArcaneLocation).where(ArcaneLocation.name == location.name)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            arc_loc = ArcaneLocation(name=location.name)
            self.db_session.add(arc_loc)
            await self.db_session.commit()
            await self.db_session.refresh(arc_loc)
            return arc_loc
        return 'Such a location already exists in the database'

    async def get_all_location(self):
        query = select(ArcaneLocation)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        locations = []
        for row in rows:
            for loc in row:
                locations.append(loc)
        return locations
