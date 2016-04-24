from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, DECIMAL, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

PuppetModel = declarative_base()


class Account(PuppetModel):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column('password_hash', String(100), nullable=False)


class Consignor(PuppetModel):
    __tablename__ = 'consignor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fk_account_id = Column(Integer, ForeignKey(Account.id), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False)

    account = relationship('Account', back_populates='consignors')
    Account.consignors = relationship('Consignor', order_by=id, back_populates='account')


class Address(PuppetModel):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fk_consignor_id = Column(Integer, ForeignKey(Consignor.id), nullable=True, index=True)
    organization_name = Column(String(100), nullable=True)
    unit = Column(String(50), nullable=True)
    sub_premise = Column(String(100), nullable=True)
    premise = Column(String(100), nullable=True)
    thoroughfare = Column(String(100), nullable=True)
    postal_code = Column(String(25), nullable=True)
    dependent_locality = Column(String(100), nullable=True)
    locality = Column(String(100), nullable=True)
    sub_administrative_area = Column(String(100), nullable=True)
    administrative_area = Column(String(100), nullable=True)
    country = Column(String(2), nullable=False)

    consignor = relationship('Consignor', back_populates='addresses')
    Consignor.addresses = relationship('Address', order_by=id, back_populates='consignor')


class AddressGeo(PuppetModel):
    __tablename__ = 'address_geography'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fk_address_id = Column(Integer, ForeignKey(Address.id), nullable=True, index=True)
    latitude = Column(DECIMAL(8, 6), nullable=True)
    longitude = Column(DECIMAL(9, 6), nullable=True)
    accuracy = Column('geo_accuracy', Integer, nullable=True)

    address = relationship('Address', back_populates='geographies')
    Address.geographies = relationship('AddressGeo', order_by=id, back_populates='address')


class AddressContact(PuppetModel):
    __tablename__ = 'address_contact'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fk_address_id = Column(Integer, ForeignKey(Address.id), nullable=True, index=True)
    email = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone_country = Column(String(2), nullable=False)
    phone_number = Column(Integer, nullable=False)
    phone_extension = Column(Integer, nullable=True)

    address = relationship('Address', back_populates='contacts')
    Address.contacts = relationship('AddressContact', order_by=id, back_populates='address')


class AddressDispatchTime(PuppetModel):
    __tablename__ = 'address_dispatch_time'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fk_address_id = Column(Integer, ForeignKey(Address.id), nullable=True, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    address = relationship('Address', back_populates='dispatch_times')
    Address.dispatch_times = relationship('AddressDispatchTime', order_by=id, back_populates='address')
