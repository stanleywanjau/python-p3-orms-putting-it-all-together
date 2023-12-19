import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY, 
                name TEXT,
                breed TEXT
            )
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = 'DROP TABLE IF EXISTS dogs'
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            # Insert a new record
            sql = 'INSERT INTO dogs (name, breed) VALUES (?, ?)'
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            # Set the id of the instance after insertion
            self.id = CURSOR.lastrowid
        else:
            # Update an existing record
            sql = 'UPDATE dogs SET name=?, breed=? WHERE id=?'
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = 'SELECT * FROM dogs'
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = 'SELECT * FROM dogs WHERE name=? LIMIT 1'
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        sql = 'SELECT * FROM dogs WHERE id=? LIMIT 1'
        CURSOR.execute(sql, (dog_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        self.save()

# Usage example:
Dog.create_table()
Dog.drop_table()
Dog.create_table()  # Recreate the table after dropping

# Example of creating and manipulating a Dog instance:
joey = Dog("Joey", "Cocker Spaniel")
joey.save()
# joey.name = "Joseph"
# joey.update()
