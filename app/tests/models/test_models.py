from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.amenity import Amenity
from app.models.apartment import Apartment
from app.models.availability import Availability, AvailabilityStatus
from app.models.review import Review


@pytest.mark.integration
def test_review_relationship(db):
    apt = Apartment(slug="apt-1", name="Apt 1", location="X", description="d")
    db.add(apt)
    db.commit()

    rev = Review(apartment_id=apt.id, author_name="Joe", text="Nice place")
    db.add(rev)
    db.commit()

    # reload apartment and assert backref
    db.refresh(apt)
    assert any(r.id == rev.id for r in apt.reviews)


@pytest.mark.integration
def test_amenity_association(db):
    apt = Apartment(slug="apt-amenity", name="Apt A", location="Y", description="d")
    am = Amenity(code="wifi", label="WiFi")
    db.add_all([apt, am])
    db.commit()

    # associate and commit
    apt.amenities.append(am)
    db.commit()

    db.refresh(apt)
    assert any(a.id == am.id for a in apt.amenities)


@pytest.mark.integration
def test_availability_unique_constraint(db):
    day = date(2025, 8, 1)
    a1 = Availability(apartment_id=5, date=day, status=AvailabilityStatus.blocked)
    db.add(a1)
    db.commit()

    a2 = Availability(apartment_id=5, date=day, status=AvailabilityStatus.reserved)
    db.add(a2)
    with pytest.raises(IntegrityError):
        db.commit()
    # rollback to keep DB clean for other tests
    db.rollback()
