# calculate days between dates
from datetime import datetime

def days_between_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    return delta.days

def main():from datetime import datetime

def days_between_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    return delta.days



if __name__ == "__main__":
    # Get current date and time
    current_date_time = datetime.now()
    print("Current date and time: ", current_date_time)

    start_date = "2021-01-01"
    end_date = "2021-01-31"
    print(days_between_dates(start_date, end_date))
