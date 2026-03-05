from fastapi import FastAPI

app = FastAPI()

# products list
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 500, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Keyboard", "price": 1500, "category": "Electronics", "in_stock": True},
    {"id": 4, "name": "Monitor", "price": 12000, "category": "Electronics", "in_stock": True},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

@app.get("/")
def home():
    return {"message": "Welcome to Product API"}

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
    
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = []
    
    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_products.append(product)
            
    if len(filtered_products) == 0:
        return {"error": "No products found in this category"}
    
    return {
        "products": filtered_products,
        "total": len(filtered_products)
    }
    
@app.get("/products/instock")
def get_instock_products():
    instock_products = []
    
    for product in products:
        if product["in_stock"] == True:
            instock_products.append(product)
            
    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }

@app.get("/store/summary")
def store_summary():
    total_products = len(products)
    
    in_stock = 0
    out_of_stock = 0
    categories = []
    
    for product in products:
        if product["in_stock"]:
            in_stock += 1
        else:
            out_of_stock += 1
        
        if product["category"] not in categories:
            categories.append(product["category"])
            
    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }
    
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    matched_products = []
    
    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(products)
        
    if len(matched_products) == 0:
        return {"message": "No products matched your search"}
    
    return {
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }

@app.get("/products/deals")
def get_best_deals():

    cheapest_product = min(products, key=lambda x: x["price"])
    most_expensive_product = max(products, key=lambda x: x["price"])

    return {
        "best_deal": cheapest_product,
        "premium_pick": most_expensive_product
    }