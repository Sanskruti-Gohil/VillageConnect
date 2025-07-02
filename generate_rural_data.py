import pandas as pd
import random
import string

def generate_village_name():
    return ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10))) + "ville"

def generate_rural_data(n=500):
    data = {
        'village_id': range(1, n + 1),
        'village_name': [generate_village_name() for _ in range(n)],
        'population': [random.randint(100, 2000) for _ in range(n)],
        'healthcare_access': [random.choice(['Yes', 'No']) for _ in range(n)],
        'education_access': [random.choice(['Yes', 'No']) for _ in range(n)],
        'water_supply': [random.choice(['Full', 'Partial', 'None']) for _ in range(n)],
        'electricity': [random.choice(['Yes', 'No']) for _ in range(n)],
        'road_connectivity': [random.choice(['Good', 'Fair', 'Poor']) for _ in range(n)],
        'income_level': [random.choice(['High', 'Medium', 'Low']) for _ in range(n)]
    }
    
    for column in ['village_name', 'healthcare_access', 'education_access', 'water_supply', 'electricity', 'road_connectivity', 'income_level']:
        for i in range(n):
            if random.random() < 0.05:  # 5% chance of missing value
                data[column][i] = None
    
    df = pd.DataFrame(data)
    
    df.to_csv('rural_services_large.csv', index=False)
    print(f"Generated dataset with {n} entries and saved to 'rural_services_large.csv'")
    print(df.head())

if __name__ == "__main__":
    generate_rural_data(500)