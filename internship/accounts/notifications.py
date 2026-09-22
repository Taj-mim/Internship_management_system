from .models import Notification


def notify_user(user, message):
    """Create a single notification for one user account."""

    if user is None:
        return None

    return Notification.objects.create(
        user=user,
        email=user.email,
        message=message
    )


def notify_users(users, message):
    """Create the same notification for a queryset/list of users."""

    notifications = [
        Notification(
            user=user,
            email=user.email,
            message=message
        )
        for user in users
    ]

    return Notification.objects.bulk_create(notifications)
