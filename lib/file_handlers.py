def handle_uploaded_resume(f, username):
    import os
    import tempfile
    from django.conf import settings
    
    extension = os.path.splitext(f.name)[-1]
    directory = ''.join((
        settings.MEDIA_ROOT, os.path.sep, 'resumes', os.path.sep,
        username, os.path.sep
    ))
    try:
        os.mkdir(directory)
    except:
        pass
    fd, filename = tempfile.mkstemp(extension, "resume_", directory)
    destination = os.fdopen(fd, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
    base_file = os.path.basename(filename)
    
    path = ''.join(('resumes', '/', username, '/', base_file))
    
    return path