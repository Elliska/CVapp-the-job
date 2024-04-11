import flet as ft
import logging
import web_scraper
import data_management

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
        data_repo = data_management.DataRepository(self.previewed_data)
        data_repo.basic_data_handling()

    def button_test(self, e):
        data_repo = data_management.DataRepository(self.previewed_data)
        data_repo.process_data()

    def get_scraper(self, url):
        if 'jobs.cz' in url:
            return web_scraper.JobsCzScraper(url)
        elif 'karriere.at' in url:
            return web_scraper.KarriereAtScraper(url)
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

