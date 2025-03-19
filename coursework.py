# Author: Gethmi Oshadhi Andrya Goonewardena
# Date: 2024.12.24
# Student ID: w2120165

import os
import csv

# Task A: Input Validation
def validate_date_input():
     """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
     while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if not 1 <= day <= 31:
                print("Out of range - values must be in the range 1 to 31.")
                continue
            break
        except ValueError:
            print("Integer required")

     while True:
         try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if not 1 <= month <= 12:
                print("Out of range - values must be in the range 1 to 12.")
                continue
            break
         except ValueError:
             print("Integer required")

     while True:
         try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if not 2000 <= year <= 2024:
                print("Out of range - values must range from 2000 and 2024.")
                continue
            break
         except ValueError:
             print("Integer required")
        

     return f"{day:02}{month:02}{year}"


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        user_input = input("Do you want to analyze another date? (Y/N): ").strip().upper()
        if user_input in ('Y', 'N'):
            return user_input
        else:
            print('Please enter "Y" or "N"')

            
# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    outcomes = {
        "total_vehicles": 0,
        "total_trucks": 0,
        "electric_vehicles": 0,
        "two_wheeled_vehicles": 0,
        "total_bicycles": 0,
        "northbound_buses": 0,
        "no_turns": 0,
        "over_speed_limit": 0,
        "junction_1_total": 0,
        "junction_2_total": 0,
        "junction_1_scooters": 0,
        "peak_hour_traffic": 0,
        "peak_hours": [],
        "rain_hours": 0,
    }

    hourly_counts_j1 = {}
    hourly_counts_j2 = {}

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                outcomes["total_vehicles"] += 1
                if row["VehicleType"] == "Truck":
                    outcomes["total_trucks"] += 1
                if row["elctricHybrid"].upper() == "TRUE":
                    outcomes["electric_vehicles"] += 1
                if row["VehicleType"] in ["Bicycle", "Motorcycle", "Scooter"]:
                    outcomes["two_wheeled_vehicles"] += 1
                if row["VehicleType"] == "Bicycle":
                    outcomes["total_bicycles"] +=1
                if row["travel_Direction_out"] == "N" and row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["VehicleType"] == "Buss":
                    outcomes["northbound_buses"] += 1
                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    outcomes["no_turns"] += 1
                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    outcomes["over_speed_limit"] += 1

                junction = row["JunctionName"]
                hour = row["timeOfDay"].split(":")[0]


                if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["VehicleType"].lower() == "Buss" and row["travel_Direction_out"].upper() == "N":
                    outcomes["northbound_buses"] +=1

                if junction == "Elm Avenue/Rabbit Road":
                    outcomes["junction_1_total"] += 1
                    hourly_counts_j1[hour] = hourly_counts_j1.get(hour, 0) + 1
                    if row["VehicleType"] == "Scooter":
                        outcomes["junction_1_scooters"] += 1
                elif junction == "Hanley Highway/Westway":
                    outcomes["junction_2_total"] += 1
                    hourly_counts_j2[hour] = hourly_counts_j2.get(hour, 0) + 1

                if row["Weather_Conditions"] == "Rain":
                    outcomes["rain_hours"] += 1

        outcomes["hourly_counts_j1"] = hourly_counts_j1
        outcomes["hourly_counts_j2"] = hourly_counts_j2

        if hourly_counts_j1 or hourly_counts_j2:
            max_j1 = max(hourly_counts_j1.values(), default=0)
            max_j2 = max(hourly_counts_j2.values(), default=0)
            outcomes["peak_hour_traffic"] = max(max_j1, max_j2)
            outcomes["peak_hours"] = [
                f"Between {hour}:00 and {int(hour) + 1}:00"
                for hour, count in {**hourly_counts_j1, **hourly_counts_j2}.items()
                if count == outcomes["peak_hour_traffic"]
            ]

    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    return outcomes



def display_outcomes(outcomes, file_name):
    """
    Displays the calculated outcomes in a clear and formatted way in the IDLE shell.
    Includes all the required statistics for the selected CSV file.
    """
    print("\n************************************")
    print(f"data file selected is {file_name}")
    print("\n************************************")
    print(f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}")
    print(f"The total number of trucks recorded for this date is {outcomes['total_trucks']}")
    print(f"The total number of electric vehicles for this date is {outcomes['electric_vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes['two_wheeled_vehicles']}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['northbound_buses']}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['no_turns']}")

    # Calculate and display the truck percentage
    truck_percentage = (
        round((outcomes['total_trucks'] / outcomes['total_vehicles']) * 100)
        if outcomes['total_vehicles'] > 0
        else 0
    )
    print(f"The percentage of total vehicles recorded that are trucks for this date is {truck_percentage}%")

    # Calculate and display the average of total bicycles per hour
    total_bicycles = outcomes['total_bicycles']
    avg_bicycles_per_hour = round(total_bicycles / 24)  # In here we assume a 24-hour period to find the average of bicycles per hour
    print(f"The average bicycles per hour for this date is {avg_bicycles_per_hour}")

    print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['over_speed_limit']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['junction_1_total']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['junction_2_total']}")

    # Calculate and display the scooter percentage
    if outcomes["junction_1_total"]>0:
        scooter_percentage =(outcomes["junction_1_scooters"]*100) //outcomes["junction_1_total"]
    else:
        scooter_percentage=0

        
    print(f"{scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")

    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_traffic']}")

    if outcomes["peak_hours"]:
        print(f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(outcomes['peak_hours'])}")
    else:
        print(f"The most vehicles through Hanley Highway/Westway were recorded is No data available")
    

    print(f"The number of hours of rain for this date is {outcomes['rain_hours']}")
    print("=" * 60 + "\n")


#add results as a list
    results = [
        f"data file selected is {file_name}",
        f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}",
        f"The total number of trucks recorded for this date is {outcomes['total_trucks']}",
        f"The total number of electric vehicles for this date is {outcomes['electric_vehicles']}",
        f"The total number of two-wheeled vehicles for this date is {outcomes['two_wheeled_vehicles']}",
        f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['northbound_buses']}",
        f"The total number of Vehicles through both junctions not turning left or right is {outcomes['no_turns']}",
        f"The percentage of total vehicles recorded that are trucks for this date is {truck_percentage}%",
        f"The average bicycles per hour for this date is {avg_bicycles_per_hour}",
        f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['over_speed_limit']}",
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['junction_1_total']}",
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['junction_2_total']}",
        f"{scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_traffic']}",
        f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(outcomes['peak_hours'])}",
        f"The number of hours of rain for this date is {outcomes['rain_hours']}",
        "\n******************************"
        ]
    # Task C: Save Results to Text File
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    with open("results.txt", "a") as result_file:
        result_file.write("\n".join(results) + "\n")

    


# Task D: Histogram Display
import tkinter as tk


def plot_histogram_tkinter(hourly_counts_j1, hourly_counts_j2, date):
    """
    Plots a histogram comparing vehicle frequency per hour for two junctions using Tkinter.
    """
    # Prepare data
    hours = [f"{hour:02}" for hour in range(24)]  # Hours from 00 to 23
    counts_j1 = [hourly_counts_j1.get(hour, 0) for hour in hours]
    counts_j2 = [hourly_counts_j2.get(hour, 0) for hour in hours]

    # Create Tkinter window
    root = tk.Tk()
    root.title(f"Histogram")

    canvas_width = 1100
    canvas_height = 700
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="yellow")
    canvas.pack()

    # Plot settings
    bar_width = 15
    bar_gap = 10
    x_start = 50
    y_offset = 50
    x_start = 50
    y_base = canvas_height - 49
    max_count = max(max(counts_j1), max(counts_j2))
    scale_factor = (canvas_height - 2 * y_offset - 50) / max_count if max_count > 0 else 1

    # Draw bars and labels
    for i, hour in enumerate(hours):
        # Calculate positions
        x1_j1 = x_start + i * (2 * bar_width + bar_gap)
        y1_j1 = canvas_height - y_offset - (counts_j1[i] * scale_factor)
        x2_j2 = x1_j1 + bar_width + 2
        y2_j2 = canvas_height - y_offset - (counts_j2[i] * scale_factor)

        # Draw bars for Junction 1
        canvas.create_rectangle(x1_j1, y1_j1, x1_j1 + bar_width, canvas_height - y_offset, fill="green", outline="green")
        canvas.create_text(x1_j1 + bar_width / 2, y1_j1 - 10, text=str(counts_j1[i]), anchor="s", font=("Arial", 8))

        # Draw bars for Junction 2
        canvas.create_rectangle(x2_j2, y2_j2, x2_j2 + bar_width, canvas_height - y_offset, fill="red", outline="red")
        canvas.create_text(x2_j2 + bar_width / 2, y2_j2 - 10, text=str(counts_j2[i]), anchor="s", font=("Arial", 8))

        # Add hour labels
        canvas.create_text((x1_j1 + x2_j2 + bar_width) / 2, canvas_height - y_offset + 8, text=hour, anchor="n", font=("Arial", 10))

    # Draw title and legend
    canvas.create_text(canvas_width / 2, 20, text=f"Histogram of Vehicle Frequency per Hour ({date[:2]}/{date[2:4]}/{date[4:8]})", font=("Arial", 16, "bold"))
    canvas.create_rectangle(60, 40, 80, 60, fill="green", outline="green")
    canvas.create_text(90, 50, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))
    canvas.create_rectangle(60, 70, 80, 90, fill="red", outline="red")
    canvas.create_text(90, 80, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10))

    # Draw axis labels
    canvas.create_text(canvas_width / 2, canvas_height - y_offset + 33, text="Hours 00:00 to 24:00", anchor="n", font=("Arial", 11))
    canvas.create_line(50, 50, 50, y_base, width=2)  # Y-axis
    canvas.create_line(50, y_base, canvas_width - 50, y_base, width=2)  # X-axis
    canvas.create_text(20, canvas_height / 2, text="Vehicle Count", anchor="center", angle=90, font=("Arial", 11))

    

    # Run Tkinter main loop
    root.mainloop()
    

# Task E: Code Loops to Handle Multiple CSV Files
def main():

    while True:
        date = validate_date_input()
        file_name = f"traffic_data{date}.csv"#processes csv files and loads its data
        file_path = os.path.join(file_name)
        if os.path.exists(file_path):
            outcomes = process_csv_data(file_path)
            display_outcomes(outcomes, file_name)
            

            plot_histogram_tkinter(outcomes["hourly_counts_j1"], outcomes["hourly_counts_j2"], date)

#quit from the loop
        if validate_continue_input() == "N":
             print(f"End of run")
             break


if __name__ == "__main__":
    main()
    
#References:
"""
W3Schools, 2024. Python try-except. W3Schools.

Coursework Specification, 2024. Traffic Data Analysis Instructions. [Informatics Institute of Technology].

Real Python, 2024. Python Dictionaries: A Comprehensive Guide. Real Python.
"""
