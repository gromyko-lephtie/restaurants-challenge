# lib/customer.py

from __init__ import CURSOR, CONN


class Customer:
    
    all = {}

    def __init__(self, first_name, last_name, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"<Customer {self.id}: {self.first_name}, {self.last_name}>"

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str) and len(first_name):
            self._first_name = first_name
        else:
            raise ValueError(
                "First name must be a non-empty string"
            )

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):  # Corrected method name to 'last_name'
        if isinstance(last_name, str) and len(last_name):
            self._last_name = last_name
        else:
            raise ValueError(
                "Last name must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Customer instances """
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Customer instances """
        sql = """
            DROP TABLE IF EXISTS customers;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Customer instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO customers (first_name, last_name)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.first_name, self.last_name))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, first_name, last_name):
        """ Initialize a new Customer instance and save the object to the database """
        customer = cls(first_name, last_name)
        customer.save()
        return customer
    
    def restaurants(self):
        """Returns a collection of all the restaurants that the customer has reviewed."""

        sql = """
            SELECT r.*
            FROM restaurants r
            JOIN reviews rv ON r.id = rv.restaurant_id
            WHERE rv.customer_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        results = CURSOR.fetchall()

        from restaurant import Restaurant
        restaurants = []
        for result in results:
            restaurant_id, name, price = result
            restaurants.append(Restaurant(name, price, restaurant_id))

        return restaurants
    
    def reviews(self):
        """Returns a collection of all the reviews left by the Customer."""
        sql = """
            SELECT *
            FROM reviews
            WHERE customer_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        results = CURSOR.fetchall()

        reviews = []

        from review import Review
        for result in results:
            review_id, restaurant_id, customer_id, star_rating = result
            review = Review(restaurant_id, customer_id, star_rating, review_id)
            reviews.append(review)

        return reviews
    
    def full_name(self):
        """Returns the full name of the customer, Western style."""
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        """Returns the restaurant instance with the highest star rating from this customer."""
        highest_rating = 0
        favorite_restaurant = None

        for review in self.reviews():
            if review.star_rating > highest_rating:
                highest_rating = review.star_rating
                favorite_restaurant = review.restaurant()

        return favorite_restaurant
    

    def add_review(self, restaurant, rating):
        """Creates a new review for the restaurant with the given restaurant_id."""
        
        from restaurant import  Restaurant
        if not isinstance(restaurant, Restaurant):
            raise ValueError("The 'restaurant' parameter must be an instance of the Restaurant class.")

        from review import Review
        new_review = Review.create(restaurant.id, self.id, rating)
        
        return new_review


    def delete_reviews(self, restaurant):
        """Removes all reviews for the given restaurant."""
        
        from restaurant import Restaurant
        if not isinstance(restaurant, Restaurant):
            raise ValueError("The 'restaurant' parameter must be an instance of the Restaurant class.")
        
        sql = """
            DELETE FROM reviews
            WHERE restaurant_id = ? AND customer_id = ?
        """
        
        CURSOR.execute(sql, (restaurant.id, self.id))
        CONN.commit()

    @classmethod
    def find_by_id(cls, customer_id):
        """Find a customer by their ID."""
        sql = """
            SELECT * FROM customers
            WHERE id = ?
        """
        CURSOR.execute(sql, (customer_id,))
        result = CURSOR.fetchone()

        if result:
            customer_id, first_name, last_name = result
            return cls(first_name, last_name, customer_id)
        else:
            return None