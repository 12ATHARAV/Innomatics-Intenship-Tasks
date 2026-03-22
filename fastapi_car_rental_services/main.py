from fastapi import FastAPI, HTTPException, status, Response, Query
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from collections import Counter

app = FastAPI(
    title="SpeedRide Car Rentals",
    description="A REST API for managing car rentals, bookings, and fleet.",
)


# Q2
cars = [
    {"id": 1, "model": "City", "brand": "Honda", "type": "Sedan", "price_per_day": 2500, "fuel_type": "Petrol", "is_available": True},
    {"id": 2, "model": "i20", "brand": "Hyundai", "type": "Hatchback", "price_per_day": 1500, "fuel_type": "Petrol", "is_available": True},
    {"id": 3, "model": "Nexon", "brand": "Tata", "type": "SUV", "price_per_day": 3000, "fuel_type": "Diesel", "is_available": False},
    {"id": 4, "model": "Model 3", "brand": "Tesla", "type": "Luxury", "price_per_day": 8000, "fuel_type": "Electric", "is_available": True},
    {"id": 5, "model": "Fortuner", "brand": "Toyota", "type": "SUV", "price_per_day": 5000, "fuel_type": "Diesel", "is_available": True},
    {"id": 6, "model": "3 Series", "brand": "BMW", "type": "Luxury", "price_per_day": 7000, "fuel_type": "Petrol", "is_available": False},
    {"id": 7, "model": "Thar", "brand": "Mahindra", "type": "SUV", "price_per_day": 3500, "fuel_type": "Petrol", "is_available": True},
    {"id": 8, "model": "E-Class", "brand": "Mercedes-Benz", "type": "Luxury", "price_per_day": 9500, "fuel_type": "Diesel", "is_available": True},
    {"id": 9, "model": "ZS EV", "brand": "MG", "type": "SUV", "price_per_day": 4000, "fuel_type": "Electric", "is_available": True},
    {"id": 10, "model": "Swift", "brand": "Maruti", "type": "Hatchback", "price_per_day": 1200, "fuel_type": "Petrol", "is_available": True}
]

rentals = []
rental_counter = 1

# Q6 , Q9 & Q11
class RentalRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    car_id: int = Field(..., gt=0)
    days: int = Field(..., ge = 0, le = 30)
    license_number: str = Field(..., min_length=8)
    insurance: bool = Field(default=False)
    driver_required: bool = Field(default=False)
    
class NewCar(BaseModel):
    model: str = Field(min_length=2)
    brand: str = Field(min_length=2)
    type: str = Field(min_length=2)
    price_per_day: int = Field(gt=0)
    fuel_type: str = Field(min_length=2)
    is_available: bool = True
    
    
# Q7 , Q9 & Q10------> Helper functions
def find_car(car_id: int):
    for car in cars:
        if car['id'] == car_id:
            return car
    return None


def calculate_rental_cost(price_per_day, days, insurance=False, driver_required=False):
    base_price = price_per_day * days
    discount = 0
    
    if days >= 15:
        discount = 0.25 * base_price
    elif days >= 7:
        discount = 0.15 * base_price
    
    insurance_cost = 500 * days if insurance else 0
    driver_cost = 800 * days if driver_required else 0
    
    total_cost = base_price - discount + insurance_cost + driver_cost
    
    return{
        'base_price': base_price,
        'discount': discount,
        'insurance_cost': insurance_cost,
        'driver_cost': driver_cost,
        'total_cost': total_cost,
    }
    
    
def filter_cars_logic(type=None, brand=None, fuel_type=None, max_price=None, is_available=None):
    result = cars
    
    if type is not None:
        result = [car for car in result if car['type'].lower() == type.lower()]
        
    if brand is not None:
        result = [car for car in result if car['brand'].lower() == brand.lower()]
        
    if fuel_type is not None:
        result = [car for car in result if car['fuel_type'].lower() == fuel_type.lower()]
        
    if max_price is not None:
        result = [car for car in result if car['price_per_day'] <= max_price]
        
    if is_available is not None:
        result = [car for car in result if car['is_available'] == is_available]
        
    return result
    


# Q1
@app.get('/')
def home():
    return {'message': 'Welcome to SpeedRide Car Rentals'}



# Q2
@app.get('/cars')
def get_all_cars():
    total = len(cars)
    
    available_cars = [car for car in cars if car['is_available'] == True]
    available_count = len(available_cars)
    
    return{
        'cars': cars,
        'total': total,
        'available_count': available_count,
    }
    
    
# Q11
@app.post('/cars', status_code=201)
def add_car(new_car: NewCar, response: Response):
    for car in cars:
        if car['model'].lower() == new_car.model.lower() and car['brand'].lower() == new_car.brand.lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'error': "Car already exists"}
        
    car_dict = new_car.model_dump()   # modern version of .dict()
    car_dict['id'] = len(cars) + 1
    cars.append(car_dict)
    return car_dict
    
    
# Q5
@app.get('/cars/summary')
def get_cars_summary():
    available = [car for car in cars if car['is_available']]
    cheapest = min(cars, key = lambda x: x['price_per_day'])
    expensive = max(cars, key = lambda x: x['price_per_day'])
    
    # creates list of types and Counter tallies them up
    type_counts = Counter(car['type'] for car in cars)
    fuel_counts = Counter(car['fuel_type'] for car in cars)
    
    return{
        'total_cars': len(cars),
        'available_count': len(available),
        'type_breakdown': type_counts,
        'fuel_type_breakdown': fuel_counts,
        'cheapest': cheapest,
        'expensive': expensive,
    }

