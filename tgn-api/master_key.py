from tgnLIB import encode
import string
import secrets
alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(24))
base_string = encode(password)
print("New Master_key: "+password)
f = open("api.db", "w")
f.write(base_string)
f.close()