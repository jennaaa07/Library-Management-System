import os
from datetime import datetime, timedelta

# === CONSTANTS ===
DATE_FORMAT = "%d-%m-%Y"  # Format used by PowerShell commands
MAX_LOAN_DAYS = 1
FINE_PER_DAY = 1.00

# === FILE PATHS ===
BOOKS_FILE = "bTP087704.txt"
USERS_FILE = "uTP087704.txt"
ISSUE_RETURN_FILE = "iTP087704.txt"
APPROVE_FILE = "rTP087704.txt"

# ============== FUNCTIONS ==============
# Load data from file
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        data = []
        for line in file:
            content = line.strip().split(',')
            data.append(content)
    return data

# Save data to file
def save_data(filename, data):
    with open(filename, 'w') as f:
        for record in data:
            f.write(','.join(record) + '\n')

# Record a transaction
def record_transaction(user_id, book_id, status, due_date):
    """Record issue/return transactions"""
    statement = [user_id, book_id, status, due_date]
    with open(ISSUE_RETURN_FILE, 'a') as f:
        f.write(','.join(statement) + '\n')

# Record a book request
def record_request(user_id, book_id, status, request_date):
    """Record book requests"""
    statement = [user_id, book_id, status, request_date]
    with open(APPROVE_FILE, 'a') as f:
        f.write(','.join(statement) + '\n')

# Calculate due date (14 days from today)
def get_due_date():
    cmd = f'powershell -Command "(Get-Date).AddDays({MAX_LOAN_DAYS}).ToString(\'dd-MM-yyyy\')"'
    return os.popen(cmd).read().strip()

# Get current date
def get_current_date():
    cmd = 'powershell -Command "(Get-Date).ToString(\'dd-MM-yyyy\')"'
    return os.popen(cmd).read().strip()

# Center Fill
def center_fill(text, width, fill='='):
    text = f" {text} "
    if width <= len(text):
        return text.center(width)
    remain = width - len(text)
    left = remain // 2
    right = remain - left
    return fill * left + text + fill * right

def get_book_title(book_id, books):
    for b in books:
        if b[0] == book_id:
            return b[1]
    return "Unknown"
    
def get_user_name(user_id, users):
    for u in users:
        if u[0] == user_id:
            return u[1]
    return "Unknown"

# ============= ADMIN FUNCTIONS =============
# Admin Login
def admin_login():
    print(center_fill("\n===== Admin Login =====", 10))
    username = input("Enter username: ")
    password = input("Enter password: ")

    users = load_data(USERS_FILE)
    for user in users:
        if len(user) >= 3 and user[0] == username and user[2] == password and user[3].strip() == "Admin":
            print("\nLogin successful! Welcome Admin.\n")
            return True
    print("Invalid admin credentials.")
    return False

# Add Book
def add_book():
    print(center_fill("\n***** Add Book *****", 10))
    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    qty = input("Enter Quantity: ")

    books = load_data(BOOKS_FILE)
    if any(b[0] == book_id for b in books):
        print("Book with this ID already exists!")
        return

    books.append([book_id, title, author, isbn, qty])
    save_data(BOOKS_FILE, books)
    print("Book added successfully!")

# Remove Book
def remove_book():
    print(center_fill("\n***** Remove Book *****", 10))
    book_id = input("Enter Book ID to remove: ")
    books = load_data(BOOKS_FILE)
    
    updated_books = [b for b in books if b[0] != book_id]
    if len(updated_books) == len(books):
        print("Book not found!")
    else:
        save_data(BOOKS_FILE, updated_books)
        print("Book removed successfully!")

# Modify Book
def modify_book():
    print(center_fill("\n***** Modify Book *****", 10))
    book_id = input("Enter Book ID to modify: ")
    books = load_data(BOOKS_FILE)

    for i, book in enumerate(books):
        if book[0] == book_id:
            print(f"Current details: {', '.join(book)}")
            title = input("Enter new title (or press Enter to keep current): ")
            author = input("Enter new author (or press Enter to keep current): ")
            isbn = input("Enter new ISBN (or press Enter to keep current): ")
            qty = input("Enter new quantity (or press Enter to keep current): ")
            
            if title: book[1] = title
            if author: book[2] = author
            if isbn: book[3] = isbn
            if qty: book[4] = qty
            
            save_data(BOOKS_FILE, books)
            print("Book updated successfully!")
            return
    print("Book not found!")

