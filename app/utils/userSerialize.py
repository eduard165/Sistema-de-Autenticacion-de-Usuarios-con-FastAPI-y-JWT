from bson import ObjectId
def serialize_user(user):
    """Convertir el ObjectId a string y retornar el documento."""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }
