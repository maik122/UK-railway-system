import tkinter as tk # Import tkinter
from tkinter import messagebox, simpledialog # Import messagebox and simpledialog from tkinter 
import pandas as pd # Import pandas to read the csv file
from tkinter import ttk # Import ttk from tkinter for styling the widgets 
import random # Import random

# Create the main window and set the title, background color, and size
root = tk.Tk()  
root.title("Train Ticket Search System")
root.configure(bg="white") 
#full screen
#oot.attributes('-fullscreen', True)

root.geometry("1000x1000") 

#create style for the widgets in the main window
style =  ttk.Style() # Create an instance of the ttk style  
style.configure(".", background="white", foreground="black") # set the style for all widgets 
style.configure("TButton", background="white", foreground="black", font=("Helvitica", 14)) # set the style for all buttons 

# Read the csv file using pandas and name the columns as station1, station2, and cost respectively
df = pd.read_csv("Task1.4/task1_4_railway_network.csv", names=["station1", "station2", "cost"])

# Define graph weight class to store the graph and perform the Dijkstra algorithm
class GraphWeight:
    def __init__(self, V=None, E=None, directed=True):
        self.gdict = {}  # Dictionary to store the graph
        self.directed = directed  # Boolean to indicate if the graph is directed or undirected
        if V is not None and E is not None: # If the graph is not empty
            for v in V: # For each vertex in the graph
                self.gdict[v] = []  # Create a list for each vertex in the graph

            if directed:  # If the graph is directed, add the edge to the start vertex
                for sv, ev, weight in E: # For each start vertex, end vertex, and weight in the graph
                    if sv in self.gdict: # If the start vertex is in the graph
                        self.gdict[sv].append((ev, weight)) # Add the edge to the start vertex

            else:  # If the graph is undirected, add the edge to both start and end vertex
                for sv, ev, weight in E:    # For each start vertex, end vertex, and weight in the graph
                    if sv in self.gdict and ev in self.gdict:   # If the start vertex and end vertex are in the graph
                        self.gdict[sv].append((ev, weight)) # Add the edge to the start vertex
                        self.gdict[ev].append((sv, weight)) # Add the edge to the end vertex

    def dijkstraSP(self, start, end):   # Function to perform the Dijkstra algorithm
        allnodes = list(self.gdict.keys())  # Get all the nodes in the graph

        if start not in allnodes or end not in allnodes:    # If the start or end node is not in the graph
            return None  # If the start or end node is not in the graph, return None

        infinite = 100000  # Set the infinite value to be 100000 to represent the infinite distance
        table = {}  # Create a table dictionary to store the distance from the start node to each node
        for node in allnodes:  # Initialize the distance from the start node to each node to be infinite
            table[node] = (node, infinite) # Set the distance from the start node to each node to be infinite

        edges = []  # Create a list to store the edges in the shortest path
        table[start] = (start, 0)  # Set the distance from the start node to itself to be 0
        current = start  # Set the current node to be the start node
        while current != end:  # While the current node is not the end node
            for v, w in self.gdict[current]:  # For each neighbor of the current node
                if v in table:  # If the neighbor is in the table
                    totalweight = table[current][1] + w  # Calculate the total weight from the start node to the neighbor
                    if totalweight < table[v][1]:  # If the total weight is less than the current weight in the table
                        table[v] = (current, totalweight)  # Update table with the new weight
            table.pop(current)  # Remove the current node from the table
            unvisited = list(table.items())  # Get the unvisited nodes from the table

            if len(unvisited) == 0: # If there is no unvisited node
                return None  # If there is
        # Sort the unvisited nodes by the weight in the table
            unvisited.sort(key=lambda x: x[1][1])   # Sort the unvisited nodes by the weight in the table

            current = unvisited[0][0]  # Set the current node to be the node with the smallest weight in the table

            edges.append((table[current][0], current, table[current][1]))  # Add the edge to the list of edges in the shortest path
        return edges  # Return the list of edges in the shortest path

#create an instance of the GraphWeight class with data from the CSV file 
graph_data = list(df.itertuples(index=False, name=None))  # Convert DataFrame rows to tuples and store in a list to be used to instantiate the GraphWeight class
stations = sorted(list(set(df["station1"]).union(set(df["station2"]))), key=lambda sta: sta.strip().lower())  # Sort the stations in alphabetical order and remove spaces and capital letters from the station names
graph = GraphWeight(stations, graph_data, directed=False)  # Instantiate the GraphWeight class with data from the CSV file and making the graph undirected 

