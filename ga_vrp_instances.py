import math
import random

SMALL_INSTANCE_1 = {
    "DEPOT": (50, 50),
    "CUSTOMERS": {i: (random.randint(10, 90), random.randint(10, 90)) for i in range(20)},
    "VEHICLES": random.randint(2, 10)
}

#accessing the CUSTOMERS dictionary from the instance
CUSTOMERS = SMALL_INSTANCE_1["CUSTOMERS"]
vehiclesM = SMALL_INSTANCE_1["VEHICLES"]

# Printing all customers and their randomly generated coordinates FOR THE SMALL_INSTANCE
for customer_id, coords in CUSTOMERS.items():
    print(f"Customer {customer_id}: Location {coords}")

#print(f"VEHICLES: {random.randint(2, 10)}")
print(f"Vehicles for the SMALL_INSTANCE {vehiclesM}")

#An example of the medium instances, will be part of the medium group
MEDIUM_INSTANCE_1 = {
    "DEPOT": (50, 50),
    "CUSTOMERS": {i: (random.randint(10, 90), random.randint(10, 90)) for i in range(30)}, #here "CUSTOMERS" is the key and the values are randomly generated between 10-90
    "VEHICLES": random.randint(11, 25)

}

#accessing the CUSTOMERS dictionary from the instance
CUSTOMERS = MEDIUM_INSTANCE_1["CUSTOMERS"]
vehiclesM = MEDIUM_INSTANCE_1["VEHICLES"]

# Printing all customers and their randomly generated coordinates FOR THE MEDIUM_INSTANCE
for customer_id, coords in CUSTOMERS.items():
    print(f"Customer {customer_id}: Location {coords}")


#print(f"VEHICLES: {random.randint(2, 10)}")
print(f"Vehicles for the MEDIUM_INSTANCE {vehiclesM}")

#An example of a large instance
LARGE_INSTANCE_1 = {
    "DEPOT": (50, 50),
    "CUSTOMERS": {i: (random.randint(10, 90), random.randint(10, 90)) for i in range(40)}, #here "CUSTOMERS" is the key and the values are randomly generated between 10-90
    "VEHICLES": random.randint(25, 50)

}

#accessing the CUSTOMERS dictionary from the instance
CUSTOMERS = LARGE_INSTANCE_1["CUSTOMERS"]
vehiclesL = LARGE_INSTANCE_1["VEHICLES"]

# Printing all customers and their randomly generated coordinates FOR THE LARGE_INSTANCE
for customer_id, coords in CUSTOMERS.items():
    print(f"Customer {customer_id}: Location {coords}")


#print(f"VEHICLES: {random.randint(2, 10)}")
print(f"Vehicles for the LARGE_INSTANCE {vehiclesL}")



