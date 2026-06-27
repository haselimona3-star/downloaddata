import os
import urllib.request

ID = 40754  # Tehran
location = "C:/Users/Arghavan Computer/.spyder-py3/"
name = "sounding_raw_data_2023.txt"

start_year = 2023
start_month = 1 
start_day = 1
start_hour = 0

end_year = 2023
end_month = 12
end_day = 31
end_hour = 12

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
if is_leap(start_year):
    days_in_month[1] = 29

output_file = os.path.join(location, name)

def get_url(year, month, day, hour, station_id):
    return (
        f"http://weather.uwyo.edu/cgi-bin/sounding?"
        f"region=mideast&TYPE=TEXT%3ALIST&YEAR={year}"
        f"&MONTH={month:02d}&FROM={day:02d}{hour:02d}&TO={day:02d}{hour:02d}&STNM={station_id}"
    )

def download_raw_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

def write_raw_data_file():
    with open(output_file, 'w', encoding='utf-8') as f:
        y, m, d, h = start_year, start_month, start_day, start_hour
        done = False

        while not done:
            url = get_url(y, m, d, h, ID)
            print(f"Downloading: {url}")
            content = download_raw_data(url)

            if content:
                header = f"\n--- {y:04d}-{m:02d}-{d:02d} {h:02d}:00 UTC ---\n"
                f.write(header)
                f.write(content)
                print("✓ Data written")
            else:
                print("✗ Failed to download")

            # Time increment
            if y == end_year and m == end_month and d == end_day and h == end_hour:
                done = True
            else:
                h += 12
                if h >= 24:
                    h = 0
                    d += 1
                    if d > days_in_month[m-1]:
                        d = 1
                        m += 1
                        if m > 12:
                            m = 1
                            y += 1
                            days_in_month[1] = 29 if is_leap(y) else 28

    print(f"\n✓ All data saved in: {output_file}")

if __name__ == "__main__":
    write_raw_data_file()
