# Example utility script (run once)
import csv
import pickle
import time

leave_lookup_table = {}
csv_filename = 'NWL23-leaves.csv' # Your exported file
pickle_filename = 'NWL23-leaves.pkl'
start_time = time.time()

print(f"Loading data from {csv_filename}...")
try:
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip header if it exists
        # next(reader, None)
        for i, row in enumerate(reader):
            if len(row) == 2:
                leave_str_sorted = "".join(sorted(row[0].upper())) # Ensure sorted and uppercase key
                try:
                    value = float(row[1]) # Or int() if values are integers
                    leave_lookup_table[leave_str_sorted] = value
                except ValueError:
                    print(f"Warning: Skipping row {i+1} due to invalid number: {row}")
            else:
                 print(f"Warning: Skipping row {i+1} due to incorrect column count: {row}")
            if (i + 1) % 100000 == 0:
                print(f"  Processed {i+1} rows...")

    print(f"Loaded {len(leave_lookup_table)} entries in {time.time() - start_time:.2f} seconds.")

    print(f"Saving dictionary to {pickle_filename}...")
    save_start = time.time()
    with open(pickle_filename, 'wb') as pf:
        pickle.dump(leave_lookup_table, pf, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Dictionary saved in {time.time() - save_start:.2f} seconds.")

except FileNotFoundError:
    print(f"Error: {csv_filename} not found.")
except Exception as e:
    print(f"An error occurred: {e}")
