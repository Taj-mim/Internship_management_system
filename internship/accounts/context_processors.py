from .models import Notification


def notifications(request):

    if not request.user.is_authenticated:
        return {
            "unread_notifications_count": 0,
            "nav_notifications": [],
        }

    user_notifications = Notification.objects.filter(
        user=request.user
    )

    return {
        "unread_notifications_count": user_notifications.filter(
            is_read=False
        ).count(),
        "nav_notifications": user_notifications[:5],
    }
