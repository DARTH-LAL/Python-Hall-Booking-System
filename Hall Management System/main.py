import datetime
from datetime import datetime, timedelta
import re


def mainMenu():
    while True:
        print("\nWelcome to The Hall Symphony Booking System!\n")
        print("-------------------------------------------\n")
        print(" Please select your preferred login - \n ")
        print("1. Login as Admin\n")
        print("2. Login as User\n")
        print("3. Exit Program\n")
        choice = input("Enter your choice:\n ")
        if choice == '1':
            admin_login()
        elif choice == '2':
            user_login()
        elif choice == '3':
            print("System exited , Goodbye :)\n")
            exit()

        else:
            print("Invalid Choice!\n")
            
def check_admin_credentials(username, password):
        with open("admin.txt", "r") as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    saved_username, saved_password = parts[0], parts[1]
                    if saved_username == username and saved_password == password:
                        return True
        return False

def admin_login():
    while True:
        choice = input("\nEnter 'c' to continue or 'b' to go back to the main menu: ")

        if choice == 'c':
            inputUN = input("\nEnter your username:\n ")
            inputPwd = input("\nEnter your password:\n ")

            if check_admin_credentials(inputUN, inputPwd):
                admin_menu(inputUN)
                break
            else:
                print("\nInvalid login! Please try again.\n")
        elif choice == 'b':
            mainMenu() 
            break
        else:
            print("\nInvalid choice! Please try again.\n")

def admin_menu(inputUN):
    while True:
        print(f"\nWelcome to the Admin Menu , {inputUN}!\n ")
        print("---------------------------------------\n")
        print("Please select your preferred menu - \n ")
        print("1. Hall Management Menu\n")
        print("2. Booking Management Menu\n")
        print("3. User Management Menu\n")
        print("4. Logout\n")
        choice = input("Enter your choice:\n ")
        if choice == '1':
             hall_management_menu((inputUN))
        elif choice == '2':
            booking_management_menu((inputUN))
        elif choice == '3':
            user_management_menu((inputUN))
        else:
            logout(inputUN)
            break


def hall_management_menu(inputUN):
    while True:
        print(f"\nWelcome to the Hall Management Menu, , {inputUN}!\n")
        print("-------------------------------------------------\n")
        print("1. Enter Hall Information\n")
        print("2. View all the hall information\n")
        print("3. Search the hall information\n")
        print("4. Edit the Hall Information\n")
        print("5. Delete the Hall Information\n")
        print("6. Return to Main Menu\n")
        choice = input("Enter your choice:\n ")
        if choice == '1':
            enter_hall_info()
        elif choice == '2':
            view_all_hall_info()
        elif choice == '3':
            search_hall_info()
        elif choice == '4':
            edit_hall_info()
        elif choice == '5':
            delete_hall_info()
        else:
            admin_menu(inputUN)
            break
            
