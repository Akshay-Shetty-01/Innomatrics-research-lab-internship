
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List 
 
app = FastAPI()
 
# ── Pydantic model ───────────────────────────────────────────────────────────
class OrderRequest(BaseModel):
    customer_name:    str = Field(..., min_length=2, max_length=100)
    product_id:       int = Field(..., gt=0)
    quantity:         int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)
 
orders = []
order_counter = 1
class customerfeedback(BaseModel):
    customer_name:    str = Field(..., min_length=2, max_length=100)
    product_id:       int = Field(..., gt=0)
    rating:         int = Field(..., gt=0, le=6)
    comment: str = Field(..., max_length=300)
feedbacks=[]
feedback_counter = 0
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity:   int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name:  str           = Field(..., min_length=2)
    contact_email: str           = Field(..., min_length=5)
    items:         List[OrderItem] = Field(..., min_items=1)

 
# ── Endpoints ───────────────────────────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}
 
@app.post('/feedback')
def get_feedback(feedback_data : customerfeedback ):
    global feedback_counter
    product = next((p for p in products if p['id']==feedback_data.product_id), None)
    if product is None:          return {'error': 'Product not found'}
    feedback={
                "customer_name": feedback_data.customer_name,
    "product_id": feedback_data.product_id,
    "rating": feedback_data.rating,
    "comment":feedback_data.comment
    }
    feedbacks.append(feedback)
    feedback_counter += 1
    return{"message": "Feedback submitted successfully","feedback":feedback,"total_feedback":feedback_counter}

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}
@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter
    product = next((p for p in products if p['id']==order_data.product_id), None)
    if product is None:          return {'error': 'Product not found'}
    if not product['in_stock']:  return {'error': f"{product['name']} is out of stock"}
    total_price = product['price'] * order_data.quantity
    order = {'order_id': order_counter, 'customer_name': order_data.customer_name,
            'product': product['name'], 'quantity': order_data.quantity,
            'delivery_address': order_data.delivery_address,
            'total_price': total_price, 'status': 'pending'}
    orders.append(order)
    order_counter += 1
    return {'message': 'Order placed successfully', 'order': order}
@app.get("/products/summary")
def product_summary():
    in_stock   = [p for p in products if     p["in_stock"]]
    out_stock  = [p for p in products if not p["in_stock"]]
    expensive  = max(products, key=lambda p: p["price"])
    cheapest   = min(products, key=lambda p: p["price"])
    categories = list(set(p["category"] for p in products))
    return {
        "total_products":     len(products),
        "in_stock_count":     len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive":     {"name": expensive["name"], "price": expensive["price"]},
        "cheapest":           {"name": cheapest["name"],  "price": cheapest["price"]},
        "categories":         categories,
    }


@app.get('/orders')
def get_all_orders():
    return {'orders': orders, 'total_orders': len(orders)}
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': True},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True}, 
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True}, 
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}
# ── Endpoint 2 — Return one product by its ID ──────────────────
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}
    return {"error": "Order not found"}
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return {"message": "Order confirmed", "order": order}
    return {"error": "Order not found"}

@app.get("/products/deals")
def product_deals():

    cheapest = products[0]
    expensive = products[0]

    for product in products:

        if product["price"] < cheapest["price"]:
            cheapest = product

        if product["price"] > expensive["price"]:
            expensive = product

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    } 

# ── Endpoint 3 — Return one product by its ID ──────────────────
@app.get("/products/instock") 
def get_instock_products():
    instock_products = []
    for p in products:
        if p["in_stock"] == True:
            instock_products.append(p)
    return { "in_stock_products": instock_products, "count": len(instock_products)}
 

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only'),
    min_price: int = Query(None, description='Minimum price'),):

    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
    if min_price:
        result = [p for p in result if p['price'] >= min_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    
 
    return {'filtered_products': result, 'count': len(result)}
@app.get('/products/{product_id}/price')
def get_product_price(product_id:int):
    for product in products:
        if product['id'] == product_id:
            return {'name':product['name'],'price':product['price'] }
    return {'error': 'Product not found'}

# ── Endpoint 4 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

@app.get("/products/category/{category_name}") 
def get_by_category(category_name: str): 
    result = [p for p in products if p["category"] == category_name] 
    if not result: 
        return {"error": "No products found in this category"} 
    return {"category": category_name, "products": result, "total": len(result)}

@app.get("/store/search/{keword}")
def store_product(keword):
    for p in products:
        if p["name"] == keword:
            return ( "the produvt is present ")
    return {"not present "}



@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(product)

    if len(matched_products) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }


@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock = 0
    out_of_stock = 0
    categories = []

    for p in products:

        if p["in_stock"]:
            in_stock += 1
        else:
            out_of_stock += 1

        if p["category"] not in categories:
            categories.append(p["category"])

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }


