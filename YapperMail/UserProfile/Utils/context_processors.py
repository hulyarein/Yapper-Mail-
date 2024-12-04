from django.templatetags.static import static

def user_profile_picture(request):
    user = request.user

    # Check if user is authenticated and has a profile picture
    if user.is_authenticated and user.profile_picture and hasattr(user.profile_picture, 'url'):
        profile_picture = user.profile_picture.url

        first_name = user.first_name
        last_name = user.last_name
    else:
        # Fallback to the static default profile picture
        profile_picture = static('images/default_profile.jpg')
        first_name = ''
        last_name = ''

    print(profile_picture) # Debugging
    return {'profile_picture_url': profile_picture,
            'first_name': first_name,
            'last_name': last_name,}
