import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def fetch_timetable(url):
    """Fetches the timetable HTML from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    return response.text  # Return HTML content

def extract_timetable(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")

    schedule = defaultdict(list)  # Dictionary to store timetable by day
    week_header = ""

    for row in rows:
        th = row.find("th", colspan="6") # Find start date of the week
        if th:
            week_header = th.text.strip() # Store the start date of the week
            continue  # Skip to next row

        cells = row.find_all("td")
        if len(cells) >= 5:  # Check all columns exist
            date = cells[0].text.strip()
            time = cells[1].text.strip()
            classroom = cells[2].text.strip()
            module = cells[4].text.strip()

            # Reformat module code into simpler abbreviation
            parts = module.split("-")
            if len(parts) >= 4:
                module_code = parts[3]  # Extracts module code
                session_type = parts[-2]  # Extracts "L" or "T"
                session_number = parts[-1]  # Extracts the number
                formatted_module = f"{module_code} ({session_type}{session_number})"
            else:
                formatted_module = module  # Uses original value in case format is different

            # Group by day (e.g., "Mon, 10-Feb-2025" → "Monday")
            day_of_week = date.split(",")[0]  # Extracts "Mon", "Tue", etc.
            schedule[day_of_week].append((time, classroom, formatted_module))

    return week_header, schedule

def main():
    # Prompt user to enter the timetable URL
    print("Note: The URL should be https://api.apiit.edu.my/timetable-print/index.php?Week=...")
    url = input("Paste the timetable URL: ").strip()
    
    # Fetch timetable HTML
    html_content = fetch_timetable(url)
    if not html_content:
        return

    # Extract timetable data
    week_header, schedule = extract_timetable(html_content)

    # Display the timetable
    print(f"\nTimetable for **{week_header}**\n")
    
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_order:
        if day[:3] in schedule:  # Check if the day is on the schedule
            print(f"\n**{day}**")
            for entry in schedule[day[:3]]:
                # Format: Time | Venue | Module
                print(f"{entry[0]} | {entry[1]} | {entry[2]}")
            print("-" * 50)  # Line separator

if __name__ == "__main__":
    main()