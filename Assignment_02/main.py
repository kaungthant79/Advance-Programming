"""CampusWheels - demonstration program. Run with: python main.py"""

from rental import Vehicle, Renter, ElectricCar, Motorbike


def main():
    print("=== 1. Vehicles and a renter ===")
    yaris = Vehicle("Toyota", "Yaris", "1AB234")
    leaf = ElectricCar("Nissan", "Leaf", "2CD567", 40)
    wave = Motorbike("Honda", "Wave", "3EF890", 125)

    kanya = Renter("Kanya Suwan", 100234)
    print(yaris)
    print(kanya)

    print("\n=== 2. Renting and returning ===")
    print("Before renting:", yaris)
    yaris.rent()
    kanya.rented.append(yaris)
    print("After renting: ", yaris)
    print(kanya)

    yaris.return_vehicle()
    kanya.rented.remove(yaris)
    print("After return:  ", yaris)

    print("\n=== 3. Encapsulation: bad data raises ValueError ===")
    try:
        Renter("", 100234)
    except ValueError as err:
        print("Empty name rejected ->", err)

    try:
        Renter("Somchai", -5)
    except ValueError as err:
        print("Bad licence rejected ->", err)

    try:
        kanya.license_no = 0
    except ValueError as err:
        print("Changing to a bad licence rejected ->", err)

    print("Kanya's licence is still:", kanya.license_no)

    print("\n=== 4. Polymorphism: one list, three formats ===")
    fleet = [yaris, leaf, wave]
    leaf.rent()
    for vehicle in fleet:
        print(vehicle)

    print("\nAll three are Vehicles:")
    for vehicle in fleet:
        print(f"  {type(vehicle).__name__:12} isinstance(Vehicle) = {isinstance(vehicle, Vehicle)}")


if __name__ == "__main__":
    main()
