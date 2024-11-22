from app.models import login_table

def logged_in_user(request):
    if request.user.is_authenticated:
        user_id = request.session.get('lid')
        try:
            user = login_table.objects.get(id=user_id)
            return {'logged_in_user': user.username}
        except login_table.DoesNotExist:
            return {'logged_in_user': None}
    return {'logged_in_user': None}
