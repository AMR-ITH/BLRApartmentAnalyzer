from selectolax.parser import HTMLParser
import httpx
import re
import time
import random

def html_parser(url):
    """
    Fetches the HTML content of a given URL and parses it using HTMLParser.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }
    resp = httpx.get(url, headers=headers, timeout=10)
    try:
        # Perform the GET request
        resp.raise_for_status()

    except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            return False
    html = HTMLParser(resp.text)
    return html

# Main URL
base_url = 'https://www.99acres.com/2-bhk-flats-in-bangalore-south-ffid'

# Parse the main page
main_html = html_parser(base_url)
if main_html is None:
    print("Failed to fetch the main page. Exiting.")
    exit()

# Extract the individual property page URLs
Fullpage_data_mine = main_html.css_first('[data-label="SEARCH"]')
if Fullpage_data_mine is None:
    print("Failed to find the search data. Exiting.")
    exit()

href_each_page = [each_node.attrs['href'] for each_node in Fullpage_data_mine.css("a.ellipsis")]
appratment_loc = [each_node.text() for each_node in Fullpage_data_mine.css('a.ellipsis h2')]

print(appratment_loc)
# print(href_each_page)


# Ensure the extracted links are not empty
if not href_each_page:
    print("No property URLs found. Exiting.")
    exit()


def area_price_residence(list_area_price):

    area_regex = re.compile(r'\d+\s*-\s*\d+\s*[a-z]+\.[a-z]+')
    price_value = list_area_price[1].strip()

    # area_type - carpet,super,builtup
    area_type = list_area_price[0].lower()

    def extract_area(text):
        """Helper function to extract area using regex."""
        match = area_regex.search(text)
        return match.group() if match else None


    if 'carpet' in area_type:

        return {
            'carpet_area':extract_area(area_type),
            'bulit_area':None,
            'super_bulit_area':None,
            'price_value':price_value

        }
    elif 'super' in list_area_price[0].lower():
        return {
            'carpet_area':None,
            'bulit_area':None,
            'super_bulit_area':extract_area(area_type),
            'price_value':price_value

        }
    else:
        try:
            return {
                'carpet_area': None,
                'bulit_area': extract_area(area_type),
                'super_bulit_area': None,
                'price_value': price_value

            }
        except Exception as error:
            return {
                'carpet_area': None,
                'bulit_area': None,
                'super_bulit_area': None,
                'price_value': None
            }

# def extract_text(html,sel):
#     try:
#         return html.css_first(sel).text()
#     except AttributeError:
#         return None



print(href_each_page)

# Scrape data from each individual property page
data = []
for counter,url in enumerate(href_each_page,0):
    # Parse the individual page
    html = html_parser(url)
    print(url)
    # Skip if the page couldn't be fetched
    if html is None:
        continue

    # Extract the apartment name
    apartment_name_node = html.css_first('h1.title_bold')

    # Skip if the name isn't found
    if apartment_name_node is None:
        continue

    # Skip if the name is empty
    apartment_name = apartment_name_node.text().strip()
    if not apartment_name:
        continue

    construction_status = html.css_first('div.ProjectInfo__imgBox1').text()
    construction_status = None if construction_status is None else construction_status


    ## area price content

    area_price_content = html.css_first('div.carousel__CarouselContainer #1_2').text()

    # Check if '₹' is present; if not, continue the loop
    if '₹' not in area_price_content:
        continue

    # Process the text if '₹' is present
    area_price_list = area_price_content.split('₹')

    area_price_dict = area_price_residence(area_price_list)
    print(area_price_dict)

    # Near by location
    near_by_location = html.css_first('[data-label="LOCATION_HIGHLIGHTS"] div.carousel__CarouselContainer')
    locations_near_residence = None
    if near_by_location:
        near_by_location = near_by_location.text().lower()
        pattern = r"([A-Za-z\s\.']*)(\d*\.?\d*\s*[k]ms?|\d+\s*[m]s?)"
        # Find all matches
        locations_near_residence = re.findall(pattern, near_by_location)

    # facilities near the residency
    facility = html.css('div.UniquesFacilities__facilitiesCardWrap  div > div')
    top_facilities = None
    if facility:
        top_facilities=list({each_facility.text().strip() for each_facility in facility if each_facility.text().strip()})


    # Store the extracted information
    data.append({
        'apartment_name': apartment_name,
        'construction_status':construction_status,
        'carpet_area': area_price_dict['carpet_area'],
        'bulit_area': area_price_dict['bulit_area'],
        'super_bulit_area': area_price_dict['super_bulit_area'],
        'price_value': area_price_dict['price_value'],
        'nearbylocation':locations_near_residence

                 })

    print(f"Fetched apartment name: {apartment_name}")
    print(f'counter : {counter}')
    print(f'construction status : {construction_status}')
    print(f'nearby location : {locations_near_residence}')
    print(f'facilities : {top_facilities}')
    # print(f"Fetched apartment location: {appratment_loc[counter]}")
    print('*'*80)

