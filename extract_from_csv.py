import pandas as pd



artistes_filepath = "C:/Users/utilisateur/Desktop/Dev/Ressources/artistes.csv"
chansons_filepath = "C:/Users/utilisateur/Desktop/Dev/Ressources/chansons.csv"

artistes_info = {}
chansons_info = {}

        
artistes_df = pd.read_csv(artistes_filepath)
chansons_df = pd.read_csv(chansons_filepath)

for header in artistes_df.columns: artistes_info[header] = ()
for header in chansons_df.columns: chansons_info[header] = ()


for column in artistes_info:
    column_content = artistes_df[column]
    processed_content = []
    for c in column_content:
        if type(c) in (int, float): processed_content.append(c)
    if processed_content == []: continue 
    artistes_info[column] = (" min : " + str(min(column_content)),  "max : " +  str(max(column_content)))



for column in chansons_info:
    column_content = chansons_df[column]
    processed_content = []
    for c in column_content:
        if type(c) in (int, float): processed_content.append(c)
    if processed_content == []: continue  
    chansons_info[column] = (" min : " + str(min(processed_content)),  "max : " +  str(max(processed_content)))

for h in artistes_info: print(h, artistes_info[h])
print("\n\n")
for h in chansons_info: print(h, chansons_info[h])



#saved_column = df.column_name #you can also use df['column_name']
