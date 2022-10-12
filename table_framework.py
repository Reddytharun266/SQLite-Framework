import sqlite3

MENU_FILE_NAME = 'menu.cfg'
table_name = 'bank'

connect = sqlite3.connect("database.db")
cursor = connect.cursor()

connect.row_factory = sqlite3.Row
cursor = connect.execute('select * from %s'%table_name)
table_headings = cursor.fetchone()
field_names = table_headings.keys()
field_names = tuple(field_names)

fields = []
for field in field_names:
	fields.append((field.replace("_", " ")).capitalize())
	# fields.append((field.replace("_", " ")).title())

def create():
	field_values = ()
	for field_index in range(0, len(field_names)):
		field_values = field_values + (input("Enter %s: "%fields[field_index]), )
	cursor.execute('INSERT INTO %s%s VALUES %s'%(table_name, field_names, field_values))
	save()

def show():
	records = cursor.execute('SELECT * FROM %s'%table_name)
	for record in records:
		display(record)

def update():
	field_value = input("Enter %s to update: "%fields[0])
	for fields_index in range(1, len(fields)):
		print("%d. %s"%(fields_index, fields[fields_index]))
	choice = int(input("Enter your choice to update: "))
	updated_value = input("Enter %s to update: "%fields[choice])
	cursor.execute('UPDATE %s SET %s = "%s" where %s = "%s"'%(table_name, field_names[choice], updated_value, field_names[0], field_value))
	save()

def delete():
	field_value = input("Enter %s: "%fields[0])
	cursor.execute('DELETE FROM %s WHERE %s = "%s"'%(table_name,field_names[0], field_value))
	save()

def search():
	field_value = input("Enter %s to search: "%fields[0])
	records = cursor.execute('SELECT * FROM %s'%table_name)
	for record in records:
		if record[0] == field_value:
			display(record)

def display(record):
	for record_index in range(0, len(fields)): 
		print("%s:"%fields[record_index], record[record_index])

def save():
	connect.commit()

with open(MENU_FILE_NAME) as file:
	menu = file.read()

while True:
	print(menu)
	functions = [create, show, update, delete, search, exit]
	try:
		choice = int(input())
		functions[choice - 1]()
	except ValueError:
		print("Enter a valid input!")
	except IndexError:
		print("Enter a valid choice!")
	except KeyboardInterrupt:
		exit()