from collections import UserDict
import re, pickle
import datetime as dt
from abc import ABC, abstractmethod

class Field():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def get_name(self) -> str:
        return str(self.value)

class Phone(Field):
# реалізація класу Phone:
# Реалізовано валідацію номера телефону (перевірка на 10 цифр).        
    def get_phone(self) -> str: 
            pattern_delete = r"[^\d]"   # створення патерну для відкидання зайвих елементів
            replacement_symbol = "" 
            number_just = re.sub(pattern_delete, replacement_symbol, self.value) #видалення будь-яких знаків, окрім цифр
            number_just = number_just.split("0", maxsplit=1) #розділення рядків за 0
            number_just[0] = "+380" # заміна першого підрядка
            self.value = "".join(number_just) #об'єднання рядків
            return str(self.value)

class Birthday(Field):
    def get_birthday(self):
        try:
            dateobjects_entered = dt.datetime.strptime(self.value, '%d-%m-%Y')
            data_second = dateobjects_entered.date() 
            self.value = data_second
            return self.value
        except Exception:
            raise ValueError("Invalid date format.\nUse DD-MM-YYYY")
        
    def get_date(self) -> str:
        self.val = dt.datetime.strftime(self.value, "%d-%m-%Y")
        return self.val

class Record():
    # реалізація класу
    def __init__(self, name):
        self.name = Name(name).get_name()  # Реалізовано зберігання об'єкта Name в окремому атрибуті.
        self.phones:list = []  # Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
        self.birthday: str = ''

# додавання 
    def add_phone(self, phone):
        if phone: 
            self.phones.append(phone)
        return self.phones
            
# видалення
    def remove_phone(self, phone): 
        phone_obj = Phone(phone).get_phone()
        self.phones.remove(phone_obj)

# редагування 
    def edit_phone(self, phone, new_phone): 
        phone_obj = Phone(phone).get_phone()
        new_phone_obj = Phone(new_phone).get_phone()
        if phone_obj in self.phones: 
            self.phones.remove(phone_obj) 
            self.phones.append(new_phone_obj)
            print("Changes made")
            return self.phones
        else:
            print(" Phone is not in list")
            return None
                
# пошук об'єктів Phone
    def find_phone(self, phone):
        phone_obj = Phone(phone).get_phone()
        if phone_obj in self.phones:
            return self.phones
        else:
            print ("Don't find this number")

    def add_birthday(self, bthday): #додаємо до контакту день народження в форматі DD.MM.YYYY
        self.bthday = Birthday(bthday).get_date()
        self.birthday = self.bthday
        return self.birthday
 
    def __str__(self):
        return f"\nIt's automatically printed.\nContact name: {self.name}, phones: {self.phones}\n"
