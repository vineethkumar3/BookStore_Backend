from Database_Connection import Database

obj=Database()
data=obj.get_user_by_name("hansitha123@gmail.com")
print(data)
print(obj.get_all_employees())
print(obj.get_all_user_cart())