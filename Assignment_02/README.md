# Assignment 02 — CampusWheels Vehicle-Rental Desk

192-201 Advanced Computer Programming with Generative AI
Siam University — Faculty of Information Technology (International)

## Files

- `rental.py` — the classes: `Vehicle`, `Renter`, `ElectricCar`, `Motorbike`
- `main.py` — a short demonstration program
- `README.md` — this file

## How to run

Python 3.8 or newer is needed. From inside the `Assignment_02` folder:

```bash
python main.py
```

(On some systems use `python3 main.py`.)

## What the program shows

1. Creating vehicles and a renter, and printing them.
2. Renting a vehicle and returning it — the printed line changes from
   `[available]` to `[rented]` and back.
3. Encapsulation — creating a `Renter` with an empty name or a licence number
   that is zero or negative raises `ValueError`. The same check runs again if
   the value is changed later, because `name` and `license_no` are `@property`
   values stored privately as `_name` and `_license_no`.
4. Polymorphism — a `Vehicle`, an `ElectricCar` and a `Motorbike` are put in one
   list and printed in a loop. Each one prints in its own format because each
   class overrides `__str__`.

## Note on AI use
I used an AI assistant to explain object-oriented concepts, in particular how
`@property` getters and setters work and why the setter also runs during
`__init__`. I wrote and tested the code myself and can explain each part of it.
