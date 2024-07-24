from collections import UserDict

class Field:
    """Base class for address book record fields"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class for address book record name field"""

class Phone(Field):
    """Class for address book record phone field"""
    def __init__(self, phone: str):
        self.value = self.__validate_phone(phone)

    def __validate_phone(self, phone: str) -> bool:
        """
        Phone validation
        Returns phone if length is 10 and all chars are digits
        """
        if len(phone) != 10:
            raise ValueError("The phone number must contain 10 digits")

        if not phone.isdigit():
            raise ValueError("The phone number must contain only numbers")

        return phone

class Record:
    """Class for address book records with contact name and phone/s"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Method to add phone numbers to contact"""
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        """Method to edit phone number of contact"""
        self.phones = list(
            map(
                lambda phone: Phone(new_phone) if phone.value == old_phone else phone,
                self.phones,
            )
        )

    def remove_phone(self, phone):
        """Method to remove phone number of contact"""
        self.phones = list(filter(lambda phone_number: phone_number == phone, self.phones))

    def find_phone(self, phone):
        """Method to find phone number of contact"""
        return next((phone_number for phone_number in self.phones
                     if phone_number.value == phone), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """Class for address book"""
    def add_record(self, record: Record):
        """Method to add a record to address book"""
        self.data[record.name.value] = record

    def find(self, name):
        """Method to find a record by name"""
        if name not in self.data:
            raise KeyError(f"Record with name '{name}' not found.")
        return self.data.get(name)

    def delete(self, name):
        """Method to delete a record from address book"""
        if name not in self.data:
            raise KeyError(f"Record with name '{name}' not found.")
        del self.data[name]

def main():
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("0937777777")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("0937777777", "0936666666")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
    print("Jane's record deleted.")

    for name, record in book.data.items():
        print(record)

if __name__ == "__main__":
    main()
