from datetime import datetime, timezone
from typing import Type, TypeVar

from django.contrib.sessions.models import Session

SessionType = TypeVar('SessionType', bound=Session)


def validate_session(session_key: str) -> Type[SessionType] | None:
    try:
        session = Session.objects.get(session_key=session_key)
        is_expired = session.expire_date < datetime.now(tz=timezone.utc)
        if is_expired:
            return None
        return session
    except Session.DoesNotExist:
        return None