# Register User
def register_user():
    print(center_fill("\n----- Register New User -----", 10))
    username = input("Enter username: ")
    name = input("Enter name: ")
    password = input("Enter password: ")
    print("\nSelect role:")
    print("1. Admin")
    print("2. Staff")
    print("3. Member")
    role_choice = input("Enter choice (1-3): ")

    if role_choice == "1":
        role = "Admin"
    elif role_choice == "2":
        role = "Staff"
    elif role_choice == "3":
        role = "Member"
    else:
        print("Invalid role choice!")
        return
        
    users = load_data(USERS_FILE)
    
    if any(u[0] == username for u in users):
        print("Username already exists!")
        return

    users.append([username, name, password, role])
    save_data(USERS_FILE, users)
    print(f"{role} registered successfully!")

# View Book
def view_all_books():
    books = load_data(BOOKS_FILE)
    print(center_fill("\n***** Book List *****", 10))
    if not books:
        print("No books in the library.")
        return
    
    print(f"{'ID':6} | {'Title':30} | {'Author':20} | {'ISBN':15} | {'Qty':5} | {'Status':10}")
    print("-" * 95)
    for book in books:
        status = "Available" if int(book[4]) > 0 else "Unavailable"
        print(f"{book[0]:6} | {book[1]:30} | {book[2]:20} | {book[3]:15} | {book[4]:5} | {status:10}")

# Edit Menu
def edit_book_menu():
    print(center_fill("\n***** Edit Book in Library *****", 10))
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Modify Book")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_book()
    elif choice == '2':
        remove_book()
    elif choice == '3':
        modify_book()

# Admin Menu
def admin_menu():
    while True:
        print(center_fill("===== Admin Menu =====", 10))
        print("1. Edit Books")
        print("2. Register New User")
        print("3. View All Books")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            edit_book_menu()
        elif choice == "2":
            register_user()
        elif choice == "3":
            view_all_books()
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            print("Logging out from admin account...\n")
            break
        else:
            print("Invalid choice! Please try again.")

# ============= STAFF FUNCTIONS =============
# Staff Login
def staff_login():
    print(center_fill("Staff Login", 10))
    username = input("Enter username: ")
    password = input("Enter password: ")

    users = load_data(USERS_FILE)
    for user in users:
        if len(user) >= 3 and user[0] == username and user[2] == password and user[3].strip() == "Staff":
            print(f"Welcome, Staff {username}!")
            return username
    print("Invalid staff credentials.")
    return None

# View Book
def view_all_books():
    books = load_data(BOOKS_FILE)
    print(center_fill("\n---** Book List **---", 10))
    if not books:
        print("No books in the library.")
        return 
    
    print(f"{'ID':6} | {'Title':30} | {'Author':20} | {'ISBN':15} | {'Qty':5} | {'Status':10}")
    print("-" * 95)
    for book in books:
        status = "Available" if int(book[4]) > 0 else "Unavailable"
        print(f"{book[0]:6} | {book[1]:30} | {book[2]:20} | {book[3]:15} | {book[4]:5} | {status:10}")

# Search Book
def staff_search_books():
    print(center_fill("Search Book", 10))
    search_term = input("Enter title, author, or ISBN to search: ").lower()
    books = load_data(BOOKS_FILE)
    
    found = [b for b in books if search_term in b[1].lower() or 
             search_term in b[2].lower() or 
             search_term in b[3].lower()]
    
    if not found:
        print("No matching books found.")
        return
        
    print("\nSearch Results:")
    print(f"{'ID':6} | {'Title':30} | {'Author':20} | {'ISBN':15} | {'Qty':5}")
    print("-" * 85)
    for book in found:
        print(f"{book[0]:6} | {book[1]:30} | {book[2]:20} | {book[3]:15} | {book[4]:5}")

# Search Menu
def staff_search_view_menu():
    print(center_fill("Search/View Books", 10))
    print("1. View All Books")
    print("2. Search Book")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        view_all_books()
        input("\nPress Enter to return to menu...")
        return staff_search_view_menu()
    elif choice == "2":
        staff_search_books()
        input("\nPress Enter to return to menu...")
        return staff_search_view_menu()
    elif choice == "3":
        return 