"""
data = {name:phones}
new.data = {'Name': {Phones: 'Phones', Birthday: 'Birthday'}, 'Other_Name': {Phones: 'Phones', Birthday: 'Birthday'} }
info = new.data['Name']
new.data['Name'][Phones] = ['380687811111',]
new.data['Name'][birthday] = birthday
"""
class AddressBook(UserDict):
    def __init__(self):
        self.data={} # словник- книга контактів

 # Реалізовано метод add_record, який додає запис до self.data.  
    def add_record(self, contact: Record):
        self.name  = contact.name
        if self.name in self.data:
            if 'phones' in self.data[self.name]:
                list_phones:list = self.data[self.name]['phones']
                list_phones.append(contact.phones)
                print(f"New phone added.")
        else:    
            self.data[self.name] = {'phones': contact.phones}  # Якщо не існує дата контакту
            print(f"Contact phone added.")
        return self.data
    
    def add_birthday_record(self, contact : Record):
        self.birthday = contact.birthday
        self.name= contact.name
        if self.name in self.data:
            self.data[self.name]['birthday'] = self.birthday
        else:
            self.data[self.name] = {'birthday': self.birthday}
        print(f"Birthday added. \nName: {contact.name}, birthday: {self.data[self.name]['birthday']}")
        return self.data

    def find(self, name): # Реалізовано метод find, який знаходить запис за ім'ям.
        self.name = name
        if self.name in self.data.keys():
                p = Record(name) #реалізація Record-обєкту
                p.name = name 
                p.phones = self.data[self.name]['phones']
                return p       # повернення Record() обєкту
        else:
                print (f"Don't find this name: {name}")
                return None
    
    def find_bthday(self, name): #показуємо день народження контакту
        self.name = name
        for key in self.data:
            if self.name in str(key):
                # print(f"Contact found. \nName: {self.name}, birthday: {self.data[self.name]["birthday"]}")
                p = Record(name) #реалізація Record-обєкту
                p.name = name 
                p.birthday = self.data[self.name]["birthday"]
                return p       # повернення Record() обєкту
            else:
                print (f"Don't find this name: {name}")
                return None
    # код привітання з дн на 7 днів вперед з різницею від словника з датами
    def get_upcoming_birthdays(self):
        tdate= dt.datetime.today().date() # беремо сьогоднішню дату
        upcoming_birthdays=[] # створюємо список для результатів
        for user, info in self.data.items(): # перебираємо користувачів
            for key in info:
                if key =='birthday':
                    bdate = info['birthday'] # отримуємо дату народження людини   
                    bdate = str(bdate[:6])+str(tdate.year) # Замінюємо рік на поточний
                    bdate=dt.datetime.strptime(bdate, "%d-%m-%Y").date() # перетворюємо дату народження в об’єкт date
                    week_day=bdate.isoweekday() # Отримуємо день тижня (1-7)
                    days_between=(bdate-tdate).days # рахуємо різницю між зараз і днем народження цьогоріч у днях
                    if 0<=days_between<7: # якщо день народження протягом 7 днів від сьогодні
                        if week_day<6: #  якщо пн-пт
                            upcoming_birthdays.append({'name': user, 'birthday': bdate.strftime("%d-%m-%Y")}) 
                            # Додаємо запис у список.
                        else:
                            if (bdate+dt.timedelta(days=1)).weekday()==0:# якщо неділя
                                upcoming_birthdays.append({f"{user}, 'birthday':{(bdate+dt.timedelta(days=1)).strftime("%d-%m-%Y")}"})
                                #Переносимо на понеділок. Додаємо запис у список.
                            elif (bdate+dt.timedelta(days=2)).weekday()==0: #якщо субота
                                upcoming_birthdays.append({f"{user}, 'birthday':{(bdate+dt.timedelta(days=2)).strftime("%d-%m-%Y")}"})
                                #Переносимо на понеділок. Додаємо запис у список.
        if not upcoming_birthdays :
            return "There are no contacts scheduled for greetings in the next week."
        else:
            return upcoming_birthdays
    # Реалізовано метод delete, який видаляє запис за ім'ям.
    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            print(f"Record for '{name}' deleted successfully.")
        else:
            print(f"Record for '{name}' not found in the address book.")

def parse_input(user_input): #функція, яка приймає введений рядок. ділить та сортує дані.
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func): # декоратор- обробка помилок при введенні
    def inner(args, contacts):
        try:
            if args[0].isdigit():
                raise ValueError
            else:
                name = args[0]
                if name in contacts:
                    print("\nThis name is in your contacts\n") 
                    if len(args) == 1:
                        print("\n->Give me name and phone please.")
                        return None
                    else:
                        if args[1].isdigit() and len(args[1])>= 10:
                            return func(args, contacts)
                        else:
                            print("\n->Phone number must contain at least 10 numbers.")
                            return None
                else:
                    print("\nIt seems to be a new contact\n") 
                    if len(args) == 1:
                        print("\n->Give me name and phone please.")
                        return None
                    else:
                        if args[1].isdigit() and len(args[1])>= 10:
                            return func(args, contacts)
                        else:
                            print("\n->Phone number must contain at least 10 numbers.")
                            return None
               
        except ValueError:
            return "\n->Give me name and phone please."
        except KeyError:
            return "\n->Is a key error. You should check it and repeat."
        except IndexError:
            return "\n->What's wrong?\nRepeat this, correctly please."
            # return "Phone must be a number"
    return inner


# operations with contacts
@input_error
def add_contact(args, contacts) -> Record:# функція додає дані в словник
    name, phone = args
    name = Name(args[0]).get_name()
    phone = Phone(args[1]).get_phone()
    record = Record(name)
    record.add_phone(phone)
    return record
    
@input_error
def check_contact(args, contacts):#фукнція змінює номер телефону, якщо імя співпадає
    return args

def added_date(args, contacts) -> Record:
    name, date = args
    name = Name(args[0]).get_name()
    date = Birthday(args[1]).get_birthday()
    rec = Record(name)
    rec.add_birthday(date)
    return  rec         

# operations with save-data file
def load_data(filename = "addressbook.pkl") ->  AddressBook:
    try:
        with open(filename, "rb") as f:
            saved_file = pickle.load(f)
            return saved_file
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def save_data(contacts):
    with open("addressbook.pkl", "wb") as file:
        pickle.dump(contacts, file)
        return print("Saved")
