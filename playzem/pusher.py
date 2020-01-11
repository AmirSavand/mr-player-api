from pusher import pusher, Pusher

from party.pusher import get_channel_name
from playzem import settings


class ModelEventNameAffix:
    """
    Model related pusher signals have these affixes
    Example: "song-create"
    """
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'


def model_trigger(instance, created: bool = None, channel: str = None, data: str = None) -> None:
    """
    Used for model receivers to trigger pusher signals for them
    """
    # Events for models with parties are structured
    if not channel and hasattr(instance, 'party'):
        channel = get_channel_name(instance.party.pk)

    # For model signals, we use PusherEventNameAffix
    event: str = ModelEventNameAffix.CREATE if created else ModelEventNameAffix.UPDATE
    if created is None:
        event = ModelEventNameAffix.DELETE

    # Add model as event name with event affix
    event = '{model}-{affix}'.format(model=instance.__class__.__name__, affix=event).lower()

    # If data is not given, set data to instance PK
    data = data if data else str(instance.pk)

    # Trigger a pusher
    pusher_client.trigger(channel, event, data)


# Initiate pusher client
if settings.PUSHER_APP_ID:
    pusher_client: Pusher = pusher.Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET,
        cluster=settings.PUSHER_CLUSTER,
        ssl=settings.PUSHER_SSL,
    )
