import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import flet as ft
"""
import os

# not elegant, but sort of working. Not suprisingly only on tested device :(
os.chdir("..")
os.chdir("..")
os.chdir("Projekt/CVapp-the-job")
current_directory = os.getcwd()
print(current_directory)
"""
class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f'Failed to retrieve the webpage. Status code: {response.status_code}')

    def get_substrings(self):
        # pak tahat z databáze
        return ['SQL', 'warehouse', 'oracle', 'azure'] 
    
    def clean_word(self, word):
        return re.sub(r'[)(,.:]', '', word)

    def run(self):
        self.fetch()
        data = self.parse()
        self.print_data(data)

class JobsCzScraper(BaseScraper):
    def parse(self):
        # Call the base class fetch method to populate self.soup
        super().fetch()

        # Now self.soup contains the parsed HTML, ready for parsing specific elements
        address_street, address_city, address_district = self.parse_address()
        first_number, second_number = self.parse_phone_numbers()
        formatted_text = self.parse_text_html()
        data = {
            'job_name': self.parse_job_name(),
            'company_name': self.parse_company_name(),
            'address_street': address_street,
            'address_city': address_city,
            'address_district': address_district,
            'text': self.parse_text(),
            'responsible_name': self.parse_responsible_name(),
            'first_number': first_number,
            'second_number': second_number,
            'matching_words': self.parse_matching_words(),
            'text': self.parse_text(),
            'html_text': self.parse_text_html(),
        }
        return data

    def parse_job_name(self):
        return self.soup.find('h1', class_='typography-heading-medium-text').get_text()

    def parse_company_name(self):
        return self.soup.find('p', class_='typography-body-medium-text-regular').get_text() 

    def parse_address(self):
        address = self.soup.find('a', class_='link-secondary link-underlined').get_text()
        address_parts = re.split(r',\s*|\s*–\s*', address)

        address_street = address_parts[0].strip() if len(address_parts) > 0 else ''
        address_city = address_parts[1].strip() if len(address_parts) > 1 else ''
        address_district = ' '.join(address_parts[2:]).strip() if len(address_parts) > 2 else ''

        return address_street, address_city, address_district

    def parse_text(self):
        # gets entire offer's text
        text_content = []
        content_container = self.soup.find('div', class_='RichContent mb-1400')

        for string in content_container.stripped_strings:
            text_content.append(string + '\n') 

        formatted_text = ''.join(text_content).strip()
        return formatted_text
    
    def parse_text_html(self):
        # html content, probably should go to the database to be formattable
        html_content = []

        content_container = self.soup.find('div', class_='RichContent mb-1400') 

        def extract_html(element):
            if isinstance(element, Tag):
                # Start tag
                html_content.append(f'<{element.name}>')
                for content in element.contents:
                    extract_html(content)
                # End tag
                html_content.append(f'</{element.name}>')
            elif isinstance(element, NavigableString):
                html_content.append(str(element))

        extract_html(content_container)

        html_content = ''.join(html_content).strip()
        return html_content
    
    def parse_responsible_name(self):
        footer_name = self.soup.find('a', class_='link-primary text-primary').get_text()
        return footer_name.strip()
    
    def parse_phone_numbers(self):
        footer_number = self.soup.find('p', class_='typography-body-medium-text-regular mr-500').get_text()
        responsible_number_parts = footer_number.split(',')

        first_number = responsible_number_parts[0].strip() if len(responsible_number_parts) > 0 else ''
        second_number = responsible_number_parts[1].strip() if len(responsible_number_parts) > 1 else ''

        return first_number, second_number

    def parse_matching_words(self):
        paragraphs = self.soup.find_all('p', class_='typography-body-large-text-regular mb-800')
        substrings = self.get_substrings()
        matching_words = []

        for paragraph in paragraphs:
            words = paragraph.get_text().split()
            for word in words:
                cleaned_word = self.clean_word(word)
                for substring in substrings:
                    if re.search(re.escape(substring), cleaned_word, re.IGNORECASE):
                        matching_words.append(cleaned_word)
                        break 

        matching_words = list(set(matching_words)) 

        return matching_words

