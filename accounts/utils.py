def detectUser(user):
    if user.role == 1:
        redirectUrl = 'accounts:vendor-dashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'accounts:customer-dashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
