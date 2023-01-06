import jwt, datetime, os 
from flask import Flask, request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

server = Flask(__name__)
mysql = MySQL(server)
bcrypt = Bcrypt(server)

# configuration
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    # check db for email and password
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT * FROM users WHERE email = %s", (auth.username,))
    if res > 0:
        user = cur.fetchone()
        email = user[0]
        password = user[1]

        if auth.username != email and bcrypt.check_password_hash(password, auth.password):
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "User not found", 404

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "Missing token", 401

    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded_jwt = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "Token expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 401

    return decoded_jwt, 200


def createJWT(username, secret, authz):
    return jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "admin": authz
    }, secret, algorithm="HS256")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)
