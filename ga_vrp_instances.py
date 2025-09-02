#An example of a small instance, will be used as one of the instances in the smallgroup
SMALL_INSTANCE_1 = {
    "DEPOT": (50, 50),
    "CUSTOMERS": {
        0: (23, 45),
        1: (55, 60),
        2: (42, 31),
        3: (67, 75),
        4: (33, 20),
        5: (59, 39),
        6: (78, 52),
        7: (46, 70),
        8: (39, 58),
        9: (25, 32),
        10: (68, 61),
        11: (49, 26)
    },
    "VEHICLES": 3
}

#An example of the medium instances, will be part of the medium group
MEDIUM_INSTANCE_1 = {
    "DEPOT": (50, 50),
    "CUSTOMERS": {i: (random.randint(10, 90), random.randint(10, 90)) for i in range(25)}, #here "CUSTOMERS" is the key and the values are randomly generated between 10-90
    "VEHICLES": 15

}

#accessing the CUSTOMERS dictionary from the instance
CUSTOMERS = MEDIUM_INSTANCE_1["CUSTOMERS"]

# Printing all customers and their randomly generated coordinates
for customer_id, coords in CUSTOMERS.items():
    print(f"Customer {customer_id}: Location {coords}")


#An example of a large instance
#We can make the large instances just like 
# the medium ones and only need to change the iputs