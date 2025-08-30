import csv

def label_data():
    """
    Reads URLs from test_wineries.txt, asks the user to label them,
    and saves the results to labeled_data.csv.
    """
    labeled_data = []
    try:
        with open('test_wineries.txt', 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: test_wineries.txt not found. Please create this file with one URL per line.")
        return

    print("Please label the following URLs as 'wine' or 'not-wine'.")
    print("Enter 'y' for wine, 'n' for not-wine, or 's' to skip.")

    for url in urls:
        while True:
            response = input(f"URL: {url}\nIs this a wine page? (y/n/s): ").lower()
            if response in ['y', 'n', 's']:
                break
            else:
                print("Invalid input. Please enter 'y', 'n', or 's'.")

        if response == 'y':
            label = 'wine'
        elif response == 'n':
            label = 'not-wine'
        else:
            continue  # Skip this URL

        labeled_data.append({'url': url, 'label': label})

    if not labeled_data:
        print("No data was labeled. Exiting.")
        return

    # Save to CSV
    with open('labeled_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['url', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(labeled_data)

    print(f"\nLabeled data saved to labeled_data.csv. Total labeled URLs: {len(labeled_data)}")

if __name__ == '__main__':
    label_data()
