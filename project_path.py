from pathlib import Path
import pandas as pd

class ProjectPath:
    root = Path(__file__).parent
    jobs_data = root/'jobs_data.xlsx'
    existing_df = pd.read_excel(jobs_data, sheet_name='job offers')

