import pandas as pd

file_countries = 'C:\\Users\\MSI\\Desktop\\countries.csv'

table = pd.read_csv(file_countries, ',')
print('\n1) 10 самых самых больших стран мира по территории:\n')
print(table.nlargest(10, ['area'])['name'])
print('\n1) 10 самых маленьких стран мира по территории:\n')
print(table.nsmallest(10, ['area'])['name'])
print('\n2) 10 самых больших стран мира по населению:\n')
print(table.nlargest(10, ['ccn3'])['name'])
print('\n2) 10 самых маленьких стран мира по населению:\n')
print(table.nsmallest(10, ['ccn3'])['name'])
print('\n3) все франкоязычные страны мира:\n')
print(table[table.languages == 'French']['name'])
print('\n4) только островные государства:\n')
print(table[table.borders.isnull()]['name'])
print('\n5) все страны, находящиеся в южном полушарии:\n')
print(table.where(pd.Series([float(str(i).split(',')[0]) < 0 for i in table.latlng])).name.dropna())

print('\nГруппировка стран по первой букве:\n')
for i, group in table.groupby([i[0] for i in table.name]):
    print(str(i) + ' : ')
    for j, name in enumerate(group.name, 1):
        print(name.split(',')[0])
print('\nГруппировка стран по населению:\n')
for i, group in table.groupby(table.ccn3):
    print(str(i) + ' : ', end='')
    for j, name in enumerate(group.name, 1):
        print(name.split(',')[0])
print('\nГруппировка стран по территории:\n')
for i, group in table.groupby(table.area):
    print(str(i) + ' : ', end='')
    for j, name in enumerate(group.name, 1):
        print(name.split(',')[0])

titles = pd.Series([i.split(',')[0] for i in table.name])
titles.name = 'name'
lat, lng = zip(*[i.split(',') for i in table.latlng])
lat, lng = map(pd.Series, (lat, lng))
lat.name = 'latitude'
lng.name = 'longitude'
output_data = pd.concat([titles, table[['capital', 'ccn3', 'area', 'currencies']], lat, lng], axis=1)
writer = pd.ExcelWriter('C:\\Users\\MSI\\Desktop\\CountriesInfo.xls')
output_data.to_excel(writer, 'Sheet1')
writer.save()