class KarriereAtScraper(BaseScraper):
    def parse(self):
        # Implement parsing logic specific to karriere.at
        pass

#-----------------------------------------------------------------------------------------------------
# Database logic, later into DB
import openpyxl
import os
import pandas as pd

class DataRepository:
    def __init__(self, previewed_data): 
        self.scraper_app = previewed_data

    def testing(self):
        try:
            data = self.scraper_app.previewed_data
            if not data:
                raise ValueError("No previewed data available.")
            
            job_data = {
                'job_name': data['job_name'],
                'text': data['text'],
                'html_text': data['html_text'],
            }
            data_job = pd.DataFrame.from_dict(job_data, orient='index')
            print(data_job)

            excel_file = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/CVapp-the-job/jobs_data.xlsx'

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                data_job.to_excel(writer, sheet_name='job offers', index=False, header=False)

            return "Data successfully processed"
        except Exception as ex:
            return f"An error occurred: {str(ex)}"
        finally:
            print('Everything is fine and life is awesome!')

    def process_data(self):
        try:
            data = self.scraper_app.previewed_data
            if not data:
                raise ValueError("No previewed data available.")
            else:
                job_data = {
                    'job_name': data['job_name'],
                    'text': data['text'],
                    'html_text': data['html_text'],
                }
                data_job = pd.DataFrame.from_dict(job_data, orient='index')
                print(data_job)

            excel_file = 'outputs/jobs_data.xlsx'

            if os.path.exists(excel_file):
                print(f"Appending data to existing file: {excel_file}")
                with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl') as writer:
                    data_job.to_excel(writer, sheet_name='job offers', index=False, header=False)
            else:
                print(f"Creating new file: {excel_file}")
                os.makedirs(os.path.dirname(excel_file), exist_ok=True)
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    data_job.to_excel(writer, sheet_name='job offers', index=False)

            return "Data successfully processed"
        except Exception as ex:
            return f"An error occurred: {str(ex)}"
        finally: 
            print('Everything is fine and life is awesome!')
    
    """ Data handling logic ideas:
    address_data = {
    'Street': data['address_street'],
    'City': data['address_city'],
    'District': data['address_district']
    }
    data_address = pd.DataFrame.from_dict(address_data, orient='index', columns=['Value'])

    other_data = {
        'Job Name': data['job_name'],
        'Company': data['company_name'],
        'Responsible Person': data['responsible_name'],
        'Matching Words': data['matching_words'],
        'Additional Text': data['text'],
        'HTML Text': data['html_text']
    }
    data_other = pd.DataFrame.from_dict(other_data, orient='index', columns=['Value'])

    # Print the DataFrames (you can adjust this as needed)
    print("Address Data:")
    print(data_address)
    print("\nOther Data:")
    print(data_other)

    """

#-----------------------------------------------------------------------------------------------------
# Design logic, later dissect into specific files and modules

