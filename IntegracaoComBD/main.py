from sqlalchemy import Connection, Inspector, Integer, String, Column, ForeignKey, create_engine, inspect, select

from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, fullname={self.fullname}'


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f'Address(id={self.id}, email-address={self.email_address}'


print(User.__tablename__)
print(Address.__tablename__)

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

isp = inspect(engine)

print(isp.get_table_names())

with Session(engine) as session:
    matheus = User(
        name='Matheus',
        fullname='Matheus Santeago',
        address=[Address(email_address='matheussanteago@email.com')]
    )

    marcos = User(
        name='Marcos',
        fullname='Marcos Silva',
        address=[Address(email_address="marcosilva@email.com"),
                 Address(email_address="marcosilva@email.org")]
    )

    patrick = User(
        name='Patrick',
        fullname='Patrick Bascos Silva',
        address=[Address(email_address="patrickbascos@email.com"),
                 Address(email_address="patricksilva@email.org")]
    )

session.add_all([matheus, marcos, patrick])
session.commit()

stmt = select(User).where(User.name.in_(['Matheus']))
for user in session.scalars(stmt):
    print(user)

order = select(User).order_by(User.fullname.desc())
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)

conn = engine.connect()
results = conn.execute(stmt_join).fetchall()
for r in session.scalars(results):
    print(r)