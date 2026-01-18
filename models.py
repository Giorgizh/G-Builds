from flask_login import UserMixin
from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="comments")


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(255), nullable=False, default="defaultuser_img.jpg")
    email = db.Column(db.String(), unique=True, nullable=False)
    role = db.Column(db.String(), default="Guest")


    def __init__(self, username, password, role="Guest", email="", image=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.image = image or "defaultuser_img.jpg"
        self.role = role
        self.email = email


    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Motherboard(db.Model):
    __tablename__ = "motherboards"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    socket = db.Column(db.String(), nullable=True)
    chipset = db.Column(db.String(), nullable=True)
    ram_type = db.Column(db.String(), nullable=True)
    ram_slots = db.Column(db.String(), nullable=True)
    wifi = db.Column(db.String(), nullable=True)
    motherboard_size = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="motherboard")


class CPU(db.Model):
    __tablename__ = "cpus"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    cpu_type = db.Column(db.String(), nullable=True)
    cpu_model = db.Column(db.String(), nullable=True)
    socket = db.Column(db.String(), nullable=True)
    cores_threads = db.Column(db.String(), nullable=True)
    integrated_graphics = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="cpu")


class CpuCooler(db.Model):
    __tablename__ = "cpucoolers"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    cooler_type = db.Column(db.String(), nullable=True)
    radiator_size = db.Column(db.String(), nullable=True)
    fan_size = db.Column(db.String(), nullable=True)
    noise_level = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)
    
    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="cpucooler")



class RAM(db.Model):
    __tablename__ = "rams"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    ram_type = db.Column(db.String(), nullable=True)
    capacity = db.Column(db.String(), nullable=True)
    speed = db.Column(db.String(), nullable=True)
    lighting = db.Column(db.String(), nullable=True)
    Color = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="ram")


class GPU(db.Model):
    __tablename__ = "gpus"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    gpu = db.Column(db.String(), nullable=True)
    memory = db.Column(db.String(), nullable=True)
    numcoolers = db.Column(db.Integer(), nullable=True)
    Ports = db.Column(db.String(), nullable=True)
    lighting = db.Column(db.String(), nullable=True)
    color = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="gpu")



class PSU(db.Model):
    __tablename__ = "psus"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand= db.Column(db.String(), nullable=True)
    brandimg=db.Column(db.String(), default="default_img.webp")
    wattage=db.Column(db.Integer(), nullable=True)
    efficiency=db.Column(db.String(), nullable=True)
    modular=db.Column(db.String(), nullable=True)
    lighting=db.Column(db.String(), nullable=True)
    color=db.Column(db.String(), nullable=True)
    condition=db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="psu")


class HDD(db.Model):
    __tablename__ = "hdds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    capacity = db.Column(db.String(), nullable=True)
    rpm = db.Column(db.String(), nullable=True)
    cache = db.Column(db.String(), nullable=True)
    interface = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="hdd")


class SSD(db.Model):
    __tablename__ = "ssds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand= db.Column(db.String(), nullable=True)
    brandimg=db.Column(db.String(), default="default_img.webp")
    capacity=db.Column(db.String(), nullable=True)
    read_speed=db.Column(db.String(), nullable=True)
    write_speed=db.Column(db.String(), nullable=True)
    interface=db.Column(db.String(), nullable=True)
    condition=db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="ssd")



class M2(db.Model):
    __tablename__ = "m2s"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand= db.Column(db.String(), nullable=True)
    brandimg=db.Column(db.String(), default="default_img.webp")
    capacity=db.Column(db.String(), nullable=True)
    read_speed=db.Column(db.String(), nullable=True)
    write_speed=db.Column(db.String(), nullable=True)
    interface=db.Column(db.String(), nullable=True)
    condition=db.Column(db.String(), nullable=True)
    
    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="m2")



class CaseItem(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand= db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    compatability = db.Column(db.String(), nullable=True)
    casetype = db.Column(db.String(), nullable=True)
    color = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)

    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="cases")


class Cooler(db.Model):
    __tablename__ = "coolers"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), default="default_img.webp")
    img1 = db.Column(db.String(), default="default_img.webp")
    img2 = db.Column(db.String(), default="default_img.webp")
    img3 = db.Column(db.String(), default="default_img.webp")
    img4 = db.Column(db.String(), default="default_img.webp")
    
    brand = db.Column(db.String(), nullable=True)
    brandimg = db.Column(db.String(), default="default_img.webp")
    numoffans = db.Column(db.Integer(), nullable=True)
    size = db.Column(db.String(), nullable=True)
    lighting = db.Column(db.String(), nullable=True)
    color = db.Column(db.String(), nullable=True)
    condition = db.Column(db.String(), nullable=True)


    stock = db.Column(db.Integer(), default=0)
    product_type = db.Column(db.String(), default="casefan")

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    stock = db.Column(db.Integer())
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)

class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  
    product_id = db.Column(db.Integer)
    product_type = db.Column(db.String())
    name = db.Column(db.String())
    price = db.Column(db.Float())
    stock = db.Column(db.Integer())


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="paid")
    
    image_snapshot = db.Column(db.String(255))

    total_price = db.Column(db.Float, default=0)

    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")



class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)

    image_snapshot = db.Column(db.String(255))

    product_type = db.Column(db.String(50))
    product_id = db.Column(db.Integer)

    name_snapshot = db.Column(db.String(200), nullable=False)
    price_snapshot = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
