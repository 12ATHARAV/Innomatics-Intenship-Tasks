# 🚗 SpeedRide Car Rental Service

A RESTful API built with **FastAPI** for managing a car rental system — including fleet management, bookings, pricing with discounts, and rental history.

---

## 🛠️ Tech Stack

- **Python** with **FastAPI**
- **Pydantic** for request validation
- **Uvicorn** as the ASGI server
- **uv** for dependency management

---

## 📁 Project Structure

```
fastapi_car_rental_service/
├── main.py              # All routes and business logic
├── pyproject.toml       # Project metadata & dependencies
├── requirements.txt     # Pip dependencies
├── uv.lock              # Locked dependency versions
├── .python-version      # Python version pin
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd fastapi_car_rental_service
```

### 2. Create virtual environment & install dependencies

Using **uv** (recommended):

```bash
uv sync
```

Or using **pip**:

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

API will be available at: `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

---

## 🚘 Fleet — 10 Cars Pre-loaded

| Brand | Model | Type | Fuel | Price/Day |
|---|---|---|---|---|
| Honda | City | Sedan | Petrol | ₹2,500 |
| Hyundai | i20 | Hatchback | Petrol | ₹1,500 |
| Tata | Nexon | SUV | Diesel | ₹3,000 |
| Tesla | Model 3 | Luxury | Electric | ₹8,000 |
| Toyota | Fortuner | SUV | Diesel | ₹5,000 |
| BMW | 3 Series | Luxury | Petrol | ₹7,000 |
| Mahindra | Thar | SUV | Petrol | ₹3,500 |
| Mercedes-Benz | E-Class | Luxury | Diesel | ₹9,500 |
| MG | ZS EV | SUV | Electric | ₹4,000 |
| Maruti | Swift | Hatchback | Petrol | ₹1,200 |

---

## 📡 API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message |

---

### Cars

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/cars` | Get all cars with total and available count |
| `GET` | `/cars/summary` | Stats: type breakdown, fuel breakdown, cheapest & most expensive |
| `GET` | `/cars/filter` | Filter by type, brand, fuel_type, max_price, is_available |
| `GET` | `/cars/search?keyword=` | Search by model, brand, or type |
| `GET` | `/cars/sort` | Sort by price_per_day, brand, or type (asc/desc) |
| `GET` | `/cars/page` | Paginate cars (page, limit) |
| `GET` | `/cars/browse` | Combined filter + sort + paginate |
| `GET` | `/cars/unavailable` | List all unavailable cars |
| `GET` | `/cars/{car_id}` | Get a single car by ID |
| `POST` | `/cars` | Add a new car |
| `PUT` | `/cars/{car_id}` | Update price and/or availability |
| `DELETE` | `/cars/{car_id}` | Delete a car (blocked if active rental exists) |

---

### Rentals

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/rental` | Get all rentals |
| `GET` | `/rentals/active` | Get only active rentals |
| `GET` | `/rentals/search?customer_name=` | Search rentals by customer name |
| `GET` | `/rentals/sort` | Sort rentals by total_cost (asc/desc) |
| `GET` | `/rentals/page` | Paginate rentals |
| `GET` | `/rentals/by-car/{car_id}` | Get rental history for a specific car |
| `POST` | `/rentals` | Create a new rental booking |
| `POST` | `/return/{rental_id}` | Return a rented car |

---

## 💰 Pricing & Discount Logic

Base cost = `price_per_day × days`

| Condition | Discount |
|---|---|
| 7–14 days | 15% off base price |
| 15+ days | 25% off base price |
| Insurance add-on | +₹500/day |
| Driver add-on | +₹800/day |

**Formula:**
```
total = base_price - discount + insurance_cost + driver_cost
```

---

## 📋 Request & Response Examples

### POST `/rentals` — Create a Rental

**Request body:**
```json
{
  "customer_name": "Rahul Sharma",
  "car_id": 1,
  "days": 7,
  "license_number": "MH12AB1234",
  "insurance": true,
  "driver_required": false
}
```

**Response:**
```json
{
  "rental_id": 1,
  "customer_name": "Rahul Sharma",
  "car_id": 1,
  "car_model": "City",
  "car_brand": "Honda",
  "days": 7,
  "cost": {
    "base_price": 17500,
    "discount": 2625,
    "insurance_cost": 3500,
    "driver_cost": 0,
    "total_cost": 18375
  },
  "status": "active"
}
```

---

### POST `/cars` — Add a New Car

**Request body:**
```json
{
  "model": "Creta",
  "brand": "Hyundai",
  "type": "SUV",
  "price_per_day": 3200,
  "fuel_type": "Petrol",
  "is_available": true
}
```

---

### GET `/cars/filter` — Filter Cars

```
GET /cars/filter?type=SUV&fuel_type=Diesel&is_available=true
```

---

### GET `/cars/sort` — Sort Cars

```
GET /cars/sort?sort_by=price_per_day&order=desc
```

---

## ✅ Validation Rules

| Field | Rule |
|---|---|
| `customer_name` | Min 2 characters |
| `license_number` | Min 8 characters |
| `days` | Between 0 and 30 |
| `car_id` | Must be > 0 |
| `price_per_day` | Must be > 0 |
| `model` / `brand` / `type` / `fuel_type` | Min 2 characters |

---

## ⚠️ Error Handling

| Scenario | Response |
|---|---|
| Car not found | `404 Not Found` |
| Car already rented | `400 Car not available` |
| Duplicate car on add | `400 Car already exists` |
| Delete car with active rental | `400 Car has active rental` |
| Rental not found on return | `404 Rental not found` |

---

## 📌 Notes

- Car availability is automatically set to `False` when rented and back to `True` when returned.
- All data is stored **in-memory** — restarting the server resets rentals and any added/modified cars.
- Routes with path parameters (e.g. `/cars/{car_id}`) are placed **after** specific routes (e.g. `/cars/filter`) to avoid conflicts.

---

## 📄 License

This project is for educational purposes.