import admin
def mainMenu():
    while True:
        print("Hall Symphony:")
        print("----------------")
        print("1) Login as Admin")
        print("2) Login as User")
        print("3) Exit Program")
        choice = input("Enter your choice: ")
        if choice == '1':
            admin.login()
        elif choice == '2':
            print("Coming Soon")
        elif choice == '3':
            print("System exited")
            exit()
        else:
            print("Invalid Choice!")
            mainMenu()

#start the program
mainMenu()
