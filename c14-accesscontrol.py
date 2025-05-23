from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from functools import wraps

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Replace with a strong key
jwt = JWTManager(app)

# In-memory stores
users = {}  # username -> {'password': ..., 'roles': [...]}
roles = {   # role -> permissions
    "admin": {"read", "write", "delete"},
    "editor": {"read", "write"},
    "viewer": {"read"}
}


# Decorator to check permission
def permission_required(permission):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            username = get_jwt_identity()
            user = users.get(username)
            if not user:
                return jsonify({"msg": "User not found"}), 404

            user_roles = user.get("roles", [])
            for role in user_roles:
                if permission in roles.get(role, set()):
                    return fn(*args, **kwargs)
            return jsonify({"msg": "Access denied"}), 403
        return wrapper
    return decorator


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "viewer")

    if username in users:
        return jsonify({"msg": "User already exists"}), 400

    if role not in roles:
        return jsonify({"msg": "Invalid role"}), 400

    users[username] = {
        "password": password,
        "roles": [role]
    }
    return jsonify({"msg": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Bad credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/read-resource", methods=["GET"])
@permission_required("read")
def read_resource():
    return jsonify({"msg": "You have access to read this resource."})


@app.route("/write-resource", methods=["POST"])
@permission_required("write")
def write_resource():
    return jsonify({"msg": "You can write to this resource."})


@app.route("/delete-resource", methods=["DELETE"])
@permission_required("delete")
def delete_resource():
    return jsonify({"msg": "You can delete this resource."})


if __name__ == "__main__":
    app.run(debug=True)