# Q16
@app.get('/cars/search')
def search(keyword: str = Query(...)):
    result = [
        car for car in cars
        if keyword.lower() in car['model'].lower()
        or keyword.lower() in car['brand'].lower()
        or keyword.lower() in car['type'].lower()
    ]
    
    return {'results': result, 'total_found': len(result)}


# Q17
@app.get('/cars/sort')
def sort(
    sort_by: str = Query('price_per_day', description='price_per_day, brand, type'),
    order: str = Query('asc', description='asc or desc')
):
    if sort_by not in ['price_per_day', 'brand', 'type']:
        return {'error': "sort_by must be 'price_per_day', 'brand' or 'type"}
    
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    
    reverse = (order == 'desc')
    
    sorted_cars = sorted(cars, key=lambda car: car[sort_by], reverse=reverse)

    return{
        'sort_by': sort_by,
        'order': order,
        'total': len(sorted_cars),
        'cars': sorted_cars,
    }
    
    
# Q18
@app.get("/cars/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]


# Q20
@app.get("/cars/browse")
def browse(
    keyword: Optional[str] = None,
    type: Optional[str] = None,
    fuel_type: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None,
    sort_by: Optional[str] = None,
    page: int = 1,
    limit: int = 3
):
    result = cars

    if keyword:
        result = [car for car in result if keyword.lower() in car["model"].lower()]

    result = filter_cars_logic(type, None, fuel_type, max_price, is_available)

    if sort_by:
        result = sorted(result, key=lambda x: x.get(sort_by))

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": len(result),
        "page": page,
        "data": result[start:end]
    }


# Q10    ---> specific route
@app.get('/cars/filter')
def filter_cars(
    type: Optional[str] = None,
    brand: Optional[str] = None,
    fuel_type: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None,
):
    return filter_cars_logic(type, brand, fuel_type, max_price, is_available)
    
    
# Q15  (continue)
@app.get('/cars/unavailable')
def unavailable_cars():
    return [car for car in cars if not car['is_available']]
    
# Q3   ---> dynamic route
@app.get('/cars/{car_id}')
def get_car(car_id: int):
    for car in cars:
        if car['id'] == car_id:
            return {'cars': car}
    return {'error': 'Car not found.'}


# Q12
@app.put('/cars/{car_id}')
def update_car(
    car_id: int,
    price_per_day: Optional[int] = None,
    is_available: Optional[bool] = None
):
    car = find_car(car_id)
    
    if not car:
        raise HTTPException(status_code=404, detail='Car not found')
    
    if price_per_day is not None:
        car['price_per_day'] = price_per_day
        
    if is_available is not None:
        car['is_available'] = is_available
        
    return car
    
# Q13
@app.delete('/cars/{car_id}')
def delete_car(car_id: int):
    car = find_car(car_id)
    
    if not car:
        raise HTTPException(status_code=401, detail='Car not found')

    for r in rentals:
        if r['car_id'] == car_id and r['status'] == 'active':
            raise HTTPException(status_code=400, detail='Car has active rental')
        
    cars.remove(car)
    return {'message': "Car deleted"}


# Q4
@app.get('/rentals')
def get_rentals():
    return {'rentals': rentals, 'total': len(rentals)}

    
# Q8
@app.post('/rentals')
def rent_car(req: RentalRequest, response: Response):
    global rental_counter
    
    car = find_car(req.car_id)
    if not car:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': 'Car not found'}
    
    if not car['is_available']:
        return {'error': 'Car not available'}
    
    cost = calculate_rental_cost(car['price_per_day'], req.days, req.insurance, req.driver_required)
    
    car['is_available'] = False
    
    rental = {
        'rental_id': rental_counter,
        'customer_name': req.customer_name,
        'car_id': req.car_id,
        'car_model': car['model'],
        'car_brand': car['brand'],
        'days': req.days,
        'cost': cost,
        'status': 'active',
    }
    
    rentals.append(rental)
    rental_counter += 1
    
    return rental


# Q15
@app.get('/rentals/active')
def active_rentals():
    return [r for r in rentals if r['status'] == 'active']


# Q19
@app.get('/rentals/search')
def search_rentals(customer_name: str):
    
    result = [
        r for r in rentals
        if customer_name.lower() in r['customer_name'].lower()
    ]
    
    return {
        "keyword": customer_name,
        "total_found": len(result),
        "rentals": result
    }


@app.get('/rentals/sort')
def sort_rentals(
    sort_by: str = Query('total_cost', description="total_cost or days"),
    order: str = Query('asc', description="asc or desc")
):
    
    if sort_by not in ['total_cost']:
        return {'error': "sort_by must be 'total_cost'"}
    
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    
    reverse = (order == 'desc')
    
    if sort_by == 'total_cost':
        sorted_rentals = sorted(
            rentals,
            key=lambda r: r['cost']['total_cost'],
            reverse=reverse
        )
    else:
        sorted_rentals = sorted(
            rentals,
            key=lambda r: r['days'],
            reverse=reverse
        )
    
    return {
        "sorted_by": sort_by,
        "order": order,
        "total": len(sorted_rentals),
        "rentals": sorted_rentals
    }


@app.get('/rentals/page')
def paginate_rentals(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated = rentals[start:end]
    
    return {
        "page": page,
        "limit": limit,
        "total_records": len(rentals),
        "total_pages": (len(rentals) + limit - 1) // limit,
        "data": paginated
    }


# Q14
@app.post('/return/{rental_id}')
def return_rental_car(rental_id: int):
    for r in rentals:
        if r['rental_id'] == rental_id:
            r['status'] = 'returned'
            car = find_car(r['car_id'])
            car['is_available'] = True
            return r
    raise HTTPException(status_code=404, detail='Rental not found')


@app.get('/rentals/by-car/{car_id}')
def rental_history(car_id: int):
    return [r for r in rentals if r['car_id'] == car_id]


