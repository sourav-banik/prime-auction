import hashlib
import urllib

# generate user avatar 
def gravatar_url(email, size=64):
    avatar_url = "https://ui-avatars.com/api/?name=" + email + "&background=random&size=" + str(size) 
    return avatar_url