import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import flet as ft
import logging
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
from pathlib import Path
from project_path import ProjectPath

class DataRepository:
    def __init__(self, previewed_data):
        self.previewed_data = previewed_data

    def basic_data_handling(self):
        data = self.previewed_data
        try:
            if not data:
                raise ValueError("No previewed data available.")
            #print(data)

            #excel_file = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/CVapp-the-job/jobs_data.xlsx'
            excel_file = ProjectPath.jobs_data
            existing_df = ProjectPath.existing_df
            #existing_df = pd.read_excel('C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/CVapp-the-job/jobs_data.xlsx', sheet_name='job offers')

            data_job = pd.DataFrame(data)

            print(data_job)

            if existing_df is not None:
                existing_df = pd.read_excel(excel_file, sheet_name='job offers')
            else:
                existing_df = pd.DataFrame()

            data_job = pd.concat([existing_df, data_job], ignore_index=True)
            data_job = data_job.loc[:, ~data_job.columns.str.contains('^Unnamed')]

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                data_job.to_excel(writer, sheet_name='job offers', index=True, header=True)
            
            return "Data successfully processed"
        except Exception as ex:
            logging.error(f"An error occurred: {str(ex)}")
            return f"An error occurred: {str(ex)}"
        finally:
            logging.info('Everything is fine and life is awesome!')

    def process_data(self):
        data = self.previewed_data
        try:
            if not data:
                raise ValueError("No previewed data available.")
            #print(data)

            excel_file = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/CVapp-the-job/jobs_data.xlsx'
            existing_df = pd.read_excel('C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/CVapp-the-job/jobs_data.xlsx', sheet_name=['job_info', 'person_info', 'company_info'])

            data_job = pd.DataFrame(data)
            print(data_job)
            address_df = pd.DataFrame({
                'company_name': data['company_name'],
                'address_street': data['address_street'],
                'address_district': data['address_district']
            })

            person_df = pd.DataFrame({
                'responsible_name': data['responsible_name'],
                'first_number': data['first_number'],
                'second_number': data['second_number']
            })

            job_df = pd.DataFrame({
                'job_name': data['job_name'],
                'text': data['text'],
                'matching_words': data['matching_words'],
                'html_text': data['html_text']
            })

            # Remove Unnamed columns
            address_df = address_df.loc[:, ~address_df.columns.str.contains('^Unnamed')]
            person_df = person_df.loc[:, ~person_df.columns.str.contains('^Unnamed')]
            job_df = job_df.loc[:, ~job_df.columns.str.contains('^Unnamed')]

            # Write to Excel with separate sheets
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                address_df.to_excel(writer, sheet_name='address', index=True, header=True)
                person_df.to_excel(writer, sheet_name='person', index=True, header=True)
                job_df.to_excel(writer, sheet_name='job', index=True, header=True)


            """
            address_df = data[['company_name', 'address_street', 'address_district']]
            person_df = data[['responsible_name', 'first_number', 'second_number']]
            job_df = data[['job_name', 'text', 'matching_words', 'html_text']]

            if existing_df is not None:
                existing_df = pd.read_excel(excel_file, sheet_name=['job_info', 'person_info', 'company_info'])
            else:
                existing_df = pd.DataFrame()

            address_df = pd.concat([existing_df, address_df], ignore_index=True)
            person_df = pd.concat([existing_df, person_df], ignore_index=True)
            job_df = pd.concat([existing_df, job_df], ignore_index=True)

            address_df = address_df.loc[:, ~address_df.columns.str.contains('^Unnamed')]
            person_df = person_df.loc[:, ~person_df.columns.str.contains('^Unnamed')]
            job_df = job_df.loc[:, ~job_df.columns.str.contains('^Unnamed')]

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                job_df.to_excel(writer, sheet_name='job_info', index=True, header=True)
                address_df.to_excel(writer, sheet_name='company_info', index=True, header=True)
                person_df.to_excel(writer, sheet_name='person_info', index=True, header=True)
            """
            return "Data successfully processed"
        except Exception as ex:
            logging.error(f"An error occurred: {str(ex)}")
            return f"An error occurred: {str(ex)}"
        finally:
            logging.info('Everything is fine and life is awesome!')

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
        test_button = ft.ElevatedButton('Write test', on_click=self.button_test)
        self.page.add(
            ft.Row(controls=[self.url]),
            ft.Row(controls=[preview_button, remove_button, write_button, test_button]),

            self.website
        )

    def button_write_to_db(self, e):
        data_repo = DataRepository(self.previewed_data)
        data_repo.basic_data_handling()

    def button_test(self, e):
        data_repo = DataRepository(self.previewed_data)
        data_repo.process_data()

    def get_scraper(self, url):
        if 'jobs.cz' in url:
            return JobsCzScraper(url)
        elif 'karriere.at' in url:
            return KarriereAtScraper(url)
        else:
            raise ValueError('No scraper found for this URL')

    def button_preview(self, e):
        try:
            scraper = self.get_scraper(self.url.value)
            scraper.fetch()
            data = scraper.parse()
            self.display_data(data)
            self.previewed_data.append(data)
        except Exception as ex:
            self.handle_error(f'An error occurred: {str(ex)}')
        finally:
            self.url.value = ''
            self.page.update()
            self.url.focus()

    def handle_error(self, message):
        self.website.controls.append(ft.Text(message))
        logging.error(message)

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