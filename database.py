import sqlite3
import os
#---------------------------------------------------------------- DB
class Database:
    def __init__(self, db):
        self.__db_name = db
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS [table_menu](
                            [ID] INT PRIMARY KEY NOT NULL UNIQUE, 
                            [name] NVARCHAR(50) NOT NULL UNIQUE, 
                            [price] INT NOT NULL,
                            [is_food] BOOL NOT NULL) WITHOUT ROWID;
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS [table_reciepts](
                            [reciept_id] INT NOT NULL,
                            [menu_id] INT NOT NULL REFERENCES [table_menu]([ID]),
                            [count] INT,
                            [price] INT);
                            """)
        
        self.cursor.execute("""
                            CREATE VIEW IF NOT EXISTS view_menu_reciepts AS 
                            SELECT table_reciepts.reciept_id ,table_menu.name , table_reciepts.count,
                            table_reciepts.price, (table_reciepts.price * table_reciepts.count) AS sum 
                            FROM table_menu 
                            INNER JOIN table_reciepts ON table_menu.ID = table_reciepts.menu_id
                            """)
        self.connection.commit()
        self.connection.close()
    
    def insert(self, id, name, price, is_food):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO table_menu VALUES (? , ? , ?, ?)" , (id, name, price, is_food))
        self.connection.commit()
        self.connection.close()
    
    def get_menu_food(self, is_food):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT * FROM table_menu WHERE is_food = ?' , (is_food,))
        result = self.cursor.fetchall()
        return result
    
    def get_max_reciept(self):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT MAX(reciept_id) FROM table_reciepts")
        result = self.cursor.fetchall()
        return result 
    
    def get_menu_item_by_name(self, menu_item_name):
          self.connection = sqlite3.connect(self.__db_name)
          self.cursor = self.connection.cursor() 
          self.cursor.execute("SELECT * FROM table_menu WHERE name = ?" , (menu_item_name,))
          result = self.cursor.fetchall()
          return result 
    
    def insert_into_table_reciept(self,reciept_id,menu_id,count,price):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor() 
        self.cursor.execute('INSERT INTO table_reciepts VALUES (?,?,?,?)' , (reciept_id,menu_id,count,price))
        self.connection.commit()
        self.connection.close()
    
    def get_reciept_by_reciept_id_menu_id(self,reciept_id, menu_id):
          self.connection = sqlite3.connect(self.__db_name)
          self.cursor = self.connection.cursor() 
          self.cursor.execute("SELECT * FROM table_reciepts WHERE reciept_id = ? and menu_id = ?" , (reciept_id,menu_id))
          result = self.cursor.fetchall()
          return result 
    
    def increase_count(self,reciept_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor() 
        self.cursor.execute('UPDATE table_reciepts SET count = count + 1 WHERE reciept_id = ? and menu_id = ?' , (reciept_id,menu_id))
        self.connection.commit()
        self.connection.close()
    
    def decrease_count(self,reciept_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor() 
        self.cursor.execute('UPDATE table_reciepts SET count = count - 1 WHERE reciept_id = ? and menu_id = ? and count > 0' , (reciept_id,menu_id))
        self.cursor.execute('DELETE FROM table_reciepts WHERE reciept_id = ? and menu_id = ? and count = 0' , (reciept_id,menu_id))
        self.connection.commit()
        self.connection.close()
    

    def get_reciept_by_reciept_id(self,reciept_id):
          self.connection = sqlite3.connect(self.__db_name)
          self.cursor = self.connection.cursor() 
          self.cursor.execute("SELECT * FROM view_menu_reciepts WHERE reciept_id = ?" , (reciept_id,))
          result = self.cursor.fetchall()
          return result 
    
    def delete_reciept(self, reciept_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor() 
        self.cursor.execute("DELETE FROM table_reciepts WHERE reciept_id = ? and menu_id = ?" , (reciept_id , menu_id))
        self.connection.commit()
        self.connection.close()
#---------------------------------------------------------------- End of DB

# creating database and inserting items into database
db = None     
if not os.path.isfile("restaurant.db"):
    db = Database('restaurant.db')
    #inserting food
    db.insert(1,'Big Mac' , 6.70, True)
    db.insert(2,'Quarter Pounder with Cheese' , 7.99, True)
    db.insert(3,'Double Big Mac' , 8.19,True)
    db.insert(4,'Junior Chicken' , 3.89,True)
    db.insert(5,'Grilled Chicken Sandwich' , 7.99,True)
    db.insert(6,'20 Chicken McNuggets' , 17.29,True)
    db.insert(7,'6-Piece Chicken McNuggets' , 7.99,True)
    db.insert(8,'Filet-O-Fish' , 4.79,True)
    db.insert(9,'Chicken McNuggets (10 pcs)' , 5.89,True)
    db.insert(10,'Egg McMuffin' , 3.99,True)
    db.insert(11,'Sausage McMuffin' , 2.79,True)
    db.insert(12,'Hash Browns' , 1.99,True)
    db.insert(13,'French Fries (Medium)' ,2.99,True)
    db.insert(14,'French Fries (Large)' , 3.49,True)
    db.insert(15,'Apple Pie' , 1.49,True)
    db.insert(16,'Happy Meal' , 4.19,True)
    db.insert(17,'Baked Apple Pie' , 1.59,True)
    db.insert(18,'Creamy Parmesan & Bacon Quarter Pounder' , 10.19,True)
    db.insert(19,'Masala McShaker Fries' , 5.79,True)
    db.insert(20,'Big Mac Extra Value Meal' , 14.97,True)
    #inserting drinks
    db.insert(21,'Medium Coca-Cola' , 2.79,False)
    db.insert(22,'Medium Diet Coke' , 2.79,False)
    db.insert(23,'Medium Sprite' , 2.79,False)
    db.insert(24,"Medium Barq's Root Beer" , 2.79,False)
    db.insert(25,'Medium NESTEA Iced Tea' , 2.79,False)
    db.insert(26,'Medium Fruitopia Strawberry' , 2.79,False)
    db.insert(27,'Medium Coke Zero' , 2.79,False)
    db.insert(28,'Medium Iced Coffee' , 3.19,False)
    db.insert(29,'Medium Vanilla Iced Coffee' , 3.59,False)
    db.insert(30,'Medium Caramel Iced Coffee' , 3.59,False)
    db.insert(31,'Medium Chocolate Triple Thick Milkshake' , 4.59,False)
    db.insert(32,'Medium Vanilla Triple Thick Milkshake' , 4.59,False)
    db.insert(33,'Medium Mango Pineapple Real Fruit Smoothie' , 4.39,False)
    db.insert(34,'Medium Strawberry Banana Smoothie' , 4.39,False)
    db.insert(35,'Medium Peach Mango Fruit Splash' , 3.19,False)
    db.insert(36,'Chocolate Milk Bottle' , 1.79,False)
    db.insert(37,'Medium Premium Roast Coffee' , 2.19,False)
    db.insert(38,'Medium Decaf Coffee' , 2.19,False)
    db.insert(39,'Medium Latte (2% Milk)' , 4.19,False)
    db.insert(40,'Medium French Vanilla Latte (2% Milk)' , 4.79,False)
    db.insert(41,'Medium Caramel Latte (2% Milk)' , 4.79,False)
    db.insert(42,'Medium Latte with Sugar-Free Syrup (2% Milk)' , 4.79,False)
    db.insert(43,'Medium Cappuccino (2% Milk)' , 4.19,False)
    db.insert(44,'Medium Mocha (2% Milk)' , 4.59,False)
    db.insert(45,'Medium Hot Chocolate (2% Milk)' , 2.79,False)
    db.insert(46,'Double Espresso' ,2.39,False)
    db.insert(47,'Espresso' ,1.79,False)
    db.insert(48,'Long Espresso' ,1.79,False)
    db.insert(49,'Medium Orange Pekoe Tea' ,2.19,False)
    db.insert(50,'Medium Earl Grey Tea' ,2.19,False)
    db.insert(51,'Medium Green Tea' ,2.19,False)
    db.insert(52,'Medium Peppermint Tea' ,2.19,False)
else:
    db = Database('restaurant.db')