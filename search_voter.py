import pandas as pd

file_name = 'Book1.xlsx'
df = pd.read_excel(file_name)

# Headings match your Excel
serial_col      = 'Serial No.'
name_col        = 'Name'
guardian_col    = "Guardian's Name"
ward_house_col  = 'OldWard No/ House No.'
house_name_col  = 'House Name'
party_col       = 'Political Party'

# Function: update voter's party
def update_party(serial_no, new_party):
    df.loc[df[serial_col] == serial_no, party_col] = new_party

# Example: update serial no. 3 to 'NDA'
update_party(3, 'NDA')

# Save changes back (optional): df.to_excel(file_name, index=False)

# Party-wise vote tally
votes_by_party = df[party_col].value_counts()
print("\nVoter count by party:\n", votes_by_party)

# Leading party & margin
top_two = votes_by_party.nlargest(2)
if len(top_two) == 2:
    margin = top_two.iloc[0] - top_two.iloc[1]
    print("\nLeading party:", top_two.index[0])
    print("Victory margin:", margin)
else:
    print("\nNot enough data to compute margin.")

# Print voters for all parties
for party in votes_by_party.index:
    party_voters = df[df[party_col] == party]
    print(f"\nVoters for {party}:")
    print(party_voters[[serial_col, name_col, guardian_col, ward_house_col, house_name_col, party_col]])
