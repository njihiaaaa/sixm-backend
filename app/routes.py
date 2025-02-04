from flask import request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from .models import db, User, Product, Order
import logging

# ✅ Initialize Logging
logging.basicConfig(level=logging.INFO)

# ✅ API Configuration
api = Api(
    title="Hardware App API",
    description="A REST API for a hardware store",
    version="1.0"
)

# ----------- Register Namespaces -----------
user_ns = api.namespace("users", description="User operations")
product_ns = api.namespace("products", description="Product operations")
order_ns = api.namespace("orders", description="Order operations")

# ----------- Swagger Models -----------
user_model = api.model(
    "User",
    {
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=True, description="Password"),
        "role": fields.String(required=True, description="User role (Admin/Regular)"),
    },
)

product_model = api.model(
    "Product",
    {
        "name": fields.String(required=True, description="Product name"),
        "description": fields.String(required=True, description="Product description"),
        "price": fields.Float(required=True, description="Product price"),
        "category": fields.String(required=True, description="Product category"),
    },
)

# ----------- ✅ User Routes -----------
@user_ns.route("/")
class UserList(Resource):
    def get(self):
        """🔹 Get all users"""
        try:
            users = User.query.all()
            return jsonify(
                [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]
            )
        except Exception as e:
            logging.error(f"Error fetching users: {str(e)}")
            return {"error": "Failed to fetch users"}, 500

    @api.expect(user_model)
    def post(self):
        """🔹 Create a new user"""
        data = request.get_json()

        required_fields = ["username", "email", "password", "role"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already registered"}, 400

        try:
            new_user = User(username=data["username"], email=data["email"], role=data["role"])
            new_user.set_password(data["password"])
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"User creation error: {str(e)}")
            return {"error": str(e)}, 500

@user_ns.route("/login")
class UserLogin(Resource):
    def post(self):
        """🔹 Authenticate user"""
        data = request.get_json()

        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return {"error": "User not found"}, 404

        if not user.check_password(data["password"]):
            return {"error": "Invalid password"}, 401

        return {
            "message": "Login successful",
            "user": {"id": user.id, "username": user.username, "email": user.email}
        }, 200

# ----------- ✅ Product Routes -----------
@product_ns.route("/")
class ProductList(Resource):
    def get(self):
        """🔹 Get all products"""
        try:
            products = Product.query.all()
            if not products:
                return {"message": "No products found"}, 200
            return jsonify(
                [
                    {
                        "id": p.id,
                        "name": p.name,
                        "description": p.description,
                        "price": p.price,
                        "category": p.category,
                    }
                    for p in products
                ]
            )
        except Exception as e:
            logging.error(f"Error fetching products: {str(e)}")
            return {"error": "Failed to fetch products"}, 500

    @api.expect(product_model)
    def post(self):
        """🔹 Create a new product and prevent duplicates"""
        data = request.get_json()

        required_fields = ["name", "description", "price", "category"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400

        existing_product = Product.query.filter_by(name=data["name"]).first()
        if existing_product:
            return {"error": "Product already exists!"}, 409  # HTTP 409 Conflict

        try:
            new_product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                category=data["category"]
            )
            db.session.add(new_product)
            db.session.commit()
            return {"message": "Product added successfully"}, 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding product: {str(e)}")
            return {"error": str(e)}, 500

# ----------- ✅ Attach Namespaces to API -----------
api.add_namespace(user_ns)
api.add_namespace(product_ns)
api.add_namespace(order_ns)

def configure_routes(app):
    """🔹 Attach API to Flask app"""
    api.init_app(app)