class ScraperApp:
    def __init__(self, page):
        self.page = page
        self.website = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.website.style = {'overflow': 'auto', 'max-height': '500px'}
        self.url = ft.TextField(label='Insert URL address', width=300)
        self.setup_ui()
        self.previewed_data = []

    def setup_ui(self):
        preview_button = ft.ElevatedButton('Offer preview', on_click=self.button_preview)
        remove_button = ft.ElevatedButton('Remove text', on_click=self.button_remove)
        write_button = ft.ElevatedButton('Write to database', on_click=self.button_write_to_db)
        test_button = ft.ElevatedButton('Test button', on_click=self.button_testing)
        self.page.add(
            ft.Row(controls=[self.url]),
            ft.Row(controls=[preview_button, remove_button, write_button, test_button]),

            self.website
        )

    def button_preview(self, e):
        try:
            if 'jobs.cz' in self.url.value:
                scraper = JobsCzScraper(self.url.value)
            elif 'karriere.at' in self.url.value:
                scraper = KarriereAtScraper(self.url.value)
            else:
                raise ValueError('No scraper found for this URL')
            scraper.fetch()
            data = scraper.parse()
            self.display_data(data)
            self.previewed_data.append(data)
        except Exception as ex:
            self.website.controls.append(ft.Text(f'An error occurred: {str(ex)}'))
        finally:
            self.url.value = ''
            self.page.update()
            self.url.focus()

    def button_testing(self, e):
        DataRepository.testing(self.previewed_data)
    
    def button_write_to_db(self, e):
        try:
            if 'jobs.cz' in self.url.value:
                scraper = JobsCzScraper(self.url.value)
            elif 'karriere.at' in self.url.value:
                scraper = KarriereAtScraper(self.url.value)
            else:
                raise ValueError('No scraper found for this URL')
            scraper.fetch()
            data = scraper.parse()
            self.display_data(data)
            self.previewed_data.append(data)

            job_data = {
            'job_name': data['job_name'],
            'text': data['text'],
            'html_text': data['html_text'],
            }

            data_job = pd.DataFrame(job_data, index=[0])
            print(data_job)
            excel_file = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/CVapp-the-job/jobs_data.xlsx'

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                data_job.to_excel(writer, sheet_name='job offers', index=True, header=True)

        except Exception as ex:
            self.website.controls.append(ft.Text(f'An error occurred: {str(ex)}'))
        finally:
            self.url.value = ''
            self.page.update()
            self.url.focus()
        """
        try:
            data = self.previewed_data
            if not data:
                raise ValueError("No previewed data available.")

            if not isinstance(data, dict):
                raise ValueError("Previewed data must be a dictionary.")

            job_data = {
                data['job_name']: 1,
                data['text']: 2,
                data['html_text']:3,
            }
            data_job = pd.DataFrame(job_data, orient='index')

            excel_file = 'jobs_data.xlsx'

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                data_job.to_excel(writer, sheet_name='job offers', index=False, header=False)

            self.website.controls.clear()
            self.page.update()
            self.website.controls.append(ft.Text(f'Your data have been successfully imported'))

        except Exception as ex:
            self.website.controls.clear()
            self.page.update()
            self.website.controls.append(ft.Text(f'An error occurred: {str(ex)}'))

        finally:
            self.page.update()
            self.url.focus()
        """

    def display_data(self, data):
        self.website.controls.clear()
        self.website.controls.extend([
            ft.Text(f"Position name: {data['job_name']}"),
            ft.Text(f"Company: {data['company_name']}"),
            ft.Text(f"Street: {data['address_street']}"),
            ft.Text(f"City: {data['address_city']}"),
            ft.Text(f"City district: {data['address_district']}"),
            ft.Text(f'Responsible person: {data["responsible_name"]}'),
            ft.Text(f'Phone number 1: {data["first_number"]}'),
            ft.Text(f'Phone number 2: {data["second_number"]}'),
            ft.Text(f'Matching words: {data["matching_words"]}'),
            ft.Text(f'{data["text"]}'),
            ft.Text(data["html_text"]),
        ])
        self.page.update()

    def button_remove(self, e):
        self.website.controls.clear()
        self.page.update()

def main(page):
    app = ScraperApp(page)

if __name__ == "__main__":
    ft.app(target=main)


# tested on: 
# https://www.jobs.cz/rpd/2000147251/?searchId=c2227d40-dc5b-47f1-b6bd-37a9caefcdd4&rps=233
# https://www.jobs.cz/fp/asb-czech-republic-s-r-o-233975/2000176507/?searchId=5b2e93b9-305a-443a-87dd-e647bfdf8e7c&rps=329 

""""
logika pro tahání tříd z jiných souborů:
from jobs_cz_scraper import JobsCzScraper

soubor jobs_cz_scraper.py bude mít třídu:
class JobsCzScraper:
    # Your scraping logic here
    ...
"""