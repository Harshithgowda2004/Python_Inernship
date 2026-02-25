from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

POINTS = ['A', 'B', 'C', 'D', 'E', 'F']

def get_point_index(p):
    return POINTS.index(p)

def calculate_distance(p1, p2):
    return abs(get_point_index(p2) - get_point_index(p1)) * 15

def calculate_travel_time(p1, p2): # in hours
    return abs(get_point_index(p2) - get_point_index(p1))

def calculate_fare(distance):
    if distance <= 5:
        return 100
    return 100 + (distance - 5) * 10

class Taxi:
    def __init__(self, taxi_id):
        self.id = taxi_id
        self.current_point = 'A'
        self.free_time = 0
        self.earnings = 0
        self.bookings = []

    def is_available(self, pickup_time):
        return self.free_time <= pickup_time

class Booking:
    id_counter = 1
    
    def __init__(self, customer_id, pickup_point, drop_point, pickup_time):
        self.id = Booking.id_counter
        Booking.id_counter += 1
        self.customer_id = customer_id
        self.pickup_point = pickup_point
        self.drop_point = drop_point
        self.pickup_time = pickup_time
        
        self.distance = calculate_distance(pickup_point, drop_point)
        self.amount = calculate_fare(self.distance)
        self.travel_duration = calculate_travel_time(pickup_point, drop_point)
        self.drop_time = pickup_time + self.travel_duration

# Initialize 4 taxis
taxis = [Taxi(i + 1) for i in range(4)]

@app.route("/", methods=["GET", "POST"])
def book_taxi():
    message = ""
    animation_data = None
    
    if request.method == "POST":
        try:
            customer_id = int(request.form["cid"])
            pickup_point = request.form["pickup"]
            drop_point = request.form["drop"]
            pickup_time = int(request.form["ptime"])
            
            # Find available taxis
            available_taxis = []
            for taxi in taxis:
                if taxi.is_available(pickup_time):
                    # Calculate distance from taxi's current location to pickup point
                    distance_to_pickup = calculate_distance(taxi.current_point, pickup_point)
                    available_taxis.append((distance_to_pickup, taxi))
            
            if not available_taxis:
                message = "Booking Rejected. No taxi available."
            else:
                # Sort by distance to pickup (asc), then earnings (asc)
                available_taxis.sort(key=lambda x: (x[0], x[1].earnings))
                chosen_taxi = available_taxis[0][1]
                
                # Create booking
                booking = Booking(customer_id, pickup_point, drop_point, pickup_time)
                
                # Prepare animation data
                animation_data = {
                    "taxi_id": chosen_taxi.id,
                    "start_point": chosen_taxi.current_point,
                    "pickup_point": booking.pickup_point,
                    "drop_point": booking.drop_point
                }
                
                # Update Taxi
                chosen_taxi.earnings += booking.amount
                chosen_taxi.current_point = drop_point
                chosen_taxi.free_time = booking.drop_time
                
                # Add booking to history
                chosen_taxi.bookings.append([
                    booking.id,
                    booking.customer_id,
                    booking.pickup_point,
                    booking.drop_point,
                    booking.pickup_time,
                    booking.drop_time,
                    booking.amount
                ])
                
                message = f"Taxi can be allotted.<br>Taxi-{chosen_taxi.id} is allotted"
                
        except ValueError:
            message = "Invalid Input: Please ensure all fields are filled correctly."

    return render_template("index.html", msg=message, taxis=taxis, animation_data=animation_data)

@app.route("/add_taxi", methods=["POST"])
def add_taxi():
    new_id = len(taxis) + 1
    taxis.append(Taxi(new_id))
    return redirect(url_for('book_taxi'))

@app.route("/remove_taxi", methods=["POST"])
def remove_taxi():
    if len(taxis) > 4:
        taxis.pop()
    return redirect(url_for('book_taxi'))

@app.route("/taxis")
def view_taxis():
    return render_template("taxis.html", taxis=taxis)

if __name__ == "__main__":
    app.run(debug=True)