#  додаткові можливості виведення
class Bot(ABC):
    def __init__(self) -> None:
        super().__init__()
    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()

class WelcomeBot(Bot):
    def welcome(self):
        return ("How can I help you?")
    
    def helping(self):
        return ("\nI have some list of commands. If you need this - enter \"help\"\nPress \"hello\" to start")
    
    def __str__(self) -> str:
        return ("_____________\nHello.\nI'm glad to see you")
       
help_list: list =[
        ['add (name) (phone)                -> for add a new contacts to me'],
        ['change (name) (phone) (new_phone) -> for change contacts i have'],
        ['all                               -> to see all contacts i save'],
        ['delete (name)                     -> to delete one contact'],
        ['show (name)                       -> to see number of somebody'],
        ['congrats                          -> for get some list - shedule to greeting' ],
        ['add-birthday (name) (birthday)    -> for add a birthday date to me'],
        ['show-birthday (name)              -> to see birthday date of somebody'],
        ['close or exit                     -> for save and exit'],
        ['print                             -> just for typing and testing']
        ]
# виведення списка HELP
class HelpBot(Bot):
    
    def __init__(self, list) -> None:
        self.list = list

    def __str__(self) -> str:
        for el in self.list:
            print(el)
        return "---DONE---"

# ідея в виведенні інформації в табличці.
class Table(ABC, AddressBook):
    def __init__(self, contacts = AddressBook):
        self.contacts= contacts.data
    #  self.data[name]={[phone]='1354', [date] = '25.02.1511'}
    def __str__(self) -> str: 
        print('{n:<15s} {d:<15s} {f:<15s}'.format(n = "NAME", d = "BIRTHDAY", f = "PHONE NUMBER"))
        for self.name, record in self.contacts.items():
            record: dict
            for key in record:
                if 'phones' == key:
                    if 'birthday' == key:
                        self.date = record['birthday']
                        self.phone:list = record['phones']
                    else:
                        self.date:str ="----------"
                        self.phone:list = record['phones']
                elif 'birthday' == key:
                        self.date = record['birthday']
                        self.phone :str= ['-------------']
                else:
                    return ("SOMETHING WRONG IN SEARCH\nTry again")
            if len(self.phone)==1:
                print('{n:<15s} {d:<15s} {f:<15s}'.format(n = self.name, d = self.date, f = str(self.phone)))
            else:
                for el in self.phone:
                    print('{n:<15s} {d:<15s} {f:<15s}'.format(n = self.name, d = self.date, f = el))
        return "-----DONE-----"
                  
def main():#основна функція
    # contacts  = AddressBook()
    contacts: AddressBook = load_data()
    print(WelcomeBot(), WelcomeBot().helping())
    while True:
        # try:
            user_input  = input("\n>>>Enter a command: ")
            command, *args = parse_input(user_input)
            if command in ["close", "exit"]:
                save_data(contacts)
                print("Good bye!")
                break
            elif command == "hello":
                print(WelcomeBot().welcome())
            elif command == "add": # додає контакт, обробляється декоратором
                rec = add_contact(args, contacts)
                contacts.add_record(rec)
            elif command == "change": # змянює контакт, обробляється декоратором
                check = check_contact(args, contacts)  
                john = contacts.find(check[0])
                john.edit_phone(check[1], check[2])
            elif command == "all": # друкує контакти зі словника. якщо пусто - нічого не друкує
                print(Table(contacts))
            elif command =="print":
                for name, record in contacts.data.items():
                    print(name," ----",record)
            elif command == "show": # показує номер за наданим іменем, працює коректно
                result = contacts.find(args[0])
                print(f"Contact {args[0]} : phones {result.phones}")
            elif command == "add-birthday":
                res = added_date(args, contacts)
                contacts.add_birthday_record(res)
            elif command == "show-birthday":
                list_btday = contacts.find_bthday(args[0])
                print(f" Contact {args[0]} : birthday {list_btday.birthday}")
            elif command == "congrats":
                congrats= contacts.get_upcoming_birthdays()
                print(HelpBot(congrats))
            elif command == "delete": # працює коректно, видаляє запис про поданого користувача повністю
                contacts.delete(args[0])
            elif command == "help": # команда-підказка вводу даних для користувача
                print(HelpBot(help_list))
            else:
                print("Invalid command.\nTry one more time")
        # except Exception as e:
            # print(f"\n{e}\n Plese, try again.")
                
if __name__ == "__main__":
    main()