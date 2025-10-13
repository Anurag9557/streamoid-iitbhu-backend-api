from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import csv
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Models ---
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=True)
    size = db.Column(db.String, nullable=True)
    mrp = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "brand": self.brand,
            "color": self.color,
            "size": self.size,
            "mrp": int(self.mrp) if self.mrp.is_integer() else self.mrp,
            "price": int(self.price) if self.price.is_integer() else self.price,
            "quantity": self.quantity,
        }

# Create DB tables
with app.app_context():
    db.create_all()

# --- Helpers ---
REQUIRED_FIELDS = {"sku", "name", "brand", "mrp", "price"}

def parse_number(value, field_name):
    if value is None or value == "":
        raise ValueError(f"{field_name} is missing")
    try:
        if "." in value:
            return float(value)
        else:
            return float(int(value))
    except Exception:
        # fallback: try float
        try:
            return float(value)
        except Exception:
            raise ValueError(f"{field_name} must be numeric (got '{value}')")

# --- Routes ---
@app.route("/upload", methods=["POST"])
def upload_csv():
    """
    Expects a form upload with field 'file' containing a CSV.
    Returns JSON: stored count and list of failed rows with errors.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part (field name must be 'file')"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # read CSV content as text
    stream = io.StringIO(file.stream.read().decode("utf-8-sig"))
    reader = csv.DictReader(stream)
    stored = 0
    failed = []

    line_num = 1  # header line
    for row in reader:
        line_num += 1
        # normalize keys (strip)
        row = {k.strip(): (v.strip() if v is not None else v) for k, v in row.items()}
        errors = []

        # Check required fields presence
        missing = [f for f in REQUIRED_FIELDS if f not in row or row[f] == "" or row[f] is None]
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")

        # parse numeric fields
        mrp = price = quantity = None
        if "mrp" in row and row.get("mrp", "") != "":
            try:
                mrp = parse_number(row["mrp"], "mrp")
            except ValueError as e:
                errors.append(str(e))
        if "price" in row and row.get("price", "") != "":
            try:
                price = parse_number(row["price"], "price")
            except ValueError as e:
                errors.append(str(e))
        if "quantity" in row and row.get("quantity", "") != "":
            try:
                q = parse_number(row["quantity"], "quantity")
                quantity = int(q)
            except ValueError:
                errors.append("quantity must be integer")
            except Exception:
                errors.append("quantity parse error")

        # business validations
        if (mrp is not None) and (price is not None):
            if price > mrp:
                errors.append("price must be <= mrp")
        if quantity is not None:
            if quantity < 0:
                errors.append("quantity must be >= 0")

        # If any errors, append to failed with row info
        if errors:
            failed.append({
                "line": line_num,
                "sku": row.get("sku"),
                "errors": errors,
                "row": row
            })
            continue

        # Save to DB (insert or update by SKU)
        sku = row.get("sku")
        name = row.get("name")
        brand = row.get("brand")
        color = row.get("color") or None
        size = row.get("size") or None
        # Ensure numeric defaults if missing
        mrp = float(mrp) if mrp is not None else 0.0
        price = float(price) if price is not None else 0.0
        quantity = int(quantity) if quantity is not None else 0

        try:
            existing = Product.query.filter_by(sku=sku).first()
            if existing:
                # update fields
                existing.name = name
                existing.brand = brand
                existing.color = color
                existing.size = size
                existing.mrp = mrp
                existing.price = price
                existing.quantity = quantity
            else:
                new_p = Product(
                    sku=sku,
                    name=name,
                    brand=brand,
                    color=color,
                    size=size,
                    mrp=mrp,
                    price=price,
                    quantity=quantity
                )
                db.session.add(new_p)
            db.session.commit()
            stored += 1
        except IntegrityError as e:
            db.session.rollback()
            failed.append({
                "line": line_num,
                "sku": sku,
                "errors": ["database integrity error", str(e.orig) if hasattr(e, "orig") else str(e)],
                "row": row
            })
        except Exception as e:
            db.session.rollback()
            failed.append({
                "line": line_num,
                "sku": sku,
                "errors": ["unexpected error saving row", str(e)],
                "row": row
            })

    return jsonify({"stored": stored, "failed": failed})

@app.route("/products", methods=["GET"])
def list_products():
    """
    GET /products?page=1&limit=10
    Returns paginated list
    """
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "page and limit must be integers"}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "page and limit must be >= 1"}), 400

    query = Product.query.order_by(Product.id)
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "products": [p.to_dict() for p in items]
    })

@app.route("/products/search", methods=["GET"])
def search_products():
    """
    Filters:
      brand
      color
      minPrice
      maxPrice
    Supports pagination: page & limit
    """
    brand = request.args.get("brand")
    color = request.args.get("color")
    min_price = request.args.get("minPrice")
    max_price = request.args.get("maxPrice")
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "page and limit must be integers"}), 400

    q = Product.query
    if brand:
        q = q.filter(Product.brand.ilike(f"%{brand}%"))
    if color:
        q = q.filter(Product.color.ilike(f"%{color}%"))
    if min_price:
        try:
            mn = float(min_price)
            q = q.filter(Product.price >= mn)
        except ValueError:
            return jsonify({"error": "minPrice must be numeric"}), 400
    if max_price:
        try:
            mx = float(max_price)
            q = q.filter(Product.price <= mx)
        except ValueError:
            return jsonify({"error": "maxPrice must be numeric"}), 400

    total = q.count()
    items = q.order_by(Product.id).offset((page - 1) * limit).limit(limit).all()
    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "products": [p.to_dict() for p in items]
    })

# Simple health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