# Approve Book
def process_book_request():
    """Process book borrow requests"""
    approve = load_data(APPROVE_FILE)
    books = load_data(BOOKS_FILE)
    users = load_data(USERS_FILE)
    
    # Filter pending requests and get user/book details
    pending = []
    for a in approve:
        if len(a) >= 3 and a[2].lower() == 'request':
            user = next((u for u in users if u[0] == a[0]), None)
            book = next((b for b in books if b[0] == a[1]), None)
            if user and book:
                pending.append([a[0], user[1], a[1], book[1], a[3]])
                   
    if not pending:
        print("\nNo pending book requests.")
        return
        
    print(center_fill("Pending Book Requests", 10))
    print(f"{'User ID':8} | {'User Name':20} | {'Book ID':8} | {'Book Title':30} | {'Request Date':12}")
    print("-" * 85)
    
    for req in pending:
         print(f"{req[0]:8} | {req[1]:20} | {req[2]:8} | {req[3]:30} | {req[4]:12}")
    
    user_id = input("\nEnter User ID to process (or Enter to cancel): ").strip()
    if not user_id:
        return
        
    book_id = input("Enter Book ID to process: ").strip()
    
    # Verify request exists
    request = next((r for r in pending if r[0] == user_id and r[2] == book_id), None)
    if not request:
        print("Request not found.")
        return
        
    # Check book availability
    book = next((b for b in books if b[0] == book_id), None)
    if not book:
        print("Book not found in library.")
        return
        
    print(f"\nProcessing request for:")
    print(f"User: {request[1]} ({user_id})")  
    print(f"Book: {request[3]} ({book_id})") 
    print(f"Current book quantity: {book[4]}")
    
    action = input("\nEnter 'A' to approve or 'R' to reject: ").strip().upper()
    
    if action == 'A':
        if int(book[4]) > 0:
            # Update book quantity
            book[4] = str(int(book[4]) - 1)
            save_data(BOOKS_FILE, books)
            
            # Update request status to approved
            approve_data = load_data(APPROVE_FILE)
            for req in approve_data:
                if req[0] == user_id and req[1] == book_id and req[2].lower() == 'request':
                    req[2] = 'approved'
            save_data(APPROVE_FILE, approve_data)
            
            # Record new transaction
            due_date = get_due_date()
            record_transaction(user_id, book_id, 'issued', due_date)
            print(f"\nRequest approved:")
            print(f"- Book issued to: {request[1]}")
            print(f"- Due date: {due_date}")
            print(f"- Remaining copies: {book[4]}")
        else:
            print("Cannot approve - book is currently unavailable.")
    elif action == 'R':
        reason = input("Enter rejection reason (optional): ").strip()
        record_transaction(user_id, book_id, 'rejected', get_current_date())
        print(f"\nRequest rejected for {request[1]}")
        if reason:
            print(f"Reason: {reason}")
    else:
        print("Invalid action. Request left pending.")

