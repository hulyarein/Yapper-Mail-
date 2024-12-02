from django.templatetags.static import static

def user_profile_picture(request):
    if request.user.is_authenticated:
        profile_picture = (
            request.user.profile_picture.url if request.user.profile_picture else static('images/default_profile.jpg')
        )
    else:
        profile_picture = static('images/default_profile.jpg')
    return {'profile_picture_url': profile_picture}
