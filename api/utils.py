import string
import secrets


def generate_random_string(length, uppercase=False, method='hex', urlsafe=True):
    if length < 1:
        length = 10

    if method == 'hex' and urlsafe:
        return secrets.token_urlsafe(length // 2)
    elif method == 'hex' and not urlsafe:
        return secrets.token_hex(length)
    elif method == 'ascii':
        return str(''.join(secrets.choice((string.ascii_uppercase if uppercase else string.ascii_lowercase) + string.digits) for i in range(length)))


def get_ip_from_request(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


EDITORJS_PLUGINS = [
    '@editorjs/paragraph',
    '@editorjs/image',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/checklist',
    '@editorjs/quote',
    '@editorjs/raw',
    '@editorjs/code',
    '@editorjs/inline-code',
    '@editorjs/embed',
    '@editorjs/delimiter',
    '@editorjs/warning',
    '@editorjs/link',
    '@editorjs/marker',
    '@editorjs/table'
]