from Database_Connection import Database

obj=Database()
data=obj.get_user_by_name("hansitha123@gmail.com")
print(data)
#result=obj.save_otp("hansitha123@gmail.com","123456")
#print(obj.verify_otp("hansitha123@gmail.com","123456"))
