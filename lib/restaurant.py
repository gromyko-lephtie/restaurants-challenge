# lib/restaurant.py

from __init__ import CURSOR, CONN



class Restaurant:
    
    all = {}

    def __init__(self, name, price, id=None):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}, {self.price}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if isinstance(price, int):
            self._price = price
        else:
            raise ValueError(
                "Price must be an integer."
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Restaurant instances """
        sql = """
            CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Restaurant instances """
        sql = """
            DROP TABLE IF EXISTS restaurants;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Restuarant instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO restaurants (name, price)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.price))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, price):
        """ Initialize a new Restaurant instance and save the object to the database """
        restaurant = cls(name, price)
        restaurant.save()
        return restaurant
    
    def reviews(self):
        """Returns a collection of all the reviews for this restaurant."""
        sql = """
            SELECT * FROM reviews
            WHERE restaurant_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        results = CURSOR.fetchall()

        from review import Review
        reviews = []
        for result in results:
            review_id, restaurant_id, customer_id, star_rating = result
            review = Review(restaurant_id, customer_id, star_rating, review_id)
            reviews.append(review)

        return reviews
    
    def customers(self):
        """Returns a collection of all the customers who reviewed the restaurant."""
        customers = []

        sql = """
            SELECT c.*
            FROM customers c
            JOIN reviews rv ON c.id = rv.customer_id
            WHERE rv.restaurant_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        results = CURSOR.fetchall()

        from customer import Customer
        for result in results:
            customer_id, first_name, last_name = result
            customers.append(Customer(first_name, last_name, customer_id))

        return customers
    
    @classmethod
    def find_by_id(cls, restaurant_id):
        """Find a restaurant by its ID."""
        sql = """
            SELECT * FROM restaurants
            WHERE id = ?
        """
        CURSOR.execute(sql, (restaurant_id,))
        result = CURSOR.fetchone()

        if result:
            restaurant_id, name, price = result
            return cls(name, price, restaurant_id)
        else:
            return None
        
    @classmethod
    def fanciest(cls):
        """Return the restaurant instance with the highest price."""
        sql = """
            SELECT * FROM restaurants
            ORDER BY price DESC
            LIMIT 1
        """
        CURSOR.execute(sql)
        result = CURSOR.fetchone()

        if result:
            restaurant_id, name, price = result
            return cls(name, price, restaurant_id)
        else:
            return None
        
    def all_reviews(self):
        """Return a list of strings with all the reviews for this restaurant."""
        sql = """
            SELECT r.name, c.first_name, c.last_name, rv.star_rating
            FROM reviews rv
            JOIN customers c ON rv.customer_id = c.id
            JOIN restaurants r ON rv.restaurant_id = r.id
            WHERE rv.restaurant_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        results = CURSOR.fetchall()

        reviews = []
        for result in results:
            restaurant_name, first_name, last_name, star_rating = result
            full_name = f"{first_name} {last_name}"
            review_str = f"Review for {restaurant_name} by {full_name}: {star_rating} stars."
            reviews.append(review_str)

        return reviews

 