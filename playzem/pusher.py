from pusher import pusher, Pusher

from playzem import settings

pusher_client: Pusher = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=settings.PUSHER_SSL,
)
