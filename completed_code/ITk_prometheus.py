import json
from prometheus_client import start_http_server, Gauge

def categorize_data(data, threshold):
    categorized_data = []

    for array in data:
        categorized_array = []
        for value in array:
            if value > threshold:
                categorized_array.append("hit")
            else:
                categorized_array.append("no-hit")
        categorized_data.append(categorized_array)

    return categorized_data

def count_hits_no_hits(categorized_data):
    total_hits = 0
    total_no_hits = 0

    for array in categorized_data:
        total_hits += array.count("hit")
        total_no_hits += array.count("no-hit")

    return total_hits, total_no_hits

def sort_by_index(i):
    if 0 <= i <= 127:
        return "syn"
    elif 128 <= i <= 263:
        return "lin"
    elif 264 <= i <= 400:
        return "diff"
    else:
        return "invalid"

def main():
    # Read data from the .json file
    with open("JohnDoe_0_NoiseMap-0.json", "r") as json_file:
        json_data = json.load(json_file)

    data_arrays = json_data["Data"]

    threshold = 200

    # Categorize the data arrays based on the threshold
    categorized_data = categorize_data(data_arrays, threshold)

    # Count the total hits and no-hits
    total_hits, total_no_hits = count_hits_no_hits(categorized_data)

   # Initialize dictionaries to store total hits and no-hits for each category
    total_hits_dict = {"syn": 0, "lin": 0, "diff": 0}
    total_no_hits_dict = {"syn": 0, "lin": 0, "diff": 0}

    # Loop through the categorized data to count hits and no-hits for each category
    for i, array in enumerate(categorized_data):
        category = sort_by_index(i)
        total_hits_dict[category] += array.count("hit")
        total_no_hits_dict[category] += array.count("no-hit")

     # Print the total hits and no-hits for each category
    print("Total Hits:")
    for category, total_hits in total_hits_dict.items():
        print("{}: {}".format(category, total_hits))

    print("Total No Hits:")
    for category, total_no_hits in total_no_hits_dict.items():
        print("{}: {}".format(category, total_no_hits))

    # Create Prometheus Gauge objects for total hits and no-hits
    hits_gauge = Gauge("hits_total", "Total hits for each category", ["category"])
    #no_hits_gauge = Gauge("no_hits_total", "Total no-hits for each category", ["category"])

    # Update Prometheus Gauges with total hits and no-hits for each category
    for category, total_hits in total_hits_dict.items():
        hits_gauge.labels(category=category).set(total_hits)

    #for category, total_no_hits in total_no_hits_dict.items():
     #   no_hits_gauge.labels(category=category).set(total_no_hits)

    # Push the metrics to Prometheus Pushgateway
    #registry = CollectorRegistry()
    #push_to_gateway("130.246.43.14:8000", job="sensor", registry=registry)
    start_http_server(8000)
    print("Prometheus ITk metrics server started")

if __name__ == "__main__":
    main()
