import csv
from .models import MGNREGAData

def load_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            MGNREGAData.objects.create(
                fin_year=row.get('fin_year'),
                month=row.get('month'),
                state_code=row.get('state_code'),
                state_name=row.get('state_name'),
                district_code=row.get('district_code'),
                district_name=row.get('district_name'),
                approved_labour_budget=float(row.get('Approved_Labour_Budget') or 0),
                average_wage_rate=float(row.get('Average_Wage_rate_per_day_per_person') or 0),
                total_expenditure=float(row.get('Total_Exp') or 0),
                total_households_worked=int(row.get('Total_Households_Worked') or 0),
                women_persondays=float(row.get('Women_Persondays') or 0)
            )
            count += 1
            print(f"{count} rows done.")
        print(f"✅ Imported {count} rows successfully.")
