import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_clean_data(file_path):
    print("=== Step 1: Loading and Cleaning Data ===")
    
    df = pd.read_csv(file_path)
    print("Initial Dataset (first 5 rows):")
    print(df.head())
    print("\nDataset Info:")
    print(df.info())
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    df['village_id'] = df['village_id'].fillna(df['village_id'].max() + 1)
    df['village_name'] = df['village_name'].fillna('Unknown')
    df['healthcare_access'] = df['healthcare_access'].fillna('No')
    df['education_access'] = df['education_access'].fillna('No')
    df['water_supply'] = df['water_supply'].fillna('None')
    df['electricity'] = df['electricity'].fillna('No')
    df['road_connectivity'] = df['road_connectivity'].fillna('Poor')
    df['income_level'] = df['income_level'].fillna('Low')
    
    categorical_cols = ['healthcare_access', 'education_access', 'water_supply', 
                       'electricity', 'road_connectivity', 'income_level']
    for col in categorical_cols:
        df[col] = df[col].str.title()
    
    print("\nDuplicates:", df.duplicated().sum())
    df = df.drop_duplicates()
    
    df.to_csv('rural_services_cleaned.csv', index=False)
    print("\nCleaned Dataset (first 5 rows):")
    print(df.head())
    return df

def create_sqlite_database(df):
    """Store the cleaned dataset in a SQLite database."""
    print("\n=== Step 2: Creating SQLite Database ===")
    
    conn = sqlite3.connect('villageconnect.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rural_services (
            village_id INTEGER PRIMARY KEY,
            village_name TEXT,
            population INTEGER,
            healthcare_access TEXT,
            education_access TEXT,
            water_supply TEXT,
            electricity TEXT,
            road_connectivity TEXT,
            income_level TEXT
        )
    ''')
    
    df.to_sql('rural_services', conn, if_exists='replace', index=False)
    
    cursor.execute('SELECT * FROM rural_services LIMIT 5')
    print("Data in SQLite (first 5 rows):")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()

def perform_eda(df):
    print("\n=== Step 3: Exploratory Data Analysis ===")
    
    sns.set_style('whitegrid')
    
    print("Summary Statistics:")
    print(df.describe(include='all'))
    
    print("\nHealthcare Access Counts:")
    print(df['healthcare_access'].value_counts())
    print("\nEducation Access Counts:")
    print(df['education_access'].value_counts())
    print("\nWater Supply Counts:")
    print(df['water_supply'].value_counts())
    
    # Population distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['population'], bins=20, kde=True)
    plt.title('Population Distribution Across Villages')
    plt.xlabel('Population')
    plt.ylabel('Count')
    plt.savefig('population_distribution.png')
    plt.close()
    
    # Healthcare access by income level
    plt.figure(figsize=(10, 6))
    sns.countplot(x='healthcare_access', hue='income_level', data=df)
    plt.title('Healthcare Access by Income Level')
    plt.savefig('healthcare_by_income.png')
    plt.close()
    
    df_numeric = df.copy()
    df_numeric['healthcare_access'] = df_numeric['healthcare_access'].map({'Yes': 1, 'No': 0})
    df_numeric['education_access'] = df_numeric['education_access'].map({'Yes': 1, 'No': 0})
    df_numeric['water_supply'] = df_numeric['water_supply'].map({'Full': 2, 'Partial': 1, 'None': 0})
    df_numeric['electricity'] = df_numeric['electricity'].map({'Yes': 1, 'No': 0})
    df_numeric['road_connectivity'] = df_numeric['road_connectivity'].map({'Good': 2, 'Fair': 1, 'Poor': 0})
    df_numeric['income_level'] = df_numeric['income_level'].map({'High': 2, 'Medium': 1, 'Low': 0})
    
    df_numeric = df_numeric.drop(columns=['village_id', 'village_name'])
    
    # Correlation matrix
    plt.figure(figsize=(12, 8))
    sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Rural Services')
    plt.savefig('correlation_matrix.png')
    plt.close()
    
    # Water supply by income level
    plt.figure(figsize=(10, 6))
    sns.countplot(x='income_level', hue='water_supply', data=df)
    plt.title('Water Supply by Income Level')
    plt.savefig('water_by_income.png')
    plt.close()
    
    # Population vs. road connectivity
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='population', y='road_connectivity', hue='income_level', size='income_level', data=df)
    plt.title('Population vs. Road Connectivity by Income Level')
    plt.savefig('population_vs_roads.png')
    plt.close()
    
    return df, df_numeric

def document_insights(df, df_numeric):
    print("\n=== Step 4: Key Insights ===")
    insights = f"""
    - Population Distribution: Villages have populations between 100–2000, with most around {int(df['population'].mean())} (mean).
    - Service Access: Approximately {100 * df['healthcare_access'].value_counts(normalize=True)['Yes']:.1f}% of villages have healthcare access, and {100 * df['education_access'].value_counts(normalize=True)['Yes']:.1f}% have education access.
    - Income Correlation: Income level shows moderate to strong correlations with road connectivity (corr: {df_numeric['income_level'].corr(df_numeric['road_connectivity']):.2f}) and electricity access (corr: {df_numeric['income_level'].corr(df_numeric['electricity']):.2f}).
    - Water Supply: Villages with higher income levels are more likely to have 'Full' water supply.
    """
    print(insights)
    
    with open('insights.txt', 'w') as f:
        f.write("VillageConnect Insights\n")
        f.write("=" * 20 + "\n")
        f.write(insights)

def main():
    print("VillageConnect: Rural Services Analysis")
    print("=" * 40)
    
    df = load_and_clean_data('rural_services_large.csv')
    
    create_sqlite_database(df)
    
    df, df_numeric = perform_eda(df)
    
    document_insights(df, df_numeric)
    
    print("\nAnalysis complete. Check output files and visualizations.")

if __name__ == "__main__":
    main()