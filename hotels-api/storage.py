hotels: list[dict] = [
    {
        "id": 1,
        "name": "Grand Hotel",
        "stars": 5,
        "location": "Paris",
    },
    {
        "id": 2,
        "name": "City Inn",
        "stars": 3,
        "location": "Berlin",
    },
]

rooms: list[dict] = [
    {
        "id": 1,
        "hotel_id": 1,
        "name": "Standard Double",
        "capacity": 2,
        "price_per_night": 150.0,
    },
    {
        "id": 2,
        "hotel_id": 1,
        "name": "Deluxe Suite",
        "capacity": 3,
        "price_per_night": 300.0,
    },
    {
        "id": 3,
        "hotel_id": 2,
        "name": "Single Room",
        "capacity": 1,
        "price_per_night": 80.0,
    },
]

next_hotel_id = 3
next_room_id = 4