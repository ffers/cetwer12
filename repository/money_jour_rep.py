from server_flask.db import db
from server_flask.models import MoneyJournal
from sqlalchemy import desc
from domain.models.money_jour_dto import MoneyJournalDto

class JourChRep:
    def load_all(self):
        items = MoneyJournal.query.order_by(desc(MoneyJournal.timestamp)).all()
        items_dto = []
        for item in items:
            items_dto.append(
                MoneyJournalDto(
                    id=item.id,
                    timestamp=item.timestamp,
                    event_date=item.event_date,
                    description=item.description,
                    movement=item.movement,
                    total=item.total
                )
                )
        return items_dto

    def add_(self, dto: MoneyJournalDto):
        try:
            item = MoneyJournal(
                    event_date=dto.event_date,
                    description=dto.description,
                    movement=dto.movement,
                    total=dto.total
                )
            db.session.add(item)
            db.session.commit()
            return True
        except Exception as e:
            ValueError(f"Помилка додавання в бд {e}")

    def update_(self, id, dto):
        try:
            instance = MoneyJournal.query.get_or_404(id)
            instance.event_date = dto.event_date
            instance.description = dto.description
            instance.movement = dto.movement
            instance.total = dto.total
            db.session.commit()
            db.session.refresh()
            return instance
        except Exception as e:
            ValueError(f"Помилка оновленя в бд {e}")

    def delete_(self, id):
        task_to_delete = MoneyJournal.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