def is_valid_number(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def is_valid_date(hall_availability_status):
    parts = hall_availability_status.split('-')
    
    if len(parts) == 3:
        year, month, day = parts
        
        if (year.isdigit() and month.isdigit() and day.isdigit() and
            1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            
            passed_date = datetime(int(year), int(month), int(day))
            current_datetime = datetime.now()
        
            current_date = datetime(current_datetime.year, current_datetime.month, current_datetime.day)
            
            if passed_date >= current_date:
                return True
    
    return False

def enter_hall_info():
    existing_halls = set()
    with open("halls.txt", "r") as file:
            for line in file:
                hall_info = line.strip().split('|')
                if len(hall_info) >= 2:
                    hall_id, hall_name = hall_info[:2]
                    existing_halls.add(hall_id)
                    existing_halls.add(hall_name)
       

    while True:
        hall_id = input("\nEnter Hall ID: ")
        if hall_id in existing_halls:
                print("\nHall ID already exists. Please enter a unique Hall ID.")
        else:
            break

    while True:
        hall_name = input("\nEnter Hall Name: ")
        if hall_name in existing_halls:
            print("\nHall Name already exists. Please enter a unique Hall Name.")
        else:
            break
    hall_description = input("\nEnter Hall Description: ")

    hall_pax = input("\nEnter Hall Capacity (Numeric): ")
    while not is_valid_number(hall_pax):
        print("\nInvalid Hall Pax. Please enter a numeric value.")
        hall_pax = input("\nEnter Hall Capacity (Numeric): ")

    while True:
        hall_available_date = input("\nEnter Hall Availability Status (YYYY-MM-DD): ")
        if is_valid_date(hall_available_date) == True:
            print ("correct date")
            break
        else:
            print("\nInvalid date format or date cannot be in the past.")
    
    while True:
        hall_available_time = input("\nEnter Hall Available Time (HH:MM): ")
        if valid_hall_book_time(hall_available_time):
            print("Correct time")
            break
        else:
            print("\nInvalid time format or hall can only be booked between 8am and 6pm")

    price_per_hour = input("\nEnter Price(RM) per hour (Numeric):\n")
    while not is_valid_number(price_per_hour):
        print("\nInvalid rate. Please enter a numeric value.")
        price_per_hour = input("\nEnter Price per hour (Numeric):\n")
        print("------------------------------------------------\n")

    new_hall_info = [hall_id, hall_name, hall_description, hall_pax, hall_available_date,hall_available_time, price_per_hour]

    with open("halls.txt", "a") as file:
        file.write('|'.join(new_hall_info) + '\n')
        print("\nAdding Hall information....\n")
        print("Hall information added successfully\n")

def view_all_hall_info():
        with open("halls.txt", "r") as file:
            halls = file.readlines()

            if not halls:
                print("\nNo hall information available\n")
                return

            print("\nAll Hall Information -\n")
            for hall in halls:
                details = hall.strip().split('|') 
                if len(details) >= 6: 
                    print(f"Hall ID: {details[0]}")
                    print(f"Hall Name: {details[1]}")
                    print(f"Hall Description: {details[2]}")
                    print(f"Hall Capacity: {details[3]}")
                    print(f"Hall Availability Date: {details[4]}")
                    print(f"Hall Availability Time: {details[5]}")
                    print(f"Price(RM) per hour: {details[6]}\n")
                    print("----------------------------------\n")
                else:
                    print("Invalid hall format detected.\n")

def search_hall_info():
    hall_name = input("\nEnter the name of the hall to search:\n").lower()
    found = False
    print("")
    print("Searching Hall Information...\n")

    with open("halls.txt", "r") as file:
            for line in file:
                if hall_name in line.lower():
                    print("Hall Found")
                    print("\nHall Information - \n")
                    details = line.strip().split('|') 
                    if len(details) >= 6:  
                        print(f"Hall ID: {details[0]}")
                        print(f"Hall Name: {details[1]}")
                        print(f"Hall Description: {details[2]}")
                        print(f"Hall Capacity: {details[3]}")
                        print(f"Hall Availability Date: {details[4]}")
                        print(f"Hall Availability Time: {details[5]}")
                        print(f"Price(RM) per hour: {details[6]}\n")
                        print("----------------------------------\n")
                    else:
                        print("Invalid hall format detected.\n")
                    found = True
                    break

    if not found:
            print("Hall not found\n")
            print("Please check the hall name is correct\n")

def edit_hall_info():
     hall_name = input("\nEnter the name of the hall to edit:\n").lower()
     updated_info = False

     print("\nSearching for hall information...\n")

     with open("halls.txt", "r") as file:
        halls = [line.strip().split('|') for line in file]

     for hall in halls:
        if hall[1].lower() == hall_name:
            print("Hall found")
            print("\nHall Information -\n ")
            print("Hall ID:", hall[0])
            print("Hall Name:", hall[1])
            print("Hall Description:", hall[2])
            print("Hall Capacity:", hall[3])
            print("Hall Availability Date:", hall[4])
            print("Hall Availability Time:", hall[5])
            print("Price (RM) per hour:", hall[6])
            print("\n------------------------------\n")
            original_info = hall.copy() 
            
            while True:
                print("\nSelect which information to edit - \n")
                print("1. Hall ID")
                print("2. Hall Name")
                print("3. Hall Description")
                print("4. Hall Capacity")
                print("5. Hall Availability Date (YYYY-MM-DD)")
                print("6. Hall Availability Time (HH:MM)")
                print("7. Price (RM) per hour")
                print("8. Exit\n")
                choice = input("Enter your choice (1-8):\n")
                
                if choice == '1':
                    new_hall_id = input("\nEnter new Hall ID:\n")
                    if any(hall_data[0] == new_hall_id for hall_data in halls):
                        print("\nHall ID already exists. Please enter a unique Hall ID\n")
                    else:
                        hall[0] = new_hall_id
                elif choice == '2':
                    new_hall_name = input("\nEnter new Hall Name:\n")
                    if any(hall_data[1].lower() == new_hall_name.lower() for hall_data in halls):
                        print("\nHall Name already exists. Please enter a unique Hall Name\n")
                    else:
                        hall[1] = new_hall_name
                elif choice == '3':
                    hall[2] = input("\nEnter new Description:\n")
                elif choice == '4':
                    while True:
                        hall_capacity = input("\nEnter new Capacity:\n")
                        if is_valid_number(hall_capacity):
                            hall[3] = hall_capacity
                            break
                        else:
                            print("\nInvalid Capacity. Please enter a numeric value\n")
                elif choice == '5':
                    while True:
                        hall_available_date = input("\nEnter new Availability Date (YYYY-MM-DD):\n")
                        if is_valid_date(hall_available_date):
                            hall[4] = hall_available_date
                            break
                        else:
                            print("\nInvalid date format. Please use YYYY-MM-DD format\n")
                elif choice == '6':
                    while True:
                        hall_available_time = input("\nEnter new Availability Time (HH:MM):\n")
                        if valid_hall_book_time(hall_available_time):
                            hall[5] = hall_available_time
                            break
                        else:
                            print("\nInvalid time format. Please use HH:MM format\n")
                elif choice == '7':
                    while True:
                        price_per_hour = input("\nEnter new price (RM) per Hour:\n")
                        if is_valid_number(price_per_hour):
                            hall[6] = price_per_hour
                            break
                        else:
                            print("\nInvalid rate. Please enter a numeric value\n")
                elif choice == '8':
                    updated_info = True
                    break
                else:
                    print("\nInvalid choice. Please enter a valid option (1-8)\n")

            if updated_info:
                print("\nUpdated hall information -\n")
                print("Hall ID:", hall[0])
                print("Hall Name:", hall[1])
                print("Hall Description:", hall[2])
                print("Hall Capacity:", hall[3])
                print("Hall Availability Date:", hall[4])
                print("Hall Availability Time:", hall[5])
                print("Price (RM) per hour:", hall[6])
                print("\n----------------------\n")
                confirm = input("Do you want to confirm the changes? (y/n):\n")
                
                if confirm.lower() == 'y':
                    with open("halls.txt", "w") as file:
                        for hall_data in halls:
                            file.write('|'.join(hall_data) + '\n')
                    print("\nEditing hall information...\n")
                    print("Hall information updated successfully\n")
                else:
                    halls[halls.index(hall)] = original_info  
                    print("\nDiscarding changes....")
                    print("\nChanges discarded")
            break

     if not updated_info:
        print("\nHall not found. Please check the hall name is correct\n")


def delete_hall_info():
    hall_name = input("\nEnter the ID or name of the hall to delete:\n ").lower()
    hall_found = False

    print("\nSearching for hall information...\n")

    with open("halls.txt", "r") as file:
        halls = [line.strip().split('|') for line in file]

    for hall in halls:
        if hall[0].lower() == hall_name or hall[1].lower() == hall_name:
            hall_found = True
            print("Hall found\n")
            print("Hall Information -\n")
            print("Hall ID:", hall[0])
            print("Hall Name:", hall[1])
            print("Hall Description:", hall[2])
            print("Hall Capacity:", hall[3])
            print("Hall Availability Date:", hall[4])
            print("Hall Availability Time:", hall[5])
            print("Price (RM) per hour:", hall[6])
            print("\n----------------------------\n")

            confirm = input("\nDo you want to delete this hall? (y/n):\n")
            
            if confirm.lower() == 'y':
                halls.remove(hall)
                with open("halls.txt", "w") as file:
                    for hall_data in halls:
                        file.write('|'.join(hall_data) + '\n')
                print("\nDeleting hall information...\n")
                print("Hall information deleted successfully\n")
            else:
                print("\nDeletion canceled\n")
                break

    if not hall_found:
        print("\nHall not found")
        print("\nPlease check the hall ID or name is correct\n")

def booking_management_menu(inputUN):
        while True: 
         print(f"\nWelcome to the Booking Management Menu,{inputUN}!\n")
         print("------------------------------------------------\n")
         print("1. View all hall booking information\n")
         print("2. Search the booking information\n")
         print("3. Edit the booking Information\n")
         print("4. Delete the Hall Information\n")
         print("5. Return to Main Menu\n")
         choice = input("Enter your choice:\n ")
         if choice == '1':
            view_all_bookings()
         elif choice == '2':
            search_booking_info(inputUN)
         elif choice == '3':
            edit_booking_info()
         elif choice == '4':
            delete_booking_info()
         else:
            admin_menu(inputUN)
            break
         
def view_all_bookings():
        with open("bookings.txt", "r") as file:
            halls = file.readlines()

            if not halls:
                print("\nNo hall booking information available at the moment\n")
                return

            print("\nAll Hall Booking Information - \n")
            for hall in halls:
                details = hall.strip().split('|') 
                if len(details) >= 9 : 
                    print(f"Username: {details[0]}")
                    print(f"Hall ID: {details[1]}")
                    print(f"Booking Date: {details[2]}")
                    print(f"Booking Time: {details[3]}")
                    print(f"Number of Hours of Booking: {details[4]}")
                    print(f"Price(RM): {details[5]}")
                    print(f"Event Name: {details[6]}")
                    print(f"Event Description: {details[7]}")
                    print(f"Number of People: {details[8]}\n")
                    print("---------------------------------\n")
                else:
                    print("Invalid hall format detected.\n")

def search_booking_info(inputUN):
    inputUN = input("\nEnter the username to search for booking information:\n ")
    search_term = inputUN.lower()

    print(f"\nSearching Booking Information for {inputUN}....\n")
    found = False

    with open("bookings.txt", "r") as file:
        for line in file:
            details = line.strip().split('|')
            if search_term == details[0].lower():
                if not found:
                    print(f"All bookings for {inputUN} - \n")
                    found = True
                print(f"Hall ID: {details[1]}")
                print(f"Booking Date: {details[2]}")
                print(f"Booking Time: {details[3]}")
                print(f"Number of Hours of Booking: {details[4]}")
                print(f"Price (RM): {details[5]}")
                print(f"Event Name: {details[6]}")
                print(f"Event Description: {details[7]}")
                print(f"Number of People: {details[8]}\n")
                print("---------------------------------\n")

    if not found:
        print(f"No booking information found for {inputUN}.\n")

def edit_booking_info():
    username = input("\nEnter the username of the booking to edit:\n ")
    found_bookings = []

    print("\nSearching for booking information...\n")

    with open("bookings.txt", "r") as file:
        bookings = [line.strip().split('|') for line in file]

    for booking in bookings:
        if username == booking[0]:
            found_bookings.append(booking)

    if not found_bookings:
        print("\nNo booking information found for the provided username.\n")
        return

    print(f"All bookings for {username} - \n")
    for i, booking in enumerate(found_bookings, start=1):
        print(f"Booking {i} -\n")
        print(f"Username: {booking[0]}")
        print(f"Hall ID: {booking[1]}")
        print(f"Booking Date: {booking[2]}")
        print(f"Booking Time: {booking[3]}")
        print(f"Number of Hours of Booking: {booking[4]}")
        print(f"Price (RM): {booking[5]}")
        print(f"Event Name: {booking[6]}")
        print(f"Event Description: {booking[7]}")
        print(f"Number of People: {booking[8]}")
        print("\n--------------------------------\n")

    while True:
        choice = input("\nEnter the number of the booking to edit (or 'c' to cancel):\n")
        if choice == 'c':
            print("\nEditing canceled\n")
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(found_bookings):
            selected_booking = found_bookings[int(choice) - 1]
            print("\nSelected booking information -\n")
            print(f"Username: {selected_booking[0]}")
            print(f"Hall ID: {selected_booking[1]}")
            print(f"Booking Date: {selected_booking[2]}")
            print(f"Booking Time: {selected_booking[3]}")
            print(f"Number of Hours of Booking: {selected_booking[4]}")
            print(f"Price (RM): {selected_booking[5]}")
            print(f"Event Name: {selected_booking[6]}")
            print(f"Event Description: {selected_booking[7]}")
            print(f"Number of People: {selected_booking[8]}")
            print("\n---------------------------------------\n")

            while True:
                print("\nSelect which information to edit - \n")
                print("1. Hall ID")
                print("2. Booking Date (YYYY-MM-DD)")
                print("3. Booking Time (HH:MM)")
                print("4. Number of Hours of Booking")
                print("5. Price (RM)")
                print("6. Event Name")
                print("7. Event Description")
                print("8. Number of People")
                print("9. Exit")
                edit_choice = input("\nEnter your choice (1-9):\n")

                if edit_choice == '1':
                    new_hall_id = input("\nEnter new Hall ID:\n")
                    is_hall_id_unique = new_hall_id not in (booking[1] for booking in found_bookings) and new_hall_id not in (hall[0] for hall in found_bookings)
                    if is_hall_id_unique:
                        selected_booking[1] = new_hall_id
                        print("\nHall ID updated successfully.")
                    else:
                        print("\nHall ID already exists. Please enter a unique Hall ID.")
                elif edit_choice == '2':
                    new_booking_date = input("\nEnter new Booking Date (YYYY-MM-DD):\n")
                    if is_valid_date(new_booking_date):
                        selected_booking[2] = new_booking_date
                    else:
                        print("\nInvalid date format or booking date can not be in the past. Please enter a valid date (YYYY-MM-DD).")
                elif edit_choice == '3':
                    new_booking_time = input("\nEnter new Booking Time (HH:MM):\n")
                    if valid_hall_book_time(new_booking_time):
                        selected_booking[3] = new_booking_time
                    else:
                        print("\nInvalid time format or hall can only be booked between 8am and 6pm.")
                elif edit_choice == '4':
                    new_hours = input("\nEnter new Number of Hours of Booking:\n")
                    if is_valid_number(new_hours):
                        selected_booking[4] = new_hours
                    else:
                        print("\nInvalid number of hours. Please enter a numeric value.")
                elif edit_choice == '5':
                    new_price = input("Enter new Price (RM):\n")
                    if is_valid_number(new_price):
                        selected_booking[5] = new_price
                    else:
                        print("\nInvalid price format. Please enter a numeric value.")
                elif edit_choice == '6':
                    new_event_name = input("\nEnter new Event Name:\n")
                    selected_booking[6] = new_event_name
                elif edit_choice == '7':
                    new_event_desc = input("\nEnter new Event Description:\n")
                    selected_booking[7] = new_event_desc
                elif edit_choice == '8':
                    new_people = input("\nEnter new Number of People:\n")
                    if is_valid_number(new_people):
                        selected_booking[8] = new_people
                    else:
                        print("\nInvalid number of people. Please enter a numeric value.")
                elif edit_choice == '9':
                    print("\nUpdated booking information -\n")
                    print(f"Username: {selected_booking[0]}")
                    print(f"Hall ID: {selected_booking[1]}")
                    print(f"Booking Date: {selected_booking[2]}")
                    print(f"Booking Time: {selected_booking[3]}")
                    print(f"Number of Hours of Booking: {selected_booking[4]}")
                    print(f"Price (RM): {selected_booking[5]}")
                    print(f"Event Name: {selected_booking[6]}")
                    print(f"Event Description: {selected_booking[7]}")
                    print(f"Number of People: {selected_booking[8]}\n")

                    confirm = input("Do you want to confirm the changes? (y/n):\n")
                    if confirm.lower() == 'y':
                        with open("bookings.txt", "w") as file:
                            for booking_data in bookings:
                                file.write('|'.join(booking_data) + '\n')
                        print("\nEditing booking information...\n")
                        print("Booking information updated successfully\n")
                    else:
                        print("\nChanges discarded.")
                    return

                else:
                    print("\nInvalid choice. Please enter a valid option (1-9).")
        else:
            print("\nInvalid choice. Please enter a valid number.")

        if not found_bookings:
            print("\nNo booking information found for the provided username.\n")


def delete_booking_info():
    username = input("Enter the username of the booking to delete:\n")
    found_bookings = []

    print("\nSearching Booking Information....\n")

    with open("bookings.txt", "r") as file:
        bookings = [line.strip().split('|') for line in file]

    for booking in bookings:
        if username == booking[0]:
            found_bookings.append(booking)

    if not found_bookings:
        print("No booking information found for the provided username.\n")
        return

    print(f"All bookings for {username} - \n")
    for i, booking in enumerate(found_bookings, start=1):
        print(f"Booking {i} -\n")
        print(f"Username: {booking[0]}")
        print(f"Hall ID: {booking[1]}")
        print(f"Booking Date: {booking[2]}")
        print(f"Booking Time: {booking[3]}")
        print(f"Number of Hours of Booking: {booking[4]}")
        print(f"Price (RM): {booking[5]}")
        print(f"Event Name: {booking[6]}")
        print(f"Event Description: {booking[7]}")
        print(f"Number of People: {booking[8]}")
        print("\n--------------------------------\n")

    while True:
        choice = input("Enter the number of the booking to delete (or 'c' to cancel):\n")
        if choice == 'c':
            print("\nDeletion canceled\n")
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(found_bookings):
            selected_booking = found_bookings[int(choice) - 1]
            print("\nSelected booking information to delete -\n")
            print(f"Username: {selected_booking[0]}")
            print(f"Hall ID: {selected_booking[1]}")
            print(f"Booking Date: {selected_booking[2]}")
            print(f"Booking Time: {selected_booking[3]}")
            print(f"Number of Hours of Booking: {selected_booking[4]}")
            print(f"Price (RM): {selected_booking[5]}")
            print(f"Event Name: {selected_booking[6]}")
            print(f"Event Description: {selected_booking[7]}")
            print(f"Number of People: {selected_booking[8]}\n")

            confirm = input("Do you want to confirm the deletion? (y/n):\n")
            if confirm.lower() == 'y':
                bookings = [booking for booking in bookings if booking != selected_booking]
                with open("bookings.txt", "w") as file:
                    for booking_data in bookings:
                        file.write('|'.join(booking_data) + '\n')
                print("\nDeleting booking information...")
                print("\nBooking information deleted successfully")
            else:
                print("\nDeletion canceled\n")
            return
        else:
            print("\nInvalid choice. Please enter a valid number.")

def user_management_menu(inputUN):
        while True: 
         print(f"\nWelcome to the User Management Menu , {inputUN}!\n")
         print("-----------------------------------\n")
         print("1. View all user information\n")
         print("2. Search user information information\n")
         print("3. Edit user information\n")
         print("4. Delete user from login\n")
         print("5. Return to Main Menu\n")
         choice = input("Enter your choice:\n ")
         if choice == '1':
            view_all_users()
         elif choice == '2':
            search_user_info()
         elif choice == '3':
            edit_user_info()
         elif choice == '4':
            delete_user()
         else:
            admin_menu(inputUN)
            break
         
def view_all_users():
       with open("users.txt", "r") as file:
        users = file.readlines()

        if not users:
            print("No user information available\n")
            return

        print("\nAll User Information - \n")
        for i, user in enumerate(users, start=1):
            details = user.strip().split('|')
            if len(details) >= 7:
                print(f"User {i} -\n")
                print(f"User Name: {details[0]}")
                print(f"User Password: {details[1]}")
                print(f"First Name: {details[2]}")
                print(f"Last Name: {details[3]}")
                print(f"Date of birth: {details[4]}")
                print(f"Contact number: {details[5]}")
                print(f"Email address: {details[6]}")
                print(f"\n----------------------------\n")
            else:
                print(f"Incomplete user information detected for User {i}.\n")

def search_user_info():
    search_term = input("\nEnter first or last name to search: ").lower()
    found = False
    user_count = 0

    print("\nSearching User Information....\n")
    
    with open("users.txt", "r") as file:
        for line in file:
            details = line.strip().split('|')  
            if len(details) >= 7:
                if search_term in [details[2].lower(), details[3].lower()]:
                    user_count += 1
                    print(f"\nUser {user_count} - \n")
                    print(f"User Name: {details[0]}")
                    print(f"User Password: {details[1]}")
                    print(f"First Name: {details[2]}")
                    print(f"Last Name: {details[3]}")
                    print(f"Date of birth: {details[4]}")
                    print(f"Contact number: {details[5]}")
                    print(f"Email address: {details[6]}")
                    found = True
    
    if not found:
        print("\nNo user information found for the given name")
    elif user_count > 1:
        print(f"\nTotal {user_count} users found with the same name\n")

def edit_user_info():
    username_to_edit = input("\nEnter the username of the user to edit: ")
    updated = False

    print("\nSearching for user information...\n")

    with open("users.txt", "r") as file:
        users = [line.strip().split('|') for line in file]

        for user in users:
            if user[0] == username_to_edit:
                print(f"User information for {user[0]} found\n")
                original_user_info = user.copy()  

                while True:
                    print("\nSelect which information to edit -\n")
                    print("1. First Name")
                    print("2. Last Name")
                    print("3. Date of Birth")
                    print("4. Contact Number")
                    print("5. Email Address")
                    print("6. Exit")
                    choice = input("\nEnter your choice (1-6):\n")

                    if choice == '1':
                        new_first_name = input("\nEnter new first name:\n")
                        user[2] = new_first_name
                    elif choice == '2':
                        new_last_name = input("\nEnter new last name:\n")
                        user[3] = new_last_name
                    elif choice == '3':
                        while True:
                            new_dob = input("\nEnter new date of birth (YYYY-MM-DD):\n")
                            if user_login_date(new_dob, '%Y-%m-%d'):
                                user[4] = new_dob
                                break
                            else:
                                print("\nInvalid date format. Enter date of birth (YYYY-MM-DD): ")
                    elif choice == '4':
                        while True:
                            new_contact_number = input("\nEnter new contact number (10 digits):\n")
                            if is_valid_contact_number(new_contact_number):
                                user[5] = new_contact_number
                                break
                            else:
                                print("\nInvalid contact number format. Enter contact number (10 digits): ")
                    elif choice == '5':
                        while True:
                            new_email = input("\nEnter new email address:\n")
                            if is_valid_email(new_email):
                                user[6] = new_email
                                break
                            else:
                                print("\nInvalid email address format. Enter email address: ")
                    elif choice == '6':
                        updated = True
                        break
                    else:
                        print("\nInvalid choice. Please enter a valid option (1-6).")

                if updated:
                    print(f"\nUpdated user information for {user[0]} - \n")
                    print("First Name:", user[2])
                    print("Last Name:", user[3])
                    print("Date of Birth:", user[4])
                    print("Contact Number:", user[5])
                    print("Email Address:", user[6], "\n")
                    confirm = input("Do you want to confirm the changes? (y/n):\n")

                    if confirm.lower() == 'y':
                        with open("users.txt", "w") as file:
                            for user_data in users:
                                file.write('|'.join(user_data) + '\n')
                        print("\nEditing user information...\n")
                        print("User information updated successfully\n")
                    else:
                        users[users.index(user)] = original_user_info  
                        print("\nDiscarding changes....")
                        print("\nChanges discarded\n")
                break

        if not updated:
            print("\nUsername not found")

def delete_user():
    username_to_delete = input("\nEnter the username of the user to delete: ")
    found_user = None

    with open("users.txt", "r") as file:
        users = [line.strip().split('|') for line in file]

    for user in users:
        if user[0] == username_to_delete:
            found_user = user
            break

    if found_user:
        print("\nUser Details - \n")
        print(f"Username: {found_user[0]}")
        print(f"Password: {found_user[1]}")
        print(f"First Name: {found_user[2]}")
        print(f"Last Name: {found_user[3]}")
        print(f"Date of Birth: {found_user[4]}")
        print(f"Contact Number: {found_user[5]}")
        print(f"Email Address: {found_user[6]}")

        confirm = input("\nDo you want to delete this user? (y/n): ")
        if confirm.lower() == 'y':
            users = [user for user in users if user[0] != username_to_delete]
            with open("users.txt", "w") as file:
                for user in users:
                    file.write('|'.join(user) + '\n')
            print("\nDeleting user....")
            print("\nUser deleted successfully")
        else:
            print("\nDeletion canceled")
    else:
        print(f"\nUser not found with username {username_to_delete}\n")

def logout(inputUN):
  while True:
        confirm = input("\nAre you sure you want to log out? (y/n):\n ").lower()
        if confirm == 'y':
            print("\nYou have been successfully logged out.\n")
            mainMenu()
            break
        elif confirm == 'n':
            admin_menu(inputUN)
            break
        else:
            print("\nInvalid response. Please enter 'y' or 'n'")

def check_user_credentials(username, password):
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    saved_username, saved_password = parts[0], parts[1]
                    if saved_username == username and saved_password == password:
                        return True
        return False
    
def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(email_pattern, email):
        return True
    else:
        return False

def is_valid_contact_number(contact_number):
    if contact_number.isdigit() and len(contact_number) == 10:
        return True
    else:
        return False

def user_login_date(dt_str, format_str):
    try:
        input_date = datetime.strptime(dt_str, format_str)
        max_allowed_date = datetime.now() - timedelta(days=365 * 18)

        if input_date <= max_allowed_date:
            return True
        else:
            print("\nYou need to be 18+ to sign up\n")
            return False
    except ValueError:
        return False
    
def user_login():
    print("\nWelcome to the User Login Page\n")
    have_account = ""
    while have_account == "":
        have_account = input("Do you have an account? (yes/no):\n ").strip().lower()

    if have_account == 'no':
        print("\nPlease sign up - \n")
        username = input("Enter Username:\n ")
        password = input("\nEnter Password:\n ")
        first_name = input("\nEnter First Name:\n ")
        last_name = input("\nEnter Last Name:\n ")
        while True:
            date_of_birth = input("\nEnter Date of Birth (YYYY-MM-DD):\n ")
            if user_login_date(date_of_birth, "%Y-%m-%d"):
                break

        while True:
            contact_number = input("\nEnter Contact Number:\n ")
            if is_valid_contact_number(contact_number):
                break
            else:
                print("\nInvalid contact number. Please enter a valid contact number of ten digits.")
        while True:
            email_address = input("\nEnter Email Address:\n ")
            if is_valid_email(email_address):
                break
            else:
                print("\nInvalid email address. Please enter a valid email address.")


        
        with open("users.txt", "a") as file:
            file.write(f"{username}|{password}|{first_name}|{last_name}|{date_of_birth}|{contact_number}|{email_address}\n")

        print("\nSignup successful. Please login.\n")
    
    elif have_account == 'yes':
     
     while True:
        login_option = input("\nEnter 'c' to continue or 'b' to go back to the main menu: ")
        if login_option == 'b':
            break
        elif login_option == 'c':
            username = input("\nEnter Username:\n ")
            password = input("\nEnter Password:\n ")

            if check_user_credentials(username, password):
                print(f"\nLogging in as {username}...")
                print("\nLogin successful\n")
                user__menu(username)
                break
            else:
                print("\nInvalid username or password. Please try again\n")
        else:
            print("\nInvalid input. Please enter 'login' or 'back'\n")

def user__menu(username):
        while True: 
         print(f"\nWelcome to the User Menu, {username}!\n")
         print("-------------------------------------\n")
         print("1. Perform Booking\n")
         print("2. View booking information\n")
         print("3. Delete booking\n")
         print("4. Edit booking information\n")
         print("5. Search booking information\n")
         print("6. Update profile information\n")
         print("7. Logout\n")
         
         choice = input("Enter your choice:\n ")
         if choice == '1':
           user_perform_booking(username)
         elif choice == '2':
            user_view_booking_info(username)
         elif choice == '3':
            user_delete_booking(username)
         elif choice == '4':
            user_edit_booking(username)
         elif choice == '5':
            user_search_booking_info()
         elif choice == '6':
            user_update_profile(username)
         else:
            logout(username) 
            break
         
def valid_hall_book_date(date_str, format_str):
    try:
        input_date = datetime.strptime(date_str, format_str)
        current_date = datetime.now()
        return current_date <= input_date 
    except ValueError:
        return False

def valid_hall_book_time(time_str):
    try:
        input_time = datetime.strptime(time_str, "%H:%M").time()
        return datetime.strptime("08:00", "%H:%M").time() <= input_time <= datetime.strptime("18:00", "%H:%M").time()
    except ValueError:
        return False


def user_perform_booking(username):
        
   while True:
        with open("halls.txt", "r") as file:
            halls = [line.strip().split('|') for line in file]

        with open("bookings.txt", "r") as file:
            booked_hall_ids = {line.strip().split('|')[1] for line in file}
        available_halls = [hall for hall in halls if hall[0] not in booked_hall_ids]

        if not available_halls:
            print("No available halls to book.")
            break  

        print("\nAvailable Hall Types:")
        hall_types = set(hall[2] for hall in available_halls)
        for index, hall_type in enumerate(hall_types, start=1):
            print(f"\n{index}.{hall_type}")

        choice = input("\nSelect the type of hall to book (1/2/3) or 'b' to go back to the user menu: ")
        if choice.lower() == 'b':
            break  

        try:
            choice = int(choice)
            if 1 <= choice <= len(hall_types):
                selected_hall_type = list(hall_types)[choice - 1]
                selected_halls = [hall for hall in available_halls if hall[2] == selected_hall_type]

                print(f"\nAvailable Halls of Type '{selected_hall_type}' - ")
                for index, hall in enumerate(selected_halls, start=1):
                    print(f"\nHall {index} - \n")
                    print(f"Hall ID: {hall[0]}")
                    print(f"Hall Name: {hall[1]}")
                    print(f"Hall Type: {hall[2]}")
                    print(f"Hall Capacity: {hall[3]}")
                    print(f"Hall available on Date: {hall[4]}")
                    print(f"Hall available from Time: {hall[5]}")
                    print(f"Rate per Hour: RM {float(hall[6]):.2f}")
                    print("\n-------------------------")

                while True:
                    choice = input("\nEnter the number of the hall to book or 'b' to go back to the user menu:\n ")
                    if choice.lower() == 'b':
                        break 

                    try:
                        choice = int(choice) - 1
                        if 0 <= choice < len(selected_halls):
                            selected_hall = selected_halls[choice]
                            hall_id = selected_hall[0]
                            rate_per_hour = float(selected_hall[6])
                            print(f"\nYou have chosen to book Hall ID - \n {hall_id}")

                            while True:
                                booking_date = input("\nEnter booking date (YYYY-MM-DD):\n ")
                                if valid_hall_book_date(booking_date, "%Y-%m-%d"):
                                    break
                                elif booking_date.lower() == 'b':
                                    break 
                                else:
                                    print("\nInvalid date format. Please use YYYY-MM-DD.")

                            while True:
                                booking_time = input("\nEnter booking time (HH:MM):\n ")
                                if valid_hall_book_time(booking_time):
                                    break
                                else:
                                    print("\nInvalid time format or hall can only be booked between 8 am and 6 pm.")

                            while True:
                                try:
                                    hours_booked = float(input("\nEnter the number of hours you want to book:\n "))
                                    if hours_booked > 0:
                                        break
                                    else:
                                        print("\nInvalid input. Please enter a positive number of hours.")
                                except ValueError:
                                    print("\nInvalid input. Please enter a valid number.")

                            total_cost = hours_booked * rate_per_hour
                            print(f"\nTotal Cost (RM):\n {total_cost:.2f}")

                            event_name = input("\nEnter Event Name:\n ")
                            event_description = input("\nEnter Event Description:\n ")

                            while True:
                                try:
                                    number_of_people = int(input("\nEnter Number of People:\n "))
                                    if 0 <= number_of_people <= int(selected_hall[3]):
                                        break
                                    else:
                                        print("\nInvalid input. Number of people must be between 0 and hall capacity.")
                                except ValueError:
                                    print("\nInvalid input. Please enter a valid number.")

                            print("\nBooking Summary -\n")
                            print(f"Hall ID: {hall_id}")
                            print(f"Booking Date: {booking_date}")
                            print(f"Booking Time: {booking_time}")
                            print(f"Hours Booked: {hours_booked}")
                            print(f"Total Cost (RM): {total_cost:.2f}")
                            print(f"Event Name: {event_name}")
                            print(f"Event Description: {event_description}")
                            print(f"Number of People: {number_of_people}")

                            confirm_booking = input("\nConfirm the booking (y/n):\n ").strip().lower()
                            if confirm_booking == 'y':
                                booking_details = [
                                    username,
                                    hall_id,
                                    booking_date,
                                    booking_time,
                                    hours_booked,
                                    total_cost,
                                    event_name,
                                    event_description,
                                    number_of_people,
                                ]

                                with open("bookings.txt", "a") as file:
                                    file.write('|'.join(map(str, booking_details)) + '\n')
                                print("\nBooking confirmed!\n")
                            elif confirm_booking == 'n' :
                                print("\nBooking canceled")
                            else:
                                print("\nInvalid Selection.Please choose y or n\n")

                        else:
                            print("Invalid selection. Please choose a valid hall.\n")
                    except ValueError:
                        print("Invalid input. Please enter a number.\n")

            else:
                print("\nInvalid selection. Please choose a valid option.")
                
        except ValueError:
            print("Invalid input. Please enter a number.\n")


def user_view_booking_info(username):
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()

            if not bookings:
                print("No booking information available\n")
                return

            print(f"\nAll Booking Information for {username} - \n")
            for booking in bookings:
                details = booking.strip().split('|') 
                if details[0] == username:
                 print(f"Username:{details[0]}")
                 print(f"Hall ID:{details[1]}")
                 print(f"Booking Date:{details[2]}")
                 print(f"Booking Time:{details[3]}")
                 print(f"Number of hours of Booking:{details[4]}")
                 print(f"Price(Rm) of Booking:{details[5]}")
                 print(f"Event Name:{details[6]}")
                 print(f"Event Description:{details[7]}")
                 print(f"Number of people:{details[8]}\n")
                 print("--------------------------------------\n")

    except FileNotFoundError:
        print("Booking information file not found.")

def user_delete_booking(username):
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()

        user_bookings = [line for line in bookings if line.split('|')[0] == username]

        if len(user_bookings) == 0:
            print(f"No bookings found for username {username}.")
            return

        print(f"\nAll Booking Information for {username} -\n")
        for i, booking in enumerate(user_bookings, 1):
            details = booking.strip().split('|')
            print(f"Booking {i}:\n")
            print(f"Username:{details[0]}")
            print(f"Hall ID:{details[1]}")
            print(f"Booking Date:{details[2]}")
            print(f"Booking Time:{details[3]}")
            print(f"Number of hours of Booking:{details[4]}")
            print(f"Price(Rm) of Booking:{details[5]}")
            print(f"Event Name:{details[6]}")
            print(f"Event Description:{details[7]}")
            print(f"Number of people:{details[8]}\n")
            print("--------------------------------------\n")

        if len(user_bookings) > 1:
            choice = int(input("Enter the number of the booking to delete:\n"))
            if choice < 1 or choice > len(user_bookings):
                print("\nInvalid selection")
                return
            booking_to_delete = user_bookings[choice - 1]
        else:
            booking_to_delete = user_bookings[0]

        updated_bookings = [line for line in bookings if line != booking_to_delete]

        with open("bookings.txt", "w") as file:
            for booking in updated_bookings:
                file.write(booking)

        print("\nDeleting booking...\n")
        print("Booking deleted successfully\n")
    
    except FileNotFoundError:
        print("Booking information file not found.")

    except IndexError:
        print("Invalid selection.")

    except ValueError:
        print("Please enter a valid number.")

def user_edit_booking(username):
    with open("bookings.txt", "r") as file:
        bookings = [line.strip() for line in file.readlines()]

    user_bookings = [booking for booking in bookings if booking.split('|')[0] == username]

    if not user_bookings:
        print(f"\nNo bookings found for username {username}")
        return

    if len(user_bookings) > 1:
        print(f"\nMultiple bookings found for {username}. Please choose which one to edit.\n")
        for index, booking in enumerate(user_bookings, start=1):
            details = booking.split('|')
            print(f"Booking {index} Details - ")
            print(f"\nEvent Name: {details[6]}")
            print(f"Event Description: {details[7]}")
            print(f"Number of hours of Booking: {details[4]}")
            print(f"Booking Date: {details[2]}")
            print(f"Booking Time: {details[3]}")
            print(f"Number of people: {details[8]}")
            print(f"Price(RM): {details[5]}")
            print("\n--------------------------------------\n")

        choice = int(input("\nEnter the number of the booking to edit: ")) - 1
        booking_to_edit = user_bookings[choice]
    else:
        booking_to_edit = user_bookings[0]

    booking_details = booking_to_edit.split('|')

    while True:
        print("\nSelect an option to edit - \n")
        print("1. Event Name")
        print("2. Event Description")
        print("3. Number of hours of Booking")
        print("4. Booking Date")
        print("5. Booking Time")
        print("6. Number of people")
        print("0. Exit\n")
        print("--------------------------------------\n")

        edit_option = input("Enter the option number to edit (0-6):\n")
        if edit_option == '0':
            break
        elif edit_option == '1':
            booking_details[6] = input("\nEnter new Event Name: ")
        elif edit_option == '2':
            booking_details[7] = input("\nEnter new Event Description: ")
        elif edit_option == '3':
            booking_details[4] = input("\nEnter new Number of hours of Booking: ")
            
            hours_booked = float(booking_details[4])
            rate_per_hour = float(booking_details[5])
            total_cost = hours_booked * rate_per_hour
            booking_details[5] = str(total_cost)
        elif edit_option == '4':
            new_booking_date = input("\nEnter new Booking Date (YYYY-MM-DD): ")
            if valid_hall_book_date(new_booking_date, "%Y-%m-%d"):
                booking_details[2] = new_booking_date
            else:
                print("\nInvalid date. Bookings must be on or after the current date.")
        elif edit_option == '5':
            new_booking_time = input("\nEnter new Booking Time (HH:MM): ")
            if valid_hall_book_time(new_booking_time):
                booking_details[3] = new_booking_time
            else:
                print("\nInvalid time. Bookings must be between 8 am to 6 pm.")
        elif edit_option == '6':
            booking_details[8] = input("\nEnter new Number of people: ")
        else:
            print("\nInvalid option. Please enter a valid option (0-6).")

    updated_booking = '|'.join(booking_details)
    for index, booking in enumerate(bookings):
        if booking == booking_to_edit:
            bookings[index] = updated_booking

    with open("bookings.txt", "w") as file:
        for booking in bookings:
            file.write(booking + '\n')

    print(f"\nUpdating booking information....\n")
    print("Updated Booking Details -\n ")
    print(f"Event Name: {booking_details[6]}")
    print(f"Event Description: {booking_details[7]}")
    print(f"Number of hours of Booking: {booking_details[4]}")
    print(f"Booking Date: {booking_details[2]}")
    print(f"Booking Time: {booking_details[3]}")
    print(f"Number of people: {booking_details[8]}")
    print(f"Price(RM): {booking_details[5]}\n")
    print("--------------------------------------")

    confirm_update = input("Confirm the update (y/n):\n ").strip().lower()
    if confirm_update == 'y':
        print("\nBooking confirmed!\n")
    else:
        print("\nBooking update canceled.\n")

    print(f"\nBooking for {username} has been successfully updated\n")

def user_search_booking_info():
    search_term = input("Enter search term (Event Name, Description, Booking ID, etc.):\n ").lower()
    found_bookings = []

    with open("bookings.txt", "r") as file:
        for line in file:
            if search_term in line.lower():
                booking_details = line.strip().split('|')
                found_bookings.append(booking_details)

    if not found_bookings:
        print(f"No booking information found based on {search_term} - \n")
    else:
        if len(found_bookings) > 1:
            print(f"Multiple bookings found based on {search_term}\n")
            for index, booking_details in enumerate(found_bookings, start=1):
                print(f"Booking {index} -\n")
                print(f"Username: {booking_details[0]}")
                print(f"Hall ID: {booking_details[1]}")
                print(f"Booking Date: {booking_details[2]}")
                print(f"Booking Time: {booking_details[3]}")
                print(f"Number of hours of Booking: {booking_details[4]}")
                print(f"Price (Rm) of Booking: {booking_details[5]}")
                print(f"Event Name: {booking_details[6]}")
                print(f"Event Description: {booking_details[7]}")
                print(f"Number of people: {booking_details[8]}\n")
                print("--------------------------------------\n")
        else:
            print("Booking Found -\n")
            booking_details = found_bookings[0]
            print(f"Username: {booking_details[0]}")
            print(f"Hall ID: {booking_details[1]}")
            print(f"Booking Date: {booking_details[2]}")
            print(f"Booking Time: {booking_details[3]}")
            print(f"Number of hours of Booking: {booking_details[4]}")
            print(f"Price (Rm) of Booking: {booking_details[5]}")
            print(f"Event Name: {booking_details[6]}")
            print(f"Event Description: {booking_details[7]}")
            print(f"Number of people: {booking_details[8]}\n")
            print("--------------------------------------\n")

def user_update_profile(username):
    found = False
    updated_users = []

    with open("users.txt", "r") as file:
        users = [line.strip().split('|') for line in file]

        for user in users:
            if user[0] == username:
                found = True
                print(f"\nCurrent user details for {username} -\n")
                print(f"Username: {user[0]}")
                print(f"First Name: {user[2]}")
                print(f"Last Name: {user[3]}")
                print(f"Birthday: {user[4]}")
                print(f"Phone Number: {user[5]}")
                print(f"Email: {user[6]}\n")
                print("-------------------------\n")

                while True:
                    current_password = input("Enter your current password to update profile (or 'b' to go back):\n")

                    if current_password.lower() == 'b':
                        break

                    if current_password == user[1]:
                        while True:
                            options = [
                                ('password', "Update password"),
                                ('first_name', "Update first name"),
                                ('last_name', "Update last name"),
                                ('birthday', "Update birthday"),
                                ('phone_number', "Update phone number"),
                                ('email', "Update email\n"),
                            ]

                            print("\nSelect the information to update -\n ")
                            for i, (key, value) in enumerate(options, start=1):
                                print(f"{i}. {value}")

                            choice = input("Enter the option number or 'b' to go back:\n ")

                            if choice.lower() == 'b':
                                break

                            if choice.isdigit():
                                choice = int(choice) - 1
                                if 0 <= choice < len(options):
                                    key, value = options[choice]
                                    if key == 'password':
                                        new_password = input("\nEnter new password: ")
                                        user[1] = new_password
                                    elif key == 'first_name':
                                        new_first_name = input("\nEnter new first name: ")
                                        user[2] = new_first_name
                                    elif key == 'last_name':
                                        new_last_name = input("\nEnter new last name: ")
                                        user[3] = new_last_name
                                    elif key == 'birthday':
                                        while True:
                                            new_birthday = input("\nEnter new birthday (YYYY-MM-DD): ")
                                            if user_login_date(new_birthday, '%Y-%m-%d'):
                                                user[4] = new_birthday
                                                break
                                            else:
                                                print("\nIncorrect birthday format. Please try again.")
                                    elif key == 'phone_number':
                                        while True:
                                            new_phone_number = input("\nEnter new phone number (10 digits): ")
                                            if is_valid_contact_number(new_phone_number):
                                                user[5] = new_phone_number
                                                break
                                            else:
                                                print("\nIncorrect phone number format. Please try again.")
                                    elif key == 'email':
                                        while True:
                                            new_email = input("Enter new email: ")
                                            if is_valid_email(new_email):
                                                user[6] = new_email
                                                break
                                            else:
                                                print("\nIncorrect email format. Please try again.")
                            else:
                                print("\nInvalid option. Please enter a valid option number or 'b'.")

                        updated_users.append('|'.join(user))
                        break 
                    else:
                        print("\nIncorrect password. Please try again or enter 'b' to go back.")
    
    if found:
        with open("users.txt", "w") as file:
            for u in users:
                file.write('|'.join(u) + '\n')
            
        if updated_users:
            updated_user = updated_users[0].split('|')
            print("\nUpdating user information....\n")
            print("-------------------------------")
            print("\nUpdated User Information -\n")
            print(f"Username: {updated_user[0]}")
            print(f"Password: {updated_user[1]}")
            print(f"First Name: {updated_user[2]}")
            print(f"Last Name: {updated_user[3]}")
            print(f"Birthday: {updated_user[4]}")
            print(f"Phone Number: {updated_user[5]}")
            print(f"Email: {updated_user[6]}\n")

            confirm_changes = input("Confirm the changes (y/n):").strip().lower()
            if confirm_changes == 'y':
                print("\nConfirming changes...\n")
                print("Changes confirmed\n")
                print("-------------------------\n")
            elif confirm_changes == 'n':
                print("\nCanceling changes...\n")
                print("Changes canceled\n")
                print("-------------------------\n")
            else :
             print("\nInvalid input. Please choose y or n\n")
        else:
            print(f"No changes were made to the profile of {username}\n")
    else:
        print(f"No user found with username {username}\n")      

mainMenu()