#search function to perform dijkstra algorithm to find the shortest path and display the result
def search():
    #get the departure and destination from the user input 
    departure = departure_option.get()  
    destination = destination_option.get()

    #if the departure or destination is not selected, return a message to ask user to select departure and destination
    if departure == "Select Departure Station" or destination == "Select Destination Station":
        result_label.configure(text="Please select a departure and destination station.")   #display the message in the result label if the departure or destination is not selected
        
    elif departure == destination: #if the departure and destination are the same, return a message to ask user to select different departure and destination
        result_label.configure(text="Departure cannot be the same as destination. Please select different departure and destination.")
    
    else: #if the departure and destination are selected, perform dijkstra algorithm to find the shortest path
        path = graph.dijkstraSP(departure, destination) #perform dijkstra algorithm to find the shortest path from the departure to the destination and store the result in the path variable
        if path:
            cost = path[-1][2] #get the cost from the path 
            route = [edge[0].capitalize() for edge in path]  #get the route from the path and capitalize the first letter of each station name in the route
        #print(path)
        #display the result in the result label with the cost and route joined by " -> "
        result_label.configure(text="The cheapest cost from {} to {} is: £ {} \n Route: {}".format(departure, destination, cost, " -> ".join(route))) 

#reset function to reset the departure and destination and result
def reset():
    departure_option.set("Select Departure Station")
    destination_option.set("Select Destination Station")
    result_label.configure(text="The route and cost will be displayed here.")


# Function to handle the admin login process  
def admin_login(): 
    # Prompt the user for credentials 
    username = simpledialog.askstring("Admin Login", "Enter your username:") 
    password = simpledialog.askstring("Admin Login", "Enter your password:", show="*")
    # Check if the credentials are correct against the credentials stored in the file 
    with open("Task1.4/credentials.txt", "r") as file:
        credentials = file.read().splitlines() # Read the credentials from the file and split them into a list
        stored_username = credentials[0] # Get the stored username 
        stored_password = credentials[1] # Get the stored password
        
        #if the username and password are correct, open the admin interface window
        if username == stored_username and password == stored_password: 
            admin_page()
        else: #if the username and password are incorrect, return a message to ask user to try again
            messagebox.showerror("Admin Login", "Invalid credentials. Please try again.")
    '''
    #test the username and password 
    print(f"entered username: {username}")
    print(f"entered password: {password}")
    print(f"stored username: {credentials[0]}")
    print(f"stored password: {credentials[1]}")
    '''
    '''
    #hardcode the username and password 
    # Check if the credentials are correct
    #if username == "admin" and password == "pass":
    #    admin_page()
    #else:
            #messagebox.showerror("Admin Login", "Invalid credentials. Please try again.")
'''
# Function to open the admin interface window
def admin_page():
    admin_window = tk.Toplevel(root) # Create a new window for the admin interface at the top level of the root window
    admin_window.title("Admin Interface") # Set the title of the admin interface window
    admin_window.geometry("450x450") # Set the size of the admin interface window

    # Create a Text widget to display the current contents of the CSV file 
    text_widget = tk.Text(admin_window) 
    text_widget.pack() 

    # Open the CSV file and read its contents 
    with open("Task1.4/task1_4_railway_network.csv", "r") as file: 
        csv_contents = file.read() 

    # Insert the CSV contents into the Text widget  
    text_widget.insert(tk.END, csv_contents) #put text at the end of the text widget 

    # Create a button to save the modified contents back to the CSV file
    save_button = tk.Button(admin_window, text="Save Changes", command=lambda: save_changes(text_widget.get("1.0", tk.END))) #get the text from the text widget from line 1 char 0  and save the changes to the CSV file
    save_button.pack()

# Function to save the changes made in the admin interface
def save_changes(contents):
    with open("Task1.4/task1_4_railway_network.csv", "w") as file:
        file.write(contents) # Write the contents of the Text widget to the CSV file
    messagebox.showinfo("Save Changes", "Changes saved successfully.")

# Function to book a ticket
def book_ticket() :
    # Get the departure and destination from the user input
    departure = departure_option.get()
    destination = destination_option.get()

    # If the departure or destination is not selected, display an error message
    if departure == "Select Departure Station" or destination == "Select Destination Station":
        messagebox.showerror("Error", "Please select a departure and destination station.")
    else:
        # Prompt the user to enter their details
        email = simpledialog.askstring("Enter Email", "Please enter your email address:")
        seat_number = simpledialog.askinteger("Select Seat Number", "Please select a seat number (1-50):", minvalue=1, maxvalue=50)

        if email and seat_number:
            # Generate a random ticket number
            ticket_number = generate_ticket_number()
            # Get the cost from the result label using the cget() method and split the string to get the cost 
            result_text = result_label.cget("text")
            cost = result_text.split("£")[1].strip().split("\n")[0].strip()
            
            # Display booking confirmation message
            messagebox.showinfo("Booking Confirmed", "Booking confirmed!\n\nTicket Number: {}\n Seat number: {}\n Total paid: {} £\n\nConfirmation email will be sent to: {}".format(ticket_number,seat_number, cost, email))
        else:
            # Display an error message if email or seat number is not provided
            messagebox.showerror("Error", "You must enter Email and seat number.")

# Function to generate a random ticket number
def generate_ticket_number():
    # Generate a random ticket number
    ticket_number = "LDN" + str(random.randint(1000, 3000))
    return ticket_number        
def view_map():
    pass
# Header frame 
header_frame = tk.Frame(root)
header_frame.grid(row=0, column=0, columnspan=2, pady=20)
header_font = ("Helvetica", 30, "bold")
header_label = tk.Label(header_frame, text="Train Ticket Search System", font=header_font, bg="white", fg="black")
header_label.pack()

# Body frame 
body_frame = tk.Frame(root)
body_frame.grid(row=1, column=0, columnspan=2, pady=20,padx=20)
body_frame.configure(bg="black", highlightthickness=1) # Add a border around the body frame 
body_font = ("Helvetica", 14)

# Departure and destination options and buttons
departure_label = tk.Label(body_frame, text="Departure Station:", font=body_font,bg="black",fg="white")
departure_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)
departure_option = tk.StringVar(root)  # Create a string variable to store the departure station
departure_optionmenu = ttk.OptionMenu(body_frame, departure_option, *stations)
departure_optionmenu.grid(row=0, column=1, pady=10, padx=10)
departure_option.set("Select Departure Station")  # Set the default value of the departure station

destination_label = tk.Label(body_frame, text="Destination Station:", font=body_font,bg="black",fg="white")
destination_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)
destination_option = tk.StringVar(root)
destination_optionmenu = ttk.OptionMenu(body_frame, destination_option, *stations)  # Create an option menu to display the destination stations in the drop-down menu
destination_optionmenu.grid(row=1, column=1, pady=10, padx=10)
destination_option.set("Select Destination Station")  # Set the default value of the destination station

search_button = ttk.Button(root, text="Search", command=search)
search_button.grid(row=2, column=1, pady=10)
# Create the search button
#search_button = tk.Button(root, text="Search", width=10, font=body_font, command=search, bg="white", fg="black")
#search_button.grid(row=2, column=1, pady=10)

# Create the reset button
reset_button = ttk.Button(root, text="Reset",command=reset)
reset_button.grid(row=3, column=1, pady=10)

# Create the result label
result_label = tk.Label(root, text="The route and cost will be displayed here", font=body_font, wraplength=700, justify=tk.LEFT, bg="white", fg="black")
result_label.grid(row=4, column=0, pady=20, padx=10, sticky=tk.NSEW, columnspan=2)

# Create the admin login button
admin_button = ttk.Button(root, text="Admin Login",command=admin_login)
admin_button.place(relx=1, x=-10, y=10, anchor=tk.NE)

# Create the book ticket button
book_ticket_button = ttk.Button(root, text="Book Ticket",command=book_ticket)
book_ticket_button.place(relx=1, x=-10, y=50, anchor=tk.NE)

# Create the view map button    
view_map_button = ttk.Button(root, text="View Map",command=view_map)
view_map_button.place(relx=1, x=-10, y=90, anchor=tk.NE)
# Start the main loop
root.mainloop()
