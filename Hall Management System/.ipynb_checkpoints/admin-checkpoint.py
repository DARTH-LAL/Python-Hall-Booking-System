def login():
    while True:
        inputUN = input("Enter your username:")
        inputPwd = input("Enter you password:")
        print("Admin Login:")

        with open("users.txt") as file:
            for line in file:
                username, password = line.strip().split(':')
                if inputUN == username and inputPwd == password:
                    admin_menu()
                    return  # Exit the function after successful login
            print("Invalid login! Please try again.")

def admin_menu():
    while True:
        print("Admin Menu:")
        print("----------------")
        print("1) Enter Hall Information")
        print("2) View all the hall information")
        print("3) Search the hall information")
        print("4) Go back to main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        else:
            print("Invalid!")
            admin_menu()