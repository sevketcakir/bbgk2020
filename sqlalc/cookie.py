from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime

engine = create_engine("sqlite:///cookie.db")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Cookie(Base):
    __tablename__ = "cookies"

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer)
    unit_cost = Column(Numeric(12, 2))

    def __repr__(self):
        return f"""Cookie[cookie_id={self.cookie_id}, 
       cookie_name={self.cookie_name},
       cookie_recipe_url={self.cookie_recipe_url},
       cookie_sku={self.cookie_sku},
       quantity={self.quantity}
       unit_cost={self.unit_cost}]"""


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    shipped = Column(Boolean, default=False)

    user = relationship('User', backref=backref('orders'), order_by=order_id)


class LineItem(Base):
    __tablename__ = 'line_items'

    line_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    cookie_id = Column(Integer, ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer)
    extended_cost = Column(Numeric(12, 2))

    order = relationship("Order", backref=backref('line_items', order_by=order_id))
    cookie = relationship("Cookie", uselist=False)


def create_tables():
    Base.metadata.create_all(engine)

def add_cookies():
    #Bütün kurabiyeleri sil
    #query = session.query(Cookie).all()
    #session.delete(query)
    #session.commit()
    cc_cookie = Cookie(
        cookie_name='chocolate chip',
        cookie_recipe_url='http://some.aweso.me/cookies/recipes/',
        cookie_sku='CC01',
        quantity=12,
        unit_cost=0.5
    )
    session.add(cc_cookie)
    session.commit()
    print(cc_cookie.cookie_id)
    c1 = Cookie(
        cookie_name='peanut butter',
        cookie_recipe_url='http://some.aweso.me/cookies/peanut.html',
        cookie_sku='PB01',
        quantity=24,
        unit_cost=0.25
    )
    c2 = Cookie(
        cookie_name='oatmeal raisin',
        cookie_recipe_url='http://some.aweso.me/cookies/raisin.html',
        cookie_sku='EWW01',
        quantity=100,
        unit_cost=1.0
    )
    session.bulk_save_objects([c1, c2])
    session.commit()
    print(c1.cookie_id, c2.cookie_id)

#add_cookies()

