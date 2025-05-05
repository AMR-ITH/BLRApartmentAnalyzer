import csv
from selectolax.parser import HTMLParser
import httpx
import re
import time
import random

import os

def get_html(url,page_no=None):
    """
    Fetches the HTML content of a given URL and parses it using HTMLParser.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }

    url = url if page_no is None else url + f"-page-{str(page_no)}"


    resp = httpx.get(url, headers=headers, follow_redirects=True,timeout=30)
    try:
        # Perform the GET request
        resp.raise_for_status()

    except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            return False
    html = HTMLParser(resp.text)
    return html



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

def append_to_csv(item):
    field_names = ['apartment_name','appartment_loc','construction_status','carpet_area',
                'bulit_area','super_bulit_area','price_value','nearbylocation','facility']
    file_name = '2bkh_flats.csv'
    file_exists =os.path.exists(file_name)

    with open(file_name,'a',newline='',encoding='utf-8') as file:
        writer = csv.DictWriter(file,fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow(item)





# Scrape data from each individual property page
def html_parser(Fullpage_data_mine,appartment_address):
    href = [each_node.attrs['href'] for each_node in Fullpage_data_mine.css("a.ellipsis")]

    for counter, url in enumerate(href, 0):
        # Parse the individual page
        html = get_html(url)
        print(url)
        # Introduce a random delay # Random delay between 2 to 5 seconds
        delay = random.uniform(1, 3)
        print(f"Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)

        # Skip if the page couldn't be fetched
        if html is None:
            continue


        elif html.css_first('span.component__pdPropAddress') is not None :

            appartment_name_loc = html.css_first('span.component__pdPropAddress').text(strip=True).split(',',
                                                                                                              maxsplit=1)
            appartment_name = appartment_name_loc[0].strip()
            appartment_loc = appartment_name_loc[-1].strip()
            print(f'appratment_name 2:{appartment_name}')
            print(f'appartment_loc 3: {appartment_name_loc}')


            price = html.css_first('#pdPrice').text(strip=True)
            print(price)

            super_built_up_area = html.css_first('#superbuiltupArea_span')
            if super_built_up_area is None:
                super_built_up_area = None
            else:
                super_built_up_area = super_built_up_area.text(strip=True) + ' sq.ft' if super_built_up_area else None


            carpet_area = html.css_first('#carpetArea_span')
            if carpet_area is None:
                carpet_area = None
            else:
                carpet_area = carpet_area.text(strip=True) + ' sq.ft' if carpet_area else None


            built_up_area = html.css_first('#builtupArea_span')

            if built_up_area is None:
                built_up_area = None
            else:
                built_up_area = built_up_area.text(strip=True) + ' sq.ft' if built_up_area else None

            # builtupArea_span
            print(carpet_area)
            print(built_up_area)

            construction_status = html.css_first('#agePossessionLbl')
            construction_status = None if construction_status is None else construction_status.text(strip=True)

            near_by_location = html.css('span.NearByLocation__infoText')
            near_by_location = None if not near_by_location else [each_loc.text() for each_loc in near_by_location]

            facilities = html.css('[data-label="FACILITIES"] ul#features div')
            facilities = None if not facilities else [each_facility.text() for each_facility in facilities]

            print('2 : construction-sattus',facilities)

            yield {
                'apartment_name': appartment_name,
                'appartment_loc':appartment_loc,
                'construction_status': construction_status,
                'carpet_area':carpet_area,
                'bulit_area':built_up_area ,
                'super_bulit_area':super_built_up_area,
                'price_value': price,
                'nearbylocation': near_by_location,
                'facility':facilities

            }


        else:
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

            each_appartment_loc = appartment_address.pop(0)



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
                top_facilities = list(
                    {each_facility.text().strip() for each_facility in facility if each_facility.text().strip()})

            print(f"Fetched apartment name: {apartment_name}")
            print(f'counter : {counter}')
            print(f'construction status : {construction_status}')
            print(f'nearby location : {locations_near_residence}')
            print(f'facilities : {top_facilities}')
            print(f'appatment add: {each_appartment_loc}')
            # print(f"Fetched apartment location: {appratment_loc[counter]}")



            # Store the extracted information
            yield {
                'apartment_name': apartment_name,
                'appartment_loc':each_appartment_loc,
                'construction_status': construction_status,
                'carpet_area': area_price_dict['carpet_area'],
                'bulit_area': area_price_dict['bulit_area'],
                'super_bulit_area': area_price_dict['super_bulit_area'],
                'price_value': area_price_dict['price_value'],
                'nearbylocation': locations_near_residence,
                'facility':top_facilities

            }




def main():
    # Main URL
    base_url = 'https://www.99acres.com/2-bhk-flats-in-bangalore-west-ffid'

    # Parse the main page
    main_html = get_html(base_url)
    print(main_html)

    # page_segements = main_html.css_first('div.Pagination__srpPagination >div').text(strip=True)
    # no_of_pages = int(page_segements.split('of')[-1].strip())
    # print(f'no of pages{no_of_pages}')


    for each_page in range(12,20):
        print(each_page)
        print('#'*100)
        each_page_html = get_html(base_url,page_no=each_page)
        # print(each_page_html.text())
        appartment_loc_type_first = [each_loc.text().split('in')[-1].strip() for each_loc in each_page_html.css('h2.ellipsis')]
        # Introduce a random delay Random delay between 2 to 5 seconds
        delay = random.uniform(1, 3)
        print(f"Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)


        print(appartment_loc_type_first)
        print(len(appartment_loc_type_first))
        # Extract the individual property page URLs
        Fullpage_data_mine = each_page_html.css_first('[data-label="SEARCH"]')

        data = html_parser(Fullpage_data_mine,appartment_loc_type_first)
        for item in data:
            print('*' * 80)
            print(item)
            append_to_csv(item)
            print('*' * 80)






if __name__ == '__main__':
    main()


