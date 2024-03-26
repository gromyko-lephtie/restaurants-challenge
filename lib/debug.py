from __init__ import CONN, CURSOR
from restaurant import Restaurant
from customer import Customer
from review import Review
#import ipdb


def reset_database():
    Review.drop_table()
    Customer.drop_table()
    Restaurant.drop_table()
    Restaurant.create_table()
    Customer.create_table()
    Review.create_table()

    # Create seed data
    Sankara = Restaurant.create("Sankara", 100)
    lakeview = Restaurant.create("lakeview", 20)
    customer1 = Customer.create("Salt", "Bae")
    customer2 = Customer.create("Bee", "Bee")
    review1 = Review.create(1, 1, 3)
    review2 = Review.create(1, 2, 4)
    review3 = Review.create(2, 2, 5)

    # Review customer()
    associated_customer = review1.customer()
    if associated_customer:
        print("Customer associated with the review:", associated_customer)
    else:
        print("No customer found for the review.")

    # Review restaurant()
    associated_restaurant = review2.restaurant()
    if associated_restaurant:
        print("Restaurant associated with the review:", associated_restaurant)
    else:
        print("No restaurant found for the review.")

    # Restaurant reviews()
    reviews_for_Sankara = Sankara.reviews()
    if reviews_for_Sankara:
        print("Sankara reviews:", reviews_for_Sankara)
    else:
        print("No reviews found for the Sankara.")

    # Restaurant customers()
    lakeview_customers = lakeview_customers.customers()
    if lakeview_customers:
        print("lakeview customers:", lakeview_customers)
    else:
        print("No customers found lakeview.")

    #Customer reviews()
    customer1_reviews = customer1.reviews()
    if customer1_reviews:
        print("Customer 1 reviews:", customer1_reviews)
    else:
        print("No reviews by customer 1.")
    
    # Customer restaurants()
    customer2_restaurants = customer2.restaurants()
    if customer2_restaurants:
        print("Customer 2 restaurants reviewed:", customer2_restaurants)
    else:
        print("No restaurants reviewed by customer 2.")

    #Customer full_name()
    customer1_full_name = customer1.full_name()
    print(f"Full name: {customer1_full_name}")
    
    # Customer favorite_restaurant()
    customer2_fav_restaurant = customer2.favorite_restaurant()
    print(f"Favorite restaurant: {customer2_fav_restaurant}")

    # Customer add_review(restaurant, rating)
    customer1_add_review =customer1.add_review(lakeview, 5)
    print(f"Added Review: {customer1_add_review}. Total Reviews: {customer1.reviews()}")

    # Delete reviews for restaurant named 'Sankara'
    customer2_delete_review = customer2.delete_reviews('Sankara')
    print(f"Deleted reviews. Current reviews: {customer2.reviews()}")

    # Review full_review()
    review3_full = review3.full_review()
    print(review3_full)

    # Restaurant fanciest()
    fanciest = Restaurant.fanciest()
    print(fanciest)

    # Restaurant all_reviews()
    all_reviews_for_lakeview = lakeview.all_reviews()
    if all_reviews_for_lakeview:
        print("All lakeview reviews:", all_reviews_for_lakeview)
    else:
        print("No reviews found for the lakeview.")
    


reset_database()
ipdb.set_trace()