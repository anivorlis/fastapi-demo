import csv


def write_data_to_csv(data, filename):
    """Writes temperature data to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['temperature', 'location', 'datetime'])
        for item in data:
            writer.writerow([item.temperature, item.location, item.datetime])