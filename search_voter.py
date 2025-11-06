import pandas as pd

# Excel voter list file (Book1.xlsx Repo-യിൽ upload ചെയ്തത്)
file_name = 'Book1.xlsx'

# Excel File open ചെയ്യുക
df = pd.read_excel(file_name)

# Function: search voter by name or family name
def search_voter(name, family=None):
    if family:
        results = df[(df['Name'].str.contains(name, case=False, na=False)) & 
                     (df['Family'].str.contains(family, case=False, na=False))]
    else:
        results = df[df['Name'].str.contains(name, case=False, na=False)]
    return results
