# Traffic Data Analysis

## Author

- Gethmi Oshadhi Andrya Goonewardena



## Coursework

- Coursework 1

## Description

This Python program analyses traffic survey data stored in CSV files. It asks the
user to enter a survey date, loads the matching file named
`traffic_dataDDMMYYYY.csv`, calculates traffic statistics, displays the results,
and creates a Tkinter histogram comparing traffic at the two junctions.

The program supports the traffic datasets included in this repository:

- `traffic_data15062024.csv`
- `traffic_data16062024.csv`
- `traffic_data21062024.csv`

## Features

- **Date Input Validation:** Validates the day, month, and year entered by the
  user.
- **CSV Data Processing:** Reads traffic records using `csv.DictReader`.
- **Traffic Statistics:** Calculates total vehicles, trucks, electric vehicles,
  two-wheeled vehicles, bicycles, buses, vehicles that did not turn, speeding
  vehicles, junction totals, scooter percentages, peak-hour traffic, and rainy
  hours.
- **Results Display:** Prints the analysis results in the console.
- **Results Saving:** Appends each analysis to `results.txt`.
- **Histogram Display:** Opens a Tkinter histogram showing hourly traffic at
  Elm Avenue/Rabbit Road and Hanley Highway/Westway.
- **Repeated Analysis:** Allows the user to analyse another date.
- **File Checking:** Checks whether the requested CSV file exists before
  processing it.

## Files

- `coursework.py`: The main Python program.
- `traffic_data15062024.csv`: Traffic data for 15/06/2024.
- `traffic_data16062024.csv`: Traffic data for 16/06/2024.
- `traffic_data21062024.csv`: Traffic data for 21/06/2024.
- `results.txt`: Saved analysis results.

## Requirements

- Python 3
- Tkinter, which is included with most standard Python installations

## How to Run

1. Make sure Python 3 is installed.
2. Open a terminal in the project directory.
3. Run the program:

   ```text
   python coursework.py
   ```

4. Enter the day, month, and year when prompted. For example:

   ```text
   Day: 15
   Month: 6
   Year: 2024
   ```

5. The program loads `traffic_data15062024.csv`, displays the statistics, and
   opens the histogram.
6. Close the histogram window to continue.
7. Choose `Y` to analyse another date or `N` to exit.

## Date and File Format

The program constructs the data filename using this format:

```text
traffic_dataDDMMYYYY.csv
```

For example, entering day `15`, month `6`, and year `2024` loads:

```text
traffic_data15062024.csv
```

Each CSV file contains fields including:

- `JunctionName`
- `Date`
- `timeOfDay`
- `travel_Direction_in`
- `travel_Direction_out`
- `Weather_Conditions`
- `JunctionSpeedLimit`
- `VehicleSpeed`
- `VehicleType`
- `elctricHybrid`

## Code Overview

### `validate_date_input()`

Prompts for the day, month, and year and checks that each value is an integer
within the accepted range. It returns the date as `DDMMYYYY` for use in the
filename.

### `validate_continue_input()`

Accepts only `Y` or `N` and controls whether another dataset is analysed.

### `process_csv_data(file_path)`

Reads the selected CSV file, counts the required traffic categories, calculates
hourly counts for both junctions, and returns the results in a dictionary.

### `display_outcomes(outcomes, file_name)`

Prints the calculated statistics and appends the same results to `results.txt`.

### `plot_histogram_tkinter(hourly_counts_j1, hourly_counts_j2, date)`

Creates a Tkinter histogram comparing the number of vehicles recorded during
each hour at both junctions.

### `main()`

Runs the complete program loop: date input, file selection, CSV processing,
result display, histogram display, and the continue prompt.

## Output

The program displays statistics such as:

- Total vehicles
- Total trucks and truck percentage
- Electric vehicles
- Two-wheeled vehicles
- Northbound buses at Elm Avenue/Rabbit Road
- Vehicles that did not turn
- Average bicycles per hour
- Vehicles over the speed limit
- Total vehicles at each junction
- Scooter percentage at Elm Avenue/Rabbit Road
- Highest hourly traffic
- Rain-related records

Results are appended to `results.txt` after each successful analysis.
