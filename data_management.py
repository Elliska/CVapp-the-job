import openpyxl
import os
import pandas as pd
from pathlib import Path
from project_path import ProjectPath
import logging

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