# Return Book
def process_return():
    """Process book returns and calculate fines"""
    issue = load_data(ISSUE_RETURN_FILE)
    books = load_data(BOOKS_FILE)
    users = load_data(USERS_FILE)
    
    # Get currently issued books
    issued = []
    for i in issue:
        if len(i) >= 4 and i[2].lower() == 'issued':
            user = next((u for u in users if u[0] == i[0]), None)
            book = next((b for b in books if b[0] == i[1]), None)
            if user and book:
                issued.append([i[0], user[1], i[1], book[1], i[3]]) 
    
    if not issued:
        print("\nNo books currently issued.")
        return
    
    print(center_fill("Process Returns", 10))
    print(f"{'User ID':8} | {'Book ID':8} | {'Book':30} | {'Due Date':12}")
    print("-" * 65)
    
    for issue in issued:
        print(f"{issue[0]:8} | {issue[2]:8} | {issue[3]:30} | {issue[4]:12}")
    
    user_id = input("\nEnter User ID: ").strip()
    book_id = input("Enter Book ID: ").strip()
    
    # Verify book is issued to this user
    issue = next((i for i in issued if i[0] == user_id and i[2] == book_id), None)
    if not issue:
        print("No such book issued to this user.")
        return
    
    print(f"\nProcessing return for:")
    print(f"User: {issue[1]} ({user_id})")  
    print(f"Book: {issue[3]} ({book_id})") 
    
    # Calculate any fines
    try:
        due_date = datetime.strptime(issue[4], DATE_FORMAT)
        days_overdue = (datetime.now() - due_date).days
        if days_overdue > 0:
            fine = days_overdue * FINE_PER_DAY
            print(f"\nBook is overdue by {days_overdue} days")
            print(f"Fine amount: RM{fine:.2f}")
            
            payment = input("\nHas fine been paid? (Y/N): ").strip().upper()
            if payment != 'Y':
                print("Please collect payment before processing return.")
                return
    except ValueError:
        days_overdue = 0
    
    # Update book quantity
    book_idx = next((i for i, b in enumerate(books) if b[0] == book_id), None)
    if book_idx is not None:
        books[book_idx][4] = str(int(books[book_idx][4]) + 1)
        save_data(BOOKS_FILE, books)
        
        # Update issue status to returned
        issue_data = load_data(ISSUE_RETURN_FILE)
        for rec in issue_data:
            if rec[0] == user_id and rec[1] == book_id and rec[2].lower() == 'issued':
                rec[2] = 'returned'
        save_data(ISSUE_RETURN_FILE, issue_data)
        
        # Record return transaction
        record_transaction(user_id, book_id, 'returned', get_current_date())
        print("\nBook return processed successfully:")
        print(f"- Returned by: {issue[1]}")
        print(f"- Return date: {get_current_date()}")
        if days_overdue > 0:
            print(f"- Fine paid: RM{fine:.2f}")
        print(f"- Available copies now: {books[book_idx][4]}")
    else:
        print("Error: Book not found in system.")

# Issue Book
def issue_pending():
    print(center_fill("Process Book Requests/Returns", 10))
    print("1. Issue Book")
    print("2. Return Book")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice =="1":
        process_book_request()
        return issue_pending()
    elif choice == "2":
        process_return()
        return issue_pending()
    elif choice == "3":
        return 

# Generate Report
def generate_report():
    transactions = load_data(ISSUE_RETURN_FILE)
    books = load_data(BOOKS_FILE)
    users = load_data(USERS_FILE)
    
    print(center_fill("Library Report", 10))
    print("\n1. Currently Issued Books:")
    print(f"{'User ID':8} | {'User':20} | {'Book ID':8} | {'Book':30} | {'Due Date':12}")
    print("-" * 85)
    
    issued = [t for t in transactions if t[2].lower() == 'issued']
    for t in issued:
        user_name = get_user_name(t[0], users)  
        book_title = get_book_title(t[1], books) 
        print(f"{t[0]:8} | {user_name:20} | {t[1]:8} | {book_title:30} | {t[3]:12}")
    
    print(f"\nTotal books issued: {len(issued)}")
    
    print("\n2. Book Status:")
    for book in books:
        print(f"{book[1]:30} | Available: {book[4]}")

# staff Menu
def staff_menu(staff_id):
    while True:
        print(center_fill("Staff Menu", 10))
        print("1. Search/View Books")
        print("2. Process Book Requests/Returns")
        print("3. Generate Report")
        print("4. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            staff_search_view_menu()
        elif choice == "2":
            issue_pending()
        elif choice == "3":
            generate_report()
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            print("Logging out from staff account...")
            break
        else:
            print("Invalid choice! Please try again.")

# ============= MEMBER FUNCTIONS =============
def member_login():   #Member Login
    print(center_fill("\n=====Member Login=====", 10))
    print("1. Login")
    print("2. Sign Up")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        username = input("\nEnter username: ")
        password = input("Enter password: ")
        
        users = load_data(USERS_FILE)
        for user in users:
            if len(user) >= 3 and user[0] == username and user[2] == password and user[3].strip() == "Member":
                print(f"Welcome back, {username}!\n")
                return username
        print("Invalid login. :()")
        input("Press ENTER to try again...\n")
        return None
        
    elif choice == "2":        #Member Sign Up
        print(center_fill("=====Member Sign Up=====", 10))
        username = input("Create username: ")
        name = input("Enter your name: ")
        password = input("Create password: ")
        
        users = load_data(USERS_FILE)
        if any(u[0] == username for u in users):
            print("Username already exists!")
            return None
            
        users.append([username, name, password, "Member"])
        save_data(USERS_FILE, users)
        print("Member account created successfully! Please login.")
        return member_login()
    
    else:
        print("Invalid choice!")
        return None

# View Available Book
def view_available_books():
    books = load_data(BOOKS_FILE)
    print(center_fill("\n=====Available Books=====", 10))
    
    if not books:
        print("No books in the library.")
        return
    
    print(f"{'ID':6} | {'Title':30} | {'Author':20} | {'ISBN':15} | {'Status':10}")
    print("-" * 90)
    
    for book in books:
        qty = int(book[4])
        status = "Available" if qty > 0 else "Unavailable"
        if qty > 0:  # Only show available books
            print(f"{book[0]:6} | {book[1]:30} | {book[2]:20} | {book[3]:15} | {status:10}")

# Search Book
def member_search_books():
    print(center_fill("\n=====Search Book=====", 10))
    search_term = input("Enter title, author, or ISBN to search: ").lower()
    books = load_data(BOOKS_FILE)
    
    found = [b for b in books if search_term in b[1].lower() or 
             search_term in b[2].lower() or 
             search_term in b[3].lower()]
    
    if not found:
        print("No matching books found.")
        return
        
    print("\nSearch Results:")
    print(f"{'ID':6} | {'Title':30} | {'Author':20} | {'ISBN':15} | {'Qty':5}")
    print("-" * 85)
    for book in found:
        print(f"{book[0]:6} | {book[1]:30} | {book[2]:20} | {book[3]:15} | {book[4]:5}")

# Search View Menu
def search_view_menu():
    print(center_fill("\n~~~Search/View Book~~~", 10))
    print("1. View All Books")
    print("2. Search Book")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice =="1":
        view_available_books()
        input("\nPress Enter to return to menu...\n")
    elif choice == "2":
        member_search_books()
        input("\nPress Enter to return to menu...\n")
    elif choice == "3":
        return 

# Request Book
def request_book(member_id):
    view_available_books()
    book_id = input("\nEnter book ID to request (or Enter to cancel): ").strip()
    if not book_id:
        return
        
    books = load_data(BOOKS_FILE)
    book = next((b for b in books if b[0] == book_id), None)
    
    if not book:
        print("Book not found. Try to find another book.\n")
        return
        
    if int(book[4]) <= 0:
        print("Sorry, this book is currently unavailable.")
        return
        
    # Check if user already has a pending request for this book
    request = load_data(APPROVE_FILE)
    existing_request = any(r[0] == member_id and r[1] == book_id and r[2] == 'request' for r in request)
    
    if existing_request:
        print("You already have a pending request for this book.")
        return
        
    record_request(member_id, book_id, 'request', get_current_date())
    print("Book request submitted successfully. Please wait for staff approval.\n")

# View History
def view_my_history(member_id):
    transactions = load_data(ISSUE_RETURN_FILE)
    books = load_data(BOOKS_FILE)
    
    print(center_fill("\n~~~~~My History~~~~~", 10))
    print(f"{'Book':30} | {'Status':10} | {'Date':12}")
    print("-" * 55)
    
    member_transactions = [t for t in transactions if t[0] == member_id]
    
    if not member_transactions:
        print("No transaction history found.\n")
        return
        
    for t in member_transactions:
        book_title = get_book_title(t[1], books)
        print(f"{book_title:30} | {t[2]:10} | {t[3]:12}")

# Calculate Fines
def calculate_fines(member_id):
    """Calculate overdue fines for a member"""
    transactions = load_data(ISSUE_RETURN_FILE)
    books = load_data(BOOKS_FILE)
    today = datetime.now()
    total_fine = 0.00
    found = False

    print(center_fill("\n***** Overdue Fines *****", 10))
    for trans in transactions:
        if len(trans) >= 4 and trans[0] == member_id and trans[2] == 'issued':
            try:
                due_date = datetime.strptime(trans[3], DATE_FORMAT)
                days_overdue = (today - due_date).days
                if days_overdue > 0:
                    book = next((b for b in books if b[0] == trans[1]), None)
                    title = book[1] if book else "Unknown"
                    fine = days_overdue * FINE_PER_DAY
                    total_fine += fine
                    print(f"{title}: {days_overdue} day(s) overdue = RM{fine:.2f}")
                    found = True
            except ValueError:
                continue

    if not found:
        print("No overdue books. Good Job!\n")
    else:
        print(f"\nTotal Fine: RM{total_fine:.2f}")

# Due Date Reminder
def due_date_reminder(member_id):
    """Show due date reminders for borrowed books"""
    transactions = load_data(ISSUE_RETURN_FILE)
    books = load_data(BOOKS_FILE)
    today = datetime.now()
    reminder_found = False

    print(center_fill("\n***** Due Date Reminder *****", 10))
    for trans in transactions:
        if len(trans) >= 4 and trans[0] == member_id and trans[2] == 'issued':
            try:
                due_date = datetime.strptime(trans[3], DATE_FORMAT)
                days_left = (due_date - today).days
                book = next((b for b in books if b[0] == trans[1]), None)
                title = book[1] if book else "Unknown"
                
                if days_left < 0:
                    print(f"{title} is overdue by {-days_left} day(s)! (Due: {trans[3]})")
                elif days_left == 0:
                    print(f"{title} is due TODAY! (Due: {trans[3]})")
                else:
                    print(f"Reminder: {title} is due in {days_left} day(s). (Due: {trans[3]})\n")
                reminder_found = True
            except ValueError:
                continue

    if not reminder_found:
        print("No upcoming due dates.\n")

# Member Menu
def member_menu(member_id):
    """Member main menu"""
    # Show fines and reminders at login
    calculate_fines(member_id)
    due_date_reminder(member_id)
    
    while True:
        print(center_fill("~~~~~~ Member Menu ~~~~~~", 10))
        print("1. View/Search Books")
        print("2. Request Book")
        print("3. View My History")
        print("4. View My Fines")
        print("5. Due Date Reminder")
        print("6. Logout")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            search_view_menu()
        elif choice == "2":
            request_book(member_id)
        elif choice == "3":
            view_my_history(member_id)
        elif choice == "4":
            calculate_fines(member_id)
        elif choice == "5":
            due_date_reminder(member_id)
        elif choice == "6":
            print("\nLogging out...\nHave a nice day! ByeBye\n")
            break
        else:
            print("Invalid choice!")

# ================Visitor==============
# Visitor Search
def visitor_search():
    print(center_fill("\n***** Book Search *****", 10))
    search_term = input("Enter search keyword: ").upper()
    books = load_data(BOOKS_FILE)
    
    print("\nSearch Results:")
    found = False
    for book in books:
        if search_term in book[1].upper() or search_term in book[2].upper():
            status = "Available" if int(book[4]) > 0 else "Unavailable"
            print(f"Title: {book[1]} / Author: {book[2]} / Status: {status}")
            found = True
    
    if not found:
        print("No search results found.")

# Visitor Catalog
def visitor_display_catalog():
    print(center_fill("\n***** Book Catalog *****", 10))
    books = load_data(BOOKS_FILE)
    
    if not books:
        print("No books in the library.")
        return
        
    for book in books:
        status = "Available" if int(book[4]) > 0 else "Unavailable"
        print(f"Title: {book[1]} / Author: {book[2]} / Status: {status}")

#Visitor Menu
def visitor_menu():
    while True:
        print(center_fill("\n===== Visitor Menu =====", 10))
        print("1. Search Book")
        print("2. View Book Catalog")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            visitor_search()
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            visitor_display_catalog()
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid choice! Please try again.")

# Login Page
def login_page():
    print(center_fill("\n----------** Login Page **----------", 10))
    print("1. Admin Login")
    print("2. Staff Login")
    print("3. Member Login")
    choice = input("Enter your choice: ")

    if choice == "1":
        if admin_login():
            admin_menu()
    elif choice == "2":
        staff_id = staff_login()
        if staff_id:
            staff_menu(staff_id)
    elif choice == "3":
        member_id = member_login()
        if member_id:
            member_menu(member_id)

# ================MAIN MENU==============
def main_menu():
    while True:
        print(center_fill("----------*** Library Management System ***----------", 10))
        print("1. Login (Admin/Staff/Member)")
        print("2. Visitor")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            login_page()
        elif choice == "2":
            visitor_menu()
        elif choice == "3":
            print("\nThank you for using the Library Management System!")
            break
        else:
            print("Invalid choice! Please try again.")

# Main Execution
if __name__ == "__main__":
    # Create files if they don't exist
    for file in [BOOKS_FILE, USERS_FILE, ISSUE_RETURN_FILE, APPROVE_FILE]:
        if not os.path.exists(file):
            open(file, 'a').close()
    main_menu()