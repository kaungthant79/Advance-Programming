"""CampusWheels - vehicle rental desk classes.

Contains: Vehicle, Renter, ElectricCar, Motorbike
"""


class Vehicle:
    """An ordinary vehicle at the rental desk."""

    def __init__(self, make, model, plate):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = False

    def rent(self):
        """Mark this vehicle as rented out."""
        self.is_rented = True

    def return_vehicle(self):
        """Mark this vehicle as available again."""
        self.is_rented = False

    def status(self):
        """Helper: the word shown in __str__."""
        return "rented" if self.is_rented else "available"

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate}) [{self.status()}]"


class Renter:
    """A member who can rent vehicles.

    name and license_no are validated every time they are set,
    including when the object is first created.
    """

    def __init__(self, name, license_no):
        # These go through the property setters, so the checks run here too.
        self.name = name
        self.license_no = license_no
        self.rented = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("name must not be empty")
        self._name = value

    @property
    def license_no(self):
        return self._license_no

    @license_no.setter
    def license_no(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("license_no must be a number")
        if value <= 0:
            raise ValueError("license_no must be a positive number")
        self._license_no = value

    def __str__(self):
        return f"Renter: {self.name} (licence {self.license_no}), {len(self.rented)} vehicle(s) rented"


class ElectricCar(Vehicle):
    """A car that runs on a battery."""

    def __init__(self, make, model, plate, battery_kwh):
        super().__init__(make, model, plate)
        self.battery_kwh = battery_kwh

    def __str__(self):
        return (
            f"[EV] {self.make} {self.model} ({self.plate}) "
            f"- {self.battery_kwh} kWh battery - {self.status()}"
        )


class Motorbike(Vehicle):
    """A motorbike, described by its engine size."""

    def __init__(self, make, model, plate, engine_cc):
        super().__init__(make, model, plate)
        self.engine_cc = engine_cc

    def __str__(self):
        return (
            f"Motorbike >> {self.make} {self.model} / {self.engine_cc}cc "
            f"/ plate {self.plate} / {self.status()}"
        )
