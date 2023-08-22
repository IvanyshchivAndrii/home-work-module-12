from collections import UserDict
from datetime import datetime
import re
import pickle
from pathlib import Path


class AddressBook(UserDict):

    def __init__(self, counter_index=0, *args, **kwargs):
        self.counter_index = counter_index
        super().__init__(*args, **kwargs)

    def add_record(self, record):
        self.data[record.name.value] = record

    def __next__(self):
        if self.counter_index < len(self.data):
            dct_keys = {key: value for key, value in enumerate(self.data.keys())}
            gen_value = self.data[dct_keys[self.counter_index]]
            gen_key = list(self.data.keys())[self.counter_index]
            self.counter_index += 1
            return gen_value
        raise StopIteration

    def iterator(self, num=None):
        count = 0
        if num is None or num == 0:
            return self.data
        else:
            while count < num:
                yield self.__next__()
                count += 1


class AddressBookGenerator:

    def __init__(self, generator):
        self.__generator = generator

    def __iter__(self):
        return self.__generator


class Record:
    def __init__(self, name, phone=None, bday=None):
        self.name = name
        if isinstance(phone, Phone):
            self.phones = [phone]
        else:
            self.phones = []
        self.birthday = bday

    def add_phone(self, phone):
        phones_list = [phone.phone for phone in self.phones]
        if phone.phone not in phones_list and phone.phone != None:
            self.phones.append(phone)
        else:
            print(f'{phone.phone} already exist!')

    def remove_phone(self, phone):
        phones_dict = {phone.phone: index for index, phone in enumerate(self.phones)}
        if phone.phone in phones_dict.keys():
            del self.phones[phones_dict[phone.phone]]
        else:
            print(f'Sorry, {phone.phone} wasn\'t founded. Try again.')

    def change_phone(self, from_phone, to_phone):
        phones_dict = {phone.phone: index for index, phone in enumerate(self.phones)}
        if from_phone.phone in phones_dict.keys():
            self.phones[phones_dict[from_phone.phone]] = to_phone
        else:
            print(f'Sorry, {from_phone.phone} wasn\'t founded. Try again.')

    def days_to_birthday(self):
        if self.birthday:
            current_day = datetime.now()
            birthday = datetime(current_day.year, self.birthday.month, self.birthday.day)
            if birthday > current_day:
                time_delta = birthday - current_day
                return time_delta.days if time_delta.days != 365 else 0
            else:
                birthday = datetime(current_day.year + 1, self.birthday.month, self.birthday.day)
                time_delta = birthday - current_day
                return time_delta.days if time_delta.days != 365 else 0
        else:
            print('Add birthday to contact')

    def __str__(self):
        return f'{self.name} {self.phones} {self.birthday}'

    def __repr__(self):
        return f'{self.name} {self.phones} {self.birthday}'


class Field:
    pass


class Name(Field):
    def __init__(self, name: str):
        self.__value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name):
        self.__value = name

    def __str__(self):
        return self.__value


class Phone(Field):
    def __init__(self):
        self.__phone = None

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        try:
            checked_phone = re.match(r'\+380\d{9}', phone).group(0)
            if len(phone) == 13 and checked_phone == phone:
                self.__phone = phone
            else:
                print('Write correct number')

        except AttributeError:
            print('Write correct number')

    def __str__(self):
        return self.__phone

    def __repr__(self):
        return self.__phone


class Birthday(Field):
    def __init__(self):
        self.__year = None
        self.__month = None
        self.__day = None

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year: str):
        if year.isdigit():
            self.__year = int(year)
        else:
            print('Year must be number')

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, month: str):
        if month.isdigit():
            self.__month = int(month)
        else:
            print('Month must must be number from 1 to 12')

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day: str):
        if day.isdigit():
            self.__day = int(day)
        else:
            print('Day must be number')


def input_error(func):
    def inner(*args):
        try:
            if 1 < len(args) <= 2 and args[0] not in ['phone', 'del']:
                print('Enter telephone number')
            elif len(args) <= 1 and args[0] == 'phone':
                print('Enter Username')
            elif len(args) <= 1 and args[0] in ['add']:
                print('Enter Username and telephone number')
            elif len(args) <= 2 and args[0] in ['add', 'change']:
                print('Enter Username and telephone number')
            elif len(args) <= 3 and args[0] in ['change']:
                print('Enter 2nd telephone number')
            elif len(args) > 3 and len(args) < 6 and args[0] in ['new']:
                print('Enter year month day of birthday through a space')
            else:
                return func(*args)
        except KeyError:
            print('Enter existing or correct username')
        except IndexError as e:
            print(e)

    return inner


def helper(*args):
    print('hello - print "say hello',
          'add - adding Name and Phone. You have to enter Name and Phone through a space',
          'change - changing Phone of user Name. You have to enter user nave and new Phone through a space',
          'phone - showing Phone of user. You have to enter username',
          'show all - showing all contacts', sep='\n')
    return ''


def say_hallo(*args):
    print("How can I help you?")
    return ''


with open('PhonePook.bin', 'rb') as fh:
    if Path('PhonePook.bin').stat().st_size != 0:
        PHONEBOOK = pickle.load(fh)
    else:
        PHONEBOOK = AddressBook()


@input_error
def add_contact(*args):
    name = Name(args[1].title())
    phone = Phone()
    phone.phone = args[2]
    if len(args) > 3:
        birthday = Birthday()
        birthday.year = args[3]
        birthday.month = args[4]
        birthday.day = args[5]
        record = Record(name, phone, birthday)
    else:
        record = Record(name, phone)
    if phone.phone:
        PHONEBOOK.add_record(record)
        print(f'Contact {args[1].title()} {args[2]} has been added to PHONEBOOK')
    return ''


@input_error
def delete_contact(*args):
    if args[1].title() in PHONEBOOK:
        PHONEBOOK.pop(args[1].title())
        print(f'Contact {args[1].title()} has been deleted from PHONEBOOK')
    else:
        print(f'Contact {args[1].title()} does not exist!!')
    return ''


@input_error
def add_phone_to_contact(*args):
    if args[1].title() in PHONEBOOK:
        phone = Phone()
        phone.phone = args[2]
        if phone.phone != None:
            PHONEBOOK[args[1].title()].add_phone(phone)
            print(f'Phone {args[2]} has been added to contact {args[1].title()}')
    else:
        print(f'Contact {args[1].title()} does not exist!!')
    return ''


@input_error
def remove_phone_contact(*args):
    if args[1].title() in PHONEBOOK:
        phone = Phone()
        phone.phone = args[2]
        if phone.phone:
            PHONEBOOK[args[1].title()].remove_phone(phone)
            print(f'Phone {args[2]} has been removed from contact {args[1].title()}')
    return ''


@input_error
def change_contact(*args):
    old_phone = Phone()
    old_phone.phone = args[2]
    new_phone = Phone()
    new_phone.phone = args[3]
    if args[1].title() in PHONEBOOK and (old_phone.phone != None and new_phone.phone != None):
        PHONEBOOK[args[1].title()].change_phone(old_phone, new_phone)
        print(f'Phone {old_phone.phone} in PHONEBOOK has been changed to {new_phone.phone}')
    else:
        print(f'There is no {args[1].title()} in PHONEBOOK or check changing numbers!')
    return ''


@input_error
def show_phone(*args):
    print(f'The number you have searched: {list(i.phone for i in PHONEBOOK[args[1].title()].phones)}')
    return ''


def show_all_contacts(*args):
    try:
        num, name, tel, bday = '№', 'Name', 'Phones', 'Birthday'
        if args[0] != 0:
            print(f'|{num:^5}|{name:^10}|{tel:^15}|{bday:^15}|')
            for k, v in enumerate(PHONEBOOK.iterator(int(args[0]))):
                phones_list = ', '.join(i.phone for i in v.phones)
                len_num = len(phones_list) if len(phones_list) > 15 else 15
                if v.birthday:
                    days_to_bday = v.days_to_birthday()
                    print(f'|{k:^5}|{v.name:^10}|{phones_list:^{len_num}}|{days_to_bday:^15}|')
                else:
                    text = 'not indicated'
                    print(f'|{k:^5}|{v.name.value:^10}|{phones_list:^{len_num}}|{text:^15}|')
        else:
            print(f'|{num:^5}|{name:^10}|{tel:^15}|{bday:^15}|')
            for k, v in enumerate(PHONEBOOK):
                phones_list = ', '.join(i.phone for i in PHONEBOOK[v].phones)
                len_num = len(phones_list) if len(phones_list) > 15 else 15
                if PHONEBOOK[v].birthday:
                    days_to_bday = v.days_to_birthday()
                    print(f'|{k:^5}|{v:^10}|{phones_list:^{len_num}}|{days_to_bday:^15}|')
                else:
                    text = 'not indicated'
                    print(f'|{k:^5}|{v:^10}|{phones_list:^{len_num}}|{text:^15}|')
    except RuntimeError:
        print('Phone book is finished')
    return ''


def find_record(*args):
    rec_list_name = [values for key, values in PHONEBOOK.items() if args[1] in key.lower() and args[1].isalpha()]
    rec_list_num = [values for key, values in PHONEBOOK.items() if args[1] in ''.join(str(values.phones))]
    if rec_list_name:
        for i in rec_list_name:
            print(i)
    elif rec_list_num:
        for i in rec_list_num:
            print(i)
    else:
        print('Sorry contact hasn\'t been found')


OPERATIONS = {
    'hello': say_hallo,
    'new': add_contact,
    'del': delete_contact,
    'add': add_phone_to_contact,
    'remove': remove_phone_contact,
    'change': change_contact,
    'phone': show_phone,
    'show all': show_all_contacts,
    'help': helper,
    'find': find_record
}


def get_hendler(*args):
    return OPERATIONS[args[0]]


def main():
    flag = True
    print('Hello!! This is your phonebook assistant. Let\'s start!!')
    try:
        while flag:
            request = input('Enter request>>>').lower()
            request_list = request.split()

            if request_list[0] in list(OPERATIONS):
                get_hendler(*request.split())(*request.split())
            elif ' '.join(request_list[0:2]) == 'show all':
                if len(request_list) >= 3:
                    show_all_contacts(request_list[2])
                else:
                    request_list.append(0)
                    show_all_contacts(request_list[2])
            elif request in ['exit', 'close', 'good bye']:
                flag = False
            else:
                print('Please, write one of the command')
        with open('PhonePook.bin', 'wb') as fh:
            pickle.dump(PHONEBOOK, fh)
    except IndexError:
        print('Enter command and values')


if __name__ == '__main__':
    main()
