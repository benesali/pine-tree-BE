from app.db.session import SessionLocal
from app.models.apartment import Apartment
from app.models.building import Building


def main():
    db = SessionLocal()

    b1 = Building(
        slug="pine-tree-house1",
        name="Pine Tree House 1",
        location="Srima I, Croatia",
        description="4 apartments suitable for families up to 6 person. \
        A peaceful location, 200m from the sea, local shop, bike rentals \
        and restaurants or icecream. \
        There is a large playground for children of all ages.",
        is_active=True,
    )

    b2 = Building(
        slug="pine-tree-house2",
        name="Pine Tree House 2",
        location="Srima III, Croatia",
        description="Apartments suitable for families up to 6 person. \
        A peaceful location, 200m from the sea, local shop, bike rentals \
        and restaurants or icecream. \
        There is a large playground for children of all ages.",
        is_active=True,
    )

    db.add_all([b1, b2])
    db.commit()

    apartments = [
        Apartment(
            building_id=b1.id,
            slug="pine-tree-apartment",
            name="Pine Tree Apartment 4+2",
            guests=6,
            bedrooms=2,
            bathrooms=1,
            is_active=True,
        ),
        Apartment(
            building_id=b1.id,
            slug="mayer-apartment",
            name="Mayer Apartment 4+2",
            guests=6,
            bedrooms=2,
            bathrooms=1,
            is_active=True,
        ),
        Apartment(
            building_id=b1.id,
            slug="dario-apartment",
            name="Dario Apartment 4+2",
            guests=6,
            bedrooms=2,
            bathrooms=1,
            is_active=True,
        ),
        Apartment(
            building_id=b1.id,
            slug="tea-apartment",
            name="Tea Apartment 4+2",
            guests=6,
            bedrooms=2,
            bathrooms=1,
            is_active=True,
        ),
        Apartment(
            building_id=b2.id,
            slug="zora-apartment",
            name="Zora Apartment 4+2",
            guests=6,
            bedrooms=2,
            bathrooms=1,
            is_active=True,
        ),
    ]

    db.add_all(apartments)
    db.commit()

    print("Buildings and apartments created successfully.")


if __name__ == "__main__":
    main()
