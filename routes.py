from itertools import product
from flask import render_template, request , redirect,flash, url_for, jsonify,session
from forms import RegisterForm,ProductForm,LoginForm
from ext import app,db
from models import Comment,Motherboard,CPU,GPU,CpuCooler,RAM,PSU,SSD,M2,CaseItem,Cooler,HDD,User,CartItem,WishlistItem,Order,OrderItem
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["PARTS_FOLDER"] = "static/images/parts"
app.config["MOBO_FOLDER"] = "static/images/parts/mobo"
app.config["CPU_FOLDER"] = "static/images/parts/cpu"
app.config["CPUCOOLER_FOLDER"] = "static/images/parts/cpucooler"
app.config["RAM_FOLDER"] = "static/images/parts/ram"
app.config["GPU_FOLDER"] = "static/images/parts/gpu"
app.config["PSU_FOLDER"] = "static/images/parts/psu"
app.config["HDD_FOLDER"] = "static/images/parts/hdd"
app.config["SSD_FOLDER"] = "static/images/parts/ssd"
app.config["M2_FOLDER"] = "static/images/parts/m2"
app.config["CASE_FOLDER"] = "static/images/parts/case"
app.config["CASEFAN_FOLDER"] = "static/images/parts/casefan"
app.config["BRANDS_FOLDER"] = "static/images/brands"


def get_products_by_mobo():
    items = Motherboard.query.all()
    mobos = []
    for idx, p in enumerate(items):
        mobos.append({
            "number": idx,
            "name": p.name,
            "brand": p.brand,
            "condition": p.condition,
            "socket": p.socket,
            "ram": p.ram_type,
            "size": p.motherboard_size,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "stock": p.stock,
            "id": p.id,
        })
    return mobos
def get_products_by_cpu():
    items = CPU.query.all()
    cpus = []
    for idx, p in enumerate(items):
        cpus.append({
            "number": idx,
            "name": p.name,
            "brand": p.brand,
            "condition": p.condition,
            "socket": p.socket,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "id": p.id,
            "stock": p.stock,
        })
    return cpus
def get_products_by_cpucooler():
    items = CpuCooler.query.all()
    cpucoolers = []
    for idx, p in enumerate(items):
        cpucoolers.append({
            "number": idx,
            "name": p.name,
            "brand": p.brand,
            "condition": p.condition,
            "cooler_type": p.cooler_type,
            "radiator_size": p.radiator_size,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "id": p.id,
            "stock": p.stock,
        })
    return cpucoolers
def get_products_by_ram():
    items = RAM.query.all()
    rams = []
    for idx, p in enumerate(items):
        rams.append({
            "number": idx,
            "name": p.name,
            "brand": p.brand,
            "condition": p.condition,
            "type": p.ram_type,          
            "color": p.Color,
            "capacity": p.capacity,  
            "speed": p.speed,        
            "rgb": p.lighting,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "id": p.id,
            "stock": p.stock,
        })
    return rams
def get_products_by_gpu():
    items = GPU.query.all()
    gpus = []
    for idx, p in enumerate(items):
        gpus.append({
            "number": idx,
            "name": p.name,
            "description": p.description,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "brand": p.brand,
            "gpu": p.gpu,            
            "memory": p.memory,         
            "numcoolers": p.numcoolers, 
            "lighting": p.lighting,     
            "color": p.color,
            "condition": p.condition,
            "id": p.id,
            "stock": p.stock,
        })
    return gpus
def get_products_by_psu():
    items = PSU.query.all() 
    psus = []

    for idx, p in enumerate(items):
        psus.append({
            "number": idx,
            "name": p.name,
            "description": p.description,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "brand": p.brand,
            "wattage": p.wattage,
            "efficiency": p.efficiency,
            "lighting": p.lighting,  
            "color": p.color,
            "condition": p.condition,
            "id": p.id,
            "stock": p.stock,
        })

    return psus
def get_products_by_hdd():
    items = HDD.query.all()
    hdds = []
    for idx, p in enumerate(items):
        hdds.append({
            "number": idx,
            "name": p.name,
            "description": p.description,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "brand": p.brand,
            "capacity": p.capacity,  
            "rpm": p.rpm,            
            "cache": p.cache,        
            "interface": p.interface,
            "condition": p.condition,
            "id": p.id,
            "stock": p.stock,
        })
    return hdds
def get_products_by_ssd():
    items = SSD.query.all()
    ssds = []
    for idx, p in enumerate(items):
        ssds.append({
            "number": idx,
            "name": p.name,
            "description": p.description,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "brand": p.brand,
            "capacity": p.capacity,
            "read_speed": p.read_speed,
            "write_speed": p.write_speed,
            "interface": p.interface,
            "condition": p.condition,
            "id": p.id,
            "stock": p.stock,
        })
    return ssds
def get_products_by_m2():
    items = M2.query.all()
    m2s = []
    for idx, p in enumerate(items):
        m2s.append({
            "number": idx,
            "id": p.id,
            "name": p.name,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "brand": p.brand,
            "condition": p.condition,
            "capacity": p.capacity,
            "read_speed": p.read_speed,
            "write_speed": p.write_speed,
            "interface": p.interface,
            "stock": p.stock,
        })
    return m2s
def get_products_by_cases():
    items = CaseItem.query.all()
    cases_list = []
    for idx, p in enumerate(items):
        cases_list.append({
            "number": idx,
            "name": p.name,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "id": p.id,
            "stock": p.stock,
        })
    return cases_list
def get_products_by_casefan():
    items = Cooler.query.all()
    casefans = []
    for idx, p in enumerate(items):
        casefans.append({
            "number": idx,
            "name": p.name,
            "price": f"${p.price:.2f}",
            "image": p.img,
            "id": p.id,
            "stock": p.stock,
        })
    return casefans
@app.route("/createproduct", methods=["GET", "POST"])
def create_product():

    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    elif current_user.role != "Admin":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("home"))

    return render_template("createproduct.html")

@app.route("/motherboards/create", methods=["POST"])
def create_motherboard_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["MOBO_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["MOBO_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["MOBO_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["MOBO_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    motherboard = Motherboard(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        socket=request.form.get("socket"),
        chipset=request.form.get("chipset"),
        ram_type=request.form.get("ram_type"),
        ram_slots=request.form.get("ram_slots"),
        wifi=request.form.get("wifi"),
        motherboard_size=request.form.get("motherboard_size"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(motherboard)
    db.session.commit()

    return redirect("/motherboard")


@app.route("/cpus/create", methods=["POST"])
def create_cpu_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["CPU_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["CPU_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["CPU_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["CPU_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    cpu = CPU(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        cpu_type=request.form.get("cpu_type"),
        cpu_model=request.form.get("cpu_model"),
        socket=request.form.get("socket"),
        cores_threads=request.form.get("cores_threads"),
        integrated_graphics=request.form.get("integrated_graphics"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(cpu)
    db.session.commit()

    return redirect("/cpu")


@app.route("/cpucoolers/create", methods=["POST"])
def create_cpucooler_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    cooler = CpuCooler(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        cooler_type=request.form.get("cooler_type"),
        radiator_size=request.form.get("radiator_size"),
        fan_size=request.form.get("fan_size"),
        noise_level=request.form.get("noise_level"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(cooler)
    db.session.commit()

    return redirect("/cpucooler")


@app.route("/rams/create", methods=["POST"])
def create_ram_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["RAM_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["RAM_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["RAM_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["RAM_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    ram = RAM(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        ram_type=request.form.get("ram_type"),
        capacity=request.form.get("capacity"),
        speed=request.form.get("speed"),
        lighting=request.form.get("lighting"),
        Color=request.form.get("Color"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(ram)
    db.session.commit()

    return redirect("/ram")


@app.route("/gpus/create", methods=["POST"])
def create_gpu_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["GPU_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["GPU_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["GPU_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["GPU_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    gpu = GPU(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        gpu=request.form.get("gpu"),
        memory=request.form.get("memory"),
        numcoolers=request.form.get("numcoolers"),
        Ports=request.form.get("Ports"),
        lighting=request.form.get("lighting"),
        color=request.form.get("color"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(gpu)
    db.session.commit()

    return redirect("/gpu")


@app.route("/psus/create", methods=["POST"])
def create_psu_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["PSU_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["PSU_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["PSU_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["PSU_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    psu = PSU(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        wattage=request.form.get("wattage"),
        efficiency=request.form.get("efficiency"),
        modular=request.form.get("modular"),
        lighting=request.form.get("lighting"),
        color=request.form.get("color"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(psu)
    db.session.commit()

    return redirect("/psu")


@app.route("/hdds/create", methods=["POST"])
def create_hdd_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["HDD_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["HDD_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["HDD_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["HDD_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    hdd = HDD(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        capacity=request.form.get("capacity"),
        rpm=request.form.get("rpm"),
        cache=request.form.get("cache"),
        interface=request.form.get("interface"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(hdd)
    db.session.commit()

    return redirect("/hdd")


@app.route("/ssds/create", methods=["POST"])
def create_ssd_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["SSD_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["SSD_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["SSD_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["SSD_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    ssd = SSD(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        capacity=request.form.get("capacity"),
        read_speed=request.form.get("read_speed"),
        write_speed=request.form.get("write_speed"),
        interface=request.form.get("interface"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(ssd)
    db.session.commit()

    return redirect("/ssd")


@app.route("/m2s/create", methods=["POST"])
def create_m2_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["M2_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["M2_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["M2_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["M2_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    m2 = M2(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        capacity=request.form.get("capacity"),
        read_speed=request.form.get("read_speed"),
        write_speed=request.form.get("write_speed"),
        interface=request.form.get("interface"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(m2)
    db.session.commit()

    return redirect("/m2")


@app.route("/cases/create", methods=["POST"])
def create_case_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["CASE_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["CASE_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["CASE_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["CASE_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    case_item = CaseItem(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        compatability=request.form.get("compatability"),
        casetype=request.form.get("casetype"),
        color=request.form.get("color"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(case_item)
    db.session.commit()

    return redirect("/cases")


@app.route("/coolers/create", methods=["POST"])
def create_cooler_popup():
    os.makedirs(app.config["PARTS_FOLDER"], exist_ok=True)

    img_file = request.files.get("img")
    img1_file = request.files.get("img1")
    img2_file = request.files.get("img2")
    img3_file = request.files.get("img3")
    img4_file = request.files.get("img4")
    brand_img_file = request.files.get("brandimg")

    if img_file and img_file.filename:
        img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
        img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
    else:
        img_name = "default_img.webp"

    if img1_file and img1_file.filename:
        img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
        img1_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img1_name))
    else:
        img1_name = "default_img.webp"

    if img2_file and img2_file.filename:
        img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
        img2_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img2_name))
    else:
        img2_name = "default_img.webp"
    
    if img3_file and img3_file.filename:
        img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
        img3_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img3_name))
    else:
        img3_name = "default_img.webp"
    
    if img4_file and img4_file.filename:
        img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
        img4_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img4_name))
    else:
        img4_name = "default_img.webp"

    if brand_img_file and brand_img_file.filename:
        brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
        brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
    else:
        brand_img_name = "default_img.webp"

    cooler = Cooler(
        name=request.form["name"],
        description=request.form.get("description"),
        price=float(request.form["price"]),
        img=img_name,
        img1=img1_name,
        img2=img2_name,
        img3=img3_name,
        img4=img4_name,
        brand=request.form.get("brand"),
        brandimg=brand_img_name,
        numoffans=request.form.get("numoffans"),
        size=request.form.get("size"),
        lighting=request.form.get("lighting"),
        color=request.form.get("color"),
        condition=request.form.get("condition"),
        stock=request.form.get("stock")
    )

    db.session.add(cooler)
    db.session.commit()

    return redirect("/cooler")


@app.route("/edit_motherboard/<int:product_id>", methods=["GET", "POST"])
def edit_motherboard(product_id):
    mobo = Motherboard.query.get_or_404(product_id)

    if request.method == "POST":

        mobo.name = request.form.get("name")
        mobo.price = float(request.form.get("price"))
        mobo.description = request.form.get("description")
        mobo.brand = request.form.get("brand")
        mobo.socket = request.form.get("socket")
        mobo.chipset = request.form.get("chipset")
        mobo.ram_type = request.form.get("ram_type")
        mobo.ram_slots = request.form.get("ram_slots")
        mobo.wifi = request.form.get("wifi")
        mobo.motherboard_size = request.form.get("motherboard_size")
        mobo.condition = request.form.get("condition")

        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            mobo.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["MOBO_FOLDER"], img1_name))
            mobo.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["MOBO_FOLDER"], img2_name))
            mobo.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["MOBO_FOLDER"], img3_name))
            mobo.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["MOBO_FOLDER"], img4_name))
            mobo.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            mobo.brandimg = brand_img_name

        db.session.commit()
        flash("Motherboard updated successfully", "success")
        return redirect(url_for("motherboard"))  

    return render_template("/edit/edit_motherboard.html", mobo=mobo)


@app.route("/edit_cpu/<int:product_id>", methods=["GET", "POST"])
def edit_cpu(product_id):
    cpu = CPU.query.get_or_404(product_id)

    if request.method == "POST":

        cpu.name = request.form.get("name")
        cpu.description = request.form.get("description")
        cpu.price = float(request.form.get("price"))
        cpu.brand = request.form.get("brand")
        cpu.cpu_type = request.form.get("cpu_type")
        cpu.cpu_model = request.form.get("cpu_model")
        cpu.socket = request.form.get("socket")
        cpu.cores_threads = request.form.get("cores_threads")
        cpu.integrated_graphics = request.form.get("integrated_graphics")
        cpu.condition = request.form.get("condition")

        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            cpu.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["CPU_FOLDER"], img1_name))
            cpu.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["CPU_FOLDER"], img2_name))
            cpu.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["CPU_FOLDER"], img3_name))
            cpu.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["CPU_FOLDER"], img4_name))
            cpu.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            cpu.brandimg = brand_img_name

        db.session.commit()
        flash("CPU updated successfully", "success")
        return redirect(url_for("cpu"))

    return render_template("/edit/edit_cpu.html", cpu=cpu)


@app.route("/edit_cpucooler/<int:product_id>", methods=["GET", "POST"])
def edit_cpucooler(product_id):
    cooler = CpuCooler.query.get_or_404(product_id)
    
    if request.method == "POST":
        cooler.name = request.form.get("name")
        cooler.description = request.form.get("description")
        cooler.price = float(request.form.get("price"))
        cooler.brand = request.form.get("brand")
        cooler.cooler_type = request.form.get("cooler_type")
        cooler.radiator_size = request.form.get("radiator_size")
        cooler.fan_size = request.form.get("fan_size")
        cooler.noise_level = request.form.get("noise_level")
        cooler.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            cooler.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img1_name))
            cooler.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img2_name))
            cooler.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img3_name))
            cooler.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["CPUCOOLER_FOLDER"], img4_name))
            cooler.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            cooler.brandimg = brand_img_name
       
        
        db.session.commit()
        flash("CpuCooler updated successfully", "success")
        return redirect(url_for("cpucooler"))  
    
    return render_template("edit/edit_cpucooler.html", cooler=cooler)


@app.route("/edit_ram/<int:product_id>", methods=["GET", "POST"])
def edit_ram(product_id):
    ram = RAM.query.get_or_404(product_id)
    
    if request.method == "POST":
        ram.name = request.form.get("name")
        ram.description = request.form.get("description")
        ram.price = float(request.form.get("price"))
        ram.brand = request.form.get("brand")
        ram.ram_type = request.form.get("ram_type")
        ram.capacity = request.form.get("capacity")
        ram.speed = request.form.get("speed")
        ram.lighting = request.form.get("lighting")
        ram.Color = request.form.get("Color")
        ram.condition = request.form.get("condition")
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            ram.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["RAM_FOLDER"], img1_name))
            ram.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["RAM_FOLDER"], img2_name))
            ram.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["RAM_FOLDER"], img3_name))
            ram.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["RAM_FOLDER"], img4_name))
            ram.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            ram.brandimg = brand_img_name
        
        db.session.commit()
        flash("RAM updated successfully", "success")
        return redirect(url_for("ram"))
    
    return render_template("edit/edit_ram.html", ram=ram)


@app.route("/edit_gpu/<int:product_id>", methods=["GET", "POST"])
def edit_gpu(product_id):
    gpu = GPU.query.get_or_404(product_id)
    
    if request.method == "POST":
        gpu.name = request.form.get("name")
        gpu.description = request.form.get("description")
        gpu.price = float(request.form.get("price"))
        gpu.brand = request.form.get("brand")
        gpu.gpu = request.form.get("gpu")  
        gpu.memory = request.form.get("memory")
        gpu.numcoolers = request.form.get("numcoolers")
        gpu.Ports = request.form.get("Ports")
        gpu.lighting = request.form.get("lighting")
        gpu.color = request.form.get("color")
        gpu.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            gpu.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["GPU_FOLDER"], img1_name))
            gpu.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["GPU_FOLDER"], img2_name))
            gpu.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["GPU_FOLDER"], img3_name))
            gpu.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["GPU_FOLDER"], img4_name))
            gpu.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            gpu.brandimg = brand_img_name
        
        db.session.commit()
        flash("GPU updated successfully", "success")
        return redirect(url_for("gpu"))  
    
    return render_template("edit/edit_gpu.html", gpu=gpu)


@app.route("/edit_psu/<int:product_id>", methods=["GET", "POST"])
def edit_psu(product_id):
    psu = PSU.query.get_or_404(product_id)
    
    if request.method == "POST":
        psu.name = request.form.get("name")
        psu.description = request.form.get("description")
        psu.price = float(request.form.get("price"))
        psu.brand = request.form.get("brand")
        psu.wattage = request.form.get("wattage")
        psu.efficiency = request.form.get("efficiency")
        psu.modular = request.form.get("modular")
        psu.lighting = request.form.get("lighting")
        psu.color = request.form.get("color")
        psu.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            psu.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["PSU_FOLDER"], img1_name))
            psu.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["PSU_FOLDER"], img2_name))
            psu.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["PSU_FOLDER"], img3_name))
            psu.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["PSU_FOLDER"], img4_name))
            psu.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            psu.brandimg = brand_img_name
        
        db.session.commit()
        flash("PSU updated successfully", "success")
        return redirect(url_for("psu"))  
    
    return render_template("edit/edit_psu.html", psu=psu)


@app.route("/edit_hdd/<int:product_id>", methods=["GET", "POST"])
def edit_hdd(product_id):
    hdd = HDD.query.get_or_404(product_id)
    
    if request.method == "POST":
        hdd.name = request.form.get("name")
        hdd.description = request.form.get("description")
        hdd.price = float(request.form.get("price"))
        hdd.brand = request.form.get("brand")
        hdd.capacity = request.form.get("capacity")
        hdd.rpm = request.form.get("rpm")
        hdd.cache = request.form.get("cache")
        hdd.interface = request.form.get("interface")
        hdd.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            hdd.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["HDD_FOLDER"], img1_name))
            hdd.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["HDD_FOLDER"], img2_name))
            hdd.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["HDD_FOLDER"], img3_name))
            hdd.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["HDD_FOLDER"], img4_name))
            hdd.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            hdd.brandimg = brand_img_name
        
        db.session.commit()
        flash("HDD updated successfully", "success")
        return redirect(url_for("hdd"))  
    
    return render_template("edit/edit_hdd.html", hdd=hdd)


@app.route("/edit_ssd/<int:product_id>", methods=["GET", "POST"])
def edit_ssd(product_id):
    ssd = SSD.query.get_or_404(product_id)
    
    if request.method == "POST":
        ssd.name = request.form.get("name")
        ssd.description = request.form.get("description")
        ssd.price = float(request.form.get("price"))
        ssd.brand = request.form.get("brand")
        ssd.capacity = request.form.get("capacity")
        ssd.read_speed = request.form.get("read_speed")
        ssd.write_speed = request.form.get("write_speed")
        ssd.interface = request.form.get("interface")
        ssd.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            ssd.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["SSD_FOLDER"], img1_name))
            ssd.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["SSD_FOLDER"], img2_name))
            ssd.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["SSD_FOLDER"], img3_name))
            ssd.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["SSD_FOLDER"], img4_name))
            ssd.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            ssd.brandimg = brand_img_name
        
        db.session.commit()
        flash("SSD updated successfully", "success")
        return redirect(url_for("ssd"))  
    
    return render_template("edit/edit_ssd.html", ssd=ssd)


@app.route("/edit_m2/<int:product_id>", methods=["GET", "POST"])
def edit_m2(product_id):
    m2 = M2.query.get_or_404(product_id)
    
    if request.method == "POST":
        m2.name = request.form.get("name")
        m2.description = request.form.get("description")
        m2.price = float(request.form.get("price"))
        m2.brand = request.form.get("brand")
        m2.capacity = request.form.get("capacity")
        m2.read_speed = request.form.get("read_speed")
        m2.write_speed = request.form.get("write_speed")
        m2.interface = request.form.get("interface")
        m2.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            m2.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["M2_FOLDER"], img1_name))
            m2.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["M2_FOLDER"], img2_name))
            m2.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["M2_FOLDER"], img3_name))
            m2.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["M2_FOLDER"], img4_name))
            m2.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            m2.brandimg = brand_img_name
        
        db.session.commit()
        flash("M.2 drive updated successfully", "success")
        return redirect(url_for("m2"))  
    
    return render_template("edit/edit_m2.html", m2=m2)


@app.route("/edit_cases/<int:product_id>", methods=["GET", "POST"])
def edit_cases(product_id):
    case_item = CaseItem.query.get_or_404(product_id)
    
    if request.method == "POST":
        case_item.name = request.form.get("name")
        case_item.description = request.form.get("description")
        case_item.price = float(request.form.get("price"))
        case_item.brand = request.form.get("brand")
        case_item.compatability = request.form.get("compatability")
        case_item.casetype = request.form.get("casetype")
        case_item.color = request.form.get("color")
        case_item.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            case_item.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["CASE_FOLDER"], img1_name))
            case_item.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["CASE_FOLDER"], img2_name))
            case_item.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["CASE_FOLDER"], img3_name))
            case_item.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["CASE_FOLDER"], img4_name))
            case_item.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            case_item.brandimg = brand_img_name
        
        db.session.commit()
        flash("Case updated successfully", "success")
        return redirect(url_for("cases"))  
    
    return render_template("edit/edit_case.html", case_item=case_item)


@app.route("/edit_casefan/<int:product_id>", methods=["GET", "POST"])
def edit_casefan(product_id):
    cooler = Cooler.query.get_or_404(product_id)
    
    if request.method == "POST":
        cooler.name = request.form.get("name")
        cooler.description = request.form.get("description")
        cooler.price = float(request.form.get("price"))
        cooler.brand = request.form.get("brand")
        cooler.numoffans = request.form.get("numoffans")
        cooler.size = request.form.get("size")
        cooler.lighting = request.form.get("lighting")
        cooler.color = request.form.get("color")
        cooler.condition = request.form.get("condition")
        
        
        img_file = request.files.get("img")
        if img_file and img_file.filename:
            img_name = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
            img_file.save(os.path.join(app.config["PARTS_FOLDER"], img_name))
            cooler.img = img_name

        img1_file = request.files.get("img1")
        if img1_file and img1_file.filename:
            img1_name = f"{uuid.uuid4().hex}_{secure_filename(img1_file.filename)}"
            img1_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img1_name))
            cooler.img1 = img1_name

        img2_file = request.files.get("img2")
        if img2_file and img2_file.filename:
            img2_name = f"{uuid.uuid4().hex}_{secure_filename(img2_file.filename)}"
            img2_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img2_name))
            cooler.img2 = img2_name

        img3_file = request.files.get("img3")
        if img3_file and img3_file.filename:
            img3_name = f"{uuid.uuid4().hex}_{secure_filename(img3_file.filename)}"
            img3_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img3_name))
            cooler.img3 = img3_name

        img4_file = request.files.get("img4")
        if img4_file and img4_file.filename:
            img4_name = f"{uuid.uuid4().hex}_{secure_filename(img4_file.filename)}"
            img4_file.save(os.path.join(app.config["CASEFAN_FOLDER"], img4_name))
            cooler.img4 = img4_name

        brand_img_file = request.files.get("brandimg")
        if brand_img_file and brand_img_file.filename:
            brand_img_name = f"{uuid.uuid4().hex}_{secure_filename(brand_img_file.filename)}"
            brand_img_file.save(os.path.join(app.config["BRANDS_FOLDER"], brand_img_name))
            cooler.brandimg = brand_img_name
        
        db.session.commit()
        flash("Cooler updated successfully", "success")
        return redirect(url_for("casefan"))  
    
    return render_template("edit/edit_cooler.html", cooler=cooler)


@app.route("/delete_motherboard/<int:product_id>")
def delete_motherboard(product_id):
    product = Motherboard.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("Motherboard deleted", "danger")
    return redirect(url_for("motherboard"))

@app.route("/delete_cpu/<int:product_id>")
def delete_cpu(product_id):
    product = CPU.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("CPU deleted", "danger")
    return redirect(url_for("cpu"))

@app.route("/delete_cpucooler/<int:product_id>")
def delete_cpucooler(product_id):
    product = CpuCooler.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("CPU Cooler deleted", "danger")
    return redirect(url_for("cpucooler"))

@app.route("/delete_ram/<int:product_id>")
def delete_ram(product_id):
    product = RAM.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("RAM deleted", "danger")
    return redirect(url_for("ram"))

@app.route("/delete_gpu/<int:product_id>")
def delete_gpu(product_id):
    product = GPU.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("GPU deleted", "danger")
    return redirect(url_for("gpu"))

@app.route("/delete_psu/<int:product_id>")
def delete_psu(product_id):
    product = PSU.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("PSU deleted", "danger")
    return redirect(url_for("psu"))

@app.route("/delete_hdd/<int:product_id>")
def delete_hdd(product_id):
    product = HDD.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("PSU deleted", "danger")
    return redirect(url_for("hdd"))

@app.route("/delete_ssd/<int:product_id>")
def delete_ssd(product_id):
    product = SSD.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("SSD deleted", "danger")
    return redirect(url_for("ssd"))

@app.route("/delete_m2/<int:product_id>")
def delete_m2(product_id):
    product = M2.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("M2 deleted", "danger")
    return redirect(url_for("m2"))

@app.route("/delete_cases/<int:product_id>")
def delete_cases(product_id):
    product = CaseItem.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("Case deleted", "danger")
    return redirect(url_for("cases"))

@app.route("/delete_casefan/<int:product_id>")
def delete_casefan(product_id):

    product = Cooler.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("Case Fan deleted", "danger")
    return redirect(url_for("casefan"))

@app.route("/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    db.session.delete(comment)
    db.session.commit()

    flash("Comment Deleted", "danger")

    return redirect(request.referrer or url_for("home"))

@app.route("/motherboard/<int:product_id>", methods=["GET", "POST"])
def motherboard_detailed(product_id):
    motherboard = Motherboard.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="motherboard",
                product_id=motherboard.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("motherboard_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="motherboard",
        product_id=motherboard.id
    ).all()

    return render_template(
        "products/motherboard.html",
        motherboard=motherboard,
        comments=comments
    )


@app.route("/cpu/<int:product_id>", methods=["GET", "POST"])
def cpu_detailed(product_id):
    Cpus = CPU.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="cpu",
                product_id=Cpus.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("cpu_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="cpu",
        product_id=Cpus.id
    ).all()
    
    return render_template("/products/processor.html",cpus=Cpus,comments=comments)

@app.route("/cpucooler/<int:product_id>", methods=["GET", "POST"])
def cpucooler_detailed(product_id):
    Cpucooler = CpuCooler.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="cpucooler",
                product_id=Cpucooler.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("cpucooler_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="cpucooler",
        product_id=Cpucooler.id
    ).all()

    return render_template("/products/processorcooler.html",cpucool=Cpucooler,comments=comments)

@app.route("/ram/<int:product_id>", methods=["GET", "POST"])
def ram_detailed(product_id):
    Ram = RAM.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="ram",
                product_id=Ram.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("ram_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="ram",
        product_id=Ram.id
    ).all()

    return render_template("/products/rams.html",ram=Ram,comments=comments)

@app.route("/gpu/<int:product_id>", methods=["GET", "POST"])
def gpu_detailed(product_id):
    Gpus = GPU.query.get(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="gpu",
                product_id=Gpus.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("gpu_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="gpu",
        product_id=Gpus.id
    ).all()

    return render_template("/products/gpus.html",gpus=Gpus,comments=comments)

@app.route("/psu/<int:product_id>", methods=["GET", "POST"])
def psu_detailed(product_id):
    Psus = PSU.query.get(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="psu",
                product_id=Psus.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("psu_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="psu",
        product_id=Psus.id
    ).all()
    
    return render_template("/products/psus.html", psus=Psus, comments=comments)

@app.route("/hdd/<int:product_id>", methods=["GET", "POST"])
def hdd_detailed(product_id):
    Hdds = HDD.query.get(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="hdd",
                product_id=Hdds.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("hdd_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="hdd",
        product_id=Hdds.id
    ).all()

    return render_template("/products/hdds.html", hdd=Hdds,comments=comments)

@app.route("/ssd/<int:product_id>", methods=["GET", "POST"])
def ssd_detailed(product_id):
    Ssds = SSD.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="ssd",
                product_id=Ssds.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("ssd_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="ssd",
        product_id=Ssds.id
    ).all()

    return render_template("/products/ssds.html", ssd=Ssds,comments=comments)

@app.route("/m2/<int:product_id>", methods=["GET", "POST"])
def m2_detailed(product_id):
    m2 = M2.query.get_or_404(product_id)
    
    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="m2",
                product_id=m2.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("m2_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="m2",
        product_id=m2.id
    ).all()

    return render_template("/products/m2.html", m2=m2, comments=comments)

@app.route("/cases/<int:product_id>", methods=["GET", "POST"])
def case_detailed(product_id):
    Case = CaseItem.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="case",
                product_id=Case.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("case_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="case",
        product_id=Case.id
    ).all()

    return render_template("/products/case.html", case=Case, comments=comments)

@app.route("/casefan/<int:product_id>", methods=["GET", "POST"])
def casefan_detailed(product_id):
    Casefan = Cooler.query.get_or_404(product_id)

    if request.method == "POST":
        text = request.form.get("text")
        rating = request.form.get("rating")

        if text and rating:
            comment = Comment(
                text=text,
                rating=int(rating),
                product_type="casefan",
                product_id=Casefan.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()

        return redirect(url_for("casefan_detailed", product_id=product_id))

    comments = Comment.query.filter_by(
        product_type="casefan",
        product_id=Casefan.id
    ).all()
    
    return render_template("/products/casefan.html", casefan=Casefan, comments=comments)

@app.route("/motherboard")
def motherboard():

    raw_mobos = get_products_by_mobo()


    mobo_list = []
    for idx, m in enumerate(raw_mobos):
        mobo_list.append({
            "number": idx,
            "id": m.get("id"),
            "name": m.get("name"),
            "price": float(str(m.get("price", "0")).replace("$", "")),
            "price_num": float(str(m.get("price", "0")).replace("$", "")),
            "image": m.get("image"),
            "brand": m.get("brand") or "Unknown",
            "condition": m.get("condition") or "Unknown",
            "socket": m.get("socket") or "Unknown",
            "ram": m.get("ram") or "Unknown",
            "size": m.get("size") or "Unknown",
            "stock": m.get("stock"),
        })



    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_sockets = [s.upper() for s in request.args.getlist("socket")]
    selected_rams = [r.upper() for r in request.args.getlist("ram")]
    selected_size = [s.upper() for s in request.args.getlist("size")]
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        mobo_list = [m for m in mobo_list if m["brand"].upper() in selected_brands]
    if selected_conditions:
        mobo_list = [m for m in mobo_list if m["condition"].lower() in selected_conditions]
    if selected_sockets:
        mobo_list = [m for m in mobo_list if m["socket"].upper() in selected_sockets]
    if selected_rams:
        mobo_list = [m for m in mobo_list if m["ram"].upper() in selected_rams]
    if selected_size:
        mobo_list = [m for m in mobo_list if m["size"].upper() in selected_size]
    if selected_min_price is not None:
        mobo_list = [m for m in mobo_list if m["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        mobo_list = [m for m in mobo_list if m["price_num"] <= selected_max_price]


    if selected_sort == "low":
        mobo_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        mobo_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        mobo_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        mobo_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({m["brand"] for m in mobo_list})
    unique_conditions = sorted({m["condition"] for m in mobo_list})
    unique_sockets = sorted({m["socket"] for m in mobo_list})
    unique_ram_types = sorted({m["ram"] for m in mobo_list})
    unique_motherboard_size = sorted({m["size"] for m in mobo_list})


    return render_template(
        "mobo.html",
        motherboards=mobo_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_sockets=unique_sockets,
        unique_ram_types=unique_ram_types,
        unique_motherboard_size=unique_motherboard_size,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_sockets=selected_sockets,
        selected_rams=selected_rams,
        selected_size=selected_size,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )


@app.route("/cpu")
def cpu():
    raw_cpus = get_products_by_cpu()  

    cpu_list = []
    for c in raw_cpus:
        raw_price = c.get("price", 0)
        try:
            price = float(str(raw_price).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            price = 0.0

        cpu_list.append({
            "id": c.get("id"),
            "name": c.get("name", "Unknown CPU"),
            "description": c.get("description", ""),
            "price": price,
            "price_num": price,
            "image": c.get("image", "placeholder.png"),
            "brand": c.get("brand", "Unknown"),
            "condition": c.get("condition", "Unknown"),
            "socket": c.get("socket", "Unknown"),
            "stock": c.get("stock"),
        })


    all_cpus = cpu_list.copy()


    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_sockets = [s.upper() for s in request.args.getlist("socket")]
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        cpu_list = [c for c in cpu_list if c["brand"].upper() in selected_brands]
    if selected_conditions:
        cpu_list = [c for c in cpu_list if c["condition"].lower() in selected_conditions]
    if selected_sockets:
        cpu_list = [c for c in cpu_list if c["socket"].upper() in selected_sockets]
    if selected_min_price is not None:
        cpu_list = [c for c in cpu_list if c["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        cpu_list = [c for c in cpu_list if c["price_num"] <= selected_max_price]


    if selected_sort == "low":
        cpu_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        cpu_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        cpu_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        cpu_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({c["brand"] for c in all_cpus})
    unique_conditions = sorted({c["condition"] for c in all_cpus})
    unique_sockets = sorted({c["socket"] for c in all_cpus})

    return render_template(
        "cpu.html",
        cpus=cpu_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_sockets=unique_sockets,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_sockets=selected_sockets,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )




@app.route("/cpucooler")
def cpucooler():
    raw_coolers = get_products_by_cpucooler()

    cooler_list = []
    for c in raw_coolers:
        price = float(str(c.get("price", 0)).replace("$", ""))
        cooler_list.append({
            "id": c.get("id"),
            "name": c.get("name"),
            "price": price,
            "price_num": price,
            "image": c.get("image"),
            "brand": c.get("brand") or "Unknown",
            "condition": c.get("condition") or "Unknown",
            "cooler_type": c.get("cooler_type") or "Unknown",
            "radiator_size": str(c.get("radiator_size")) if c.get("radiator_size") else "Unknown",
            "stock": c.get("stock"),
        })


    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_cooler_types = [t.lower() for t in request.args.getlist("cooler_type")]
    selected_radiator_sizes = request.args.getlist("radiator_size")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")

    if selected_brands:
        cooler_list = [c for c in cooler_list if c["brand"].upper() in selected_brands]
    if selected_conditions:
        cooler_list = [c for c in cooler_list if c["condition"].lower() in selected_conditions]
    if selected_cooler_types:
        cooler_list = [c for c in cooler_list if c["cooler_type"].lower() in selected_cooler_types]
    if selected_radiator_sizes:
        cooler_list = [c for c in cooler_list if c["radiator_size"] in selected_radiator_sizes]
    if selected_min_price is not None:
        cooler_list = [c for c in cooler_list if c["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        cooler_list = [c for c in cooler_list if c["price_num"] <= selected_max_price]

    if selected_sort == "low":
        cooler_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        cooler_list.sort(key=lambda x: x["price_num"], reverse=True)

    unique_brands = sorted({c["brand"] for c in cooler_list})
    unique_conditions = sorted({c["condition"] for c in cooler_list})
    unique_cooler_types = sorted({c["cooler_type"] for c in cooler_list})
    unique_radiator_sizes = sorted({c["radiator_size"] for c in cooler_list})

    return render_template(
        "cpucooler.html",
        cpucool=cooler_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_cooler_types=unique_cooler_types,
        unique_radiator_sizes=unique_radiator_sizes,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_cooler_types=selected_cooler_types,
        selected_radiator_sizes=selected_radiator_sizes,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )



@app.route("/ram")
def ram():
    raw_rams = get_products_by_ram()

    ram_list = []
    for r in raw_rams:
        try:
            price = float(str(r.get("price", 0)).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            price = 0.0

        ram_list.append({
            "id": r.get("id"),
            "name": r.get("name", "Unknown RAM"),
            "price": price,
            "price_num": price,
            "image": r.get("image", "placeholder.png"),
            "brand": (r.get("brand") or "Unknown").upper(),
            "condition": (r.get("condition") or "Unknown").lower(),
            "type": (r.get("type") or "Unknown").upper(),
            "color": (r.get("color") or "Unknown").upper(),
            "capacity": str(r.get("capacity")) if r.get("capacity") else "Unknown",
            "speed": str(r.get("speed")) if r.get("speed") else "Unknown",
            "rgb": str(r.get("rgb")) if r.get("rgb") is not None else "Unknown",
            "stock": r.get("stock"),
        })


    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_types = [t.upper() for t in request.args.getlist("type")]
    selected_colors = [c.upper() for c in request.args.getlist("color")]
    selected_capacity = request.args.getlist("capacity")
    selected_speed = request.args.getlist("speed")
    selected_rgb = request.args.getlist("rgb")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")

    if selected_brands:
        ram_list = [r for r in ram_list if r["brand"] in selected_brands]
    if selected_conditions:
        ram_list = [r for r in ram_list if r["condition"] in selected_conditions]
    if selected_types:
        ram_list = [r for r in ram_list if r["type"] in selected_types]
    if selected_colors:
        ram_list = [r for r in ram_list if r["color"] in selected_colors]
    if selected_capacity:
        ram_list = [r for r in ram_list if r["capacity"] in selected_capacity]
    if selected_speed:
        ram_list = [r for r in ram_list if r["speed"] in selected_speed]
    if selected_rgb:
        ram_list = [r for r in ram_list if r["rgb"] in selected_rgb]
    if selected_min_price is not None:
        ram_list = [r for r in ram_list if r["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        ram_list = [r for r in ram_list if r["price_num"] <= selected_max_price]


    if selected_sort == "low":
        ram_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        ram_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        ram_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        ram_list.sort(key=lambda x: x.get("id", 0), reverse=True)

    unique_brands = sorted({r["brand"] for r in ram_list})
    unique_conditions = sorted({r["condition"] for r in ram_list})
    unique_types = sorted({r["type"] for r in ram_list})
    unique_colors = sorted({r["color"] for r in ram_list})
    unique_capacity = sorted({r["capacity"] for r in ram_list})
    unique_speed = sorted({r["speed"] for r in ram_list})
    unique_rgb = sorted({r["rgb"] for r in ram_list})

    return render_template(
        "ram.html",
        ramm=ram_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_types=unique_types,
        unique_colors=unique_colors,
        unique_capacity=unique_capacity,
        unique_speed=unique_speed,
        unique_rgb=unique_rgb,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_types=selected_types,
        selected_colors=selected_colors,
        selected_capacity=selected_capacity,
        selected_speed=selected_speed,
        selected_rgb=selected_rgb,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )



@app.route("/gpu")
def gpu():
    raw_gpus = get_products_by_gpu()

    gpu_list = []
    for g in raw_gpus:
        try:
            price = float(str(g.get("price", 0)).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            price = 0.0

        gpu_list.append({
            "id": g.get("id"),
            "name": g.get("name", "Unknown GPU"),
            "price": price,
            "price_num": price,
            "image": g.get("image", "placeholder.png"),
            "brand": (g.get("brand") or "Unknown").upper(),
            "condition": (g.get("condition") or "Unknown").lower(),
            "gpu": (g.get("gpu") or "Unknown").upper(),
            "memory": str(g.get("memory")) if g.get("memory") else "Unknown",
            "numcoolers": str(g.get("numcoolers")) if g.get("numcoolers") else "Unknown",
            "ports": g.get("ports") or "Unknown",
            "lighting": g.get("lighting") or "Unknown",
            "color": g.get("color") or "Unknown",
            "stock": g.get("stock"),
        })

    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_chips = [c.upper() for c in request.args.getlist("gpu")]
    selected_memory = request.args.getlist("memory")
    selected_numcoolers = request.args.getlist("numcoolers")
    selected_ports = request.args.getlist("ports")
    selected_lighting = request.args.getlist("lighting")
    selected_colors = request.args.getlist("color")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        gpu_list = [g for g in gpu_list if g["brand"] in selected_brands]
    if selected_conditions:
        gpu_list = [g for g in gpu_list if g["condition"] in selected_conditions]
    if selected_chips:
        gpu_list = [g for g in gpu_list if g["gpu"] in selected_chips]
    if selected_memory:
        gpu_list = [g for g in gpu_list if g["memory"] in selected_memory]
    if selected_numcoolers:
        gpu_list = [g for g in gpu_list if g["numcoolers"] in selected_numcoolers]
    if selected_ports:
        gpu_list = [g for g in gpu_list if g["ports"] in selected_ports]
    if selected_lighting:
        gpu_list = [g for g in gpu_list if g["lighting"] in selected_lighting]
    if selected_colors:
        gpu_list = [g for g in gpu_list if g["color"] in selected_colors]
    if selected_min_price is not None:
        gpu_list = [g for g in gpu_list if g["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        gpu_list = [g for g in gpu_list if g["price_num"] <= selected_max_price]


    if selected_sort == "low":
        gpu_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        gpu_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        gpu_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        gpu_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({g["brand"] for g in gpu_list})
    unique_conditions = sorted({g["condition"] for g in gpu_list})
    unique_chips = sorted({g["gpu"] for g in gpu_list})
    unique_memory = sorted({g["memory"] for g in gpu_list})
    unique_numcoolers = sorted({g["numcoolers"] for g in gpu_list})
    unique_ports = sorted({g["ports"] for g in gpu_list})
    unique_lighting = sorted({g["lighting"] for g in gpu_list})
    unique_colors = sorted({g["color"] for g in gpu_list})

    return render_template(
        "gpu.html",
        gpus=gpu_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_chips=unique_chips,
        unique_memory=unique_memory,
        unique_numcoolers=unique_numcoolers,
        unique_ports=unique_ports,
        unique_lighting=unique_lighting,
        unique_colors=unique_colors,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_chips=selected_chips,
        selected_memory=selected_memory,
        selected_numcoolers=selected_numcoolers,
        selected_ports=selected_ports,
        selected_lighting=selected_lighting,
        selected_colors=selected_colors,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )



@app.route("/psu")
def psu():
    raw_psus = get_products_by_psu()

    psu_list = []
    for p in raw_psus:
        try:
            price = float(str(p.get("price", 0)).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            price = 0.0

        psu_list.append({
            "id": p.get("id"),
            "name": p.get("name", "Unknown PSU"),
            "description": p.get("description", ""),
            "price": price,
            "price_num": price,
            "image": p.get("image", "placeholder.png"),
            "brand": (p.get("brand") or "Unknown").upper(),
            "condition": (p.get("condition") or "Unknown").lower(),
            "wattage": str(p.get("wattage")) if p.get("wattage") else "Unknown",
            "efficiency": (p.get("efficiency") or "Unknown"),
            "lighting": (p.get("lighting") or "Unknown"),
            "color": (p.get("color") or "Unknown"),
            "stock": p.get("stock"),
        })


    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_wattage = request.args.getlist("wattage")
    selected_efficiency = request.args.getlist("efficiency")
    selected_lighting = request.args.getlist("lighting")
    selected_colors = request.args.getlist("color")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        psu_list = [p for p in psu_list if p["brand"] in selected_brands]
    if selected_conditions:
        psu_list = [p for p in psu_list if p["condition"] in selected_conditions]
    if selected_wattage:
        psu_list = [p for p in psu_list if p["wattage"] in selected_wattage]
    if selected_efficiency:
        psu_list = [p for p in psu_list if p["efficiency"] in selected_efficiency]
    if selected_lighting:
        psu_list = [p for p in psu_list if p["lighting"] in selected_lighting]
    if selected_colors:
        psu_list = [p for p in psu_list if p["color"] in selected_colors]
    if selected_min_price is not None:
        psu_list = [p for p in psu_list if p["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        psu_list = [p for p in psu_list if p["price_num"] <= selected_max_price]


    if selected_sort == "low":
        psu_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        psu_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        psu_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        psu_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({p["brand"] for p in psu_list})
    unique_conditions = sorted({p["condition"] for p in psu_list})
    unique_wattage = sorted({p["wattage"] for p in psu_list})
    unique_efficiency = sorted({p["efficiency"] for p in psu_list})
    unique_lighting = sorted({p["lighting"] for p in psu_list})
    unique_colors = sorted({p["color"] for p in psu_list})

    return render_template(
        "psu.html",
        psus=psu_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_wattage=unique_wattage,
        unique_efficiency=unique_efficiency,
        unique_lighting=unique_lighting,
        unique_colors=unique_colors,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_wattage=selected_wattage,
        selected_efficiency=selected_efficiency,
        selected_lighting=selected_lighting,
        selected_colors=selected_colors,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )



@app.route("/hdd")
def storage():
    raw_storages = get_products_by_hdd()

    hdd_list = []
    for s in raw_storages:
        try:
            price = float(str(s.get("price", 0)).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            price = 0.0

        hdd_list.append({
            "id": s.get("id"),
            "name": s.get("name", "Unknown HDD"),
            "description": s.get("description", ""),
            "price": price,
            "price_num": price,
            "image": s.get("image", "placeholder.png"),
            "brand": (s.get("brand") or "Unknown").upper(),
            "condition": (s.get("condition") or "Unknown").lower(),
            "capacity": str(s.get("capacity")) if s.get("capacity") else "Unknown",
            "rpm": str(s.get("rpm")) if s.get("rpm") else "Unknown",
            "cache": str(s.get("cache")) if s.get("cache") else "Unknown",
            "interface": s.get("interface") or "Unknown",
            "stock": s.get("stock"),
        })


    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_capacity = request.args.getlist("capacity")
    selected_rpm = request.args.getlist("rpm")
    selected_cache = request.args.getlist("cache")
    selected_interface = request.args.getlist("interface")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        hdd_list = [s for s in hdd_list if s["brand"] in selected_brands]
    if selected_conditions:
        hdd_list = [s for s in hdd_list if s["condition"] in selected_conditions]
    if selected_capacity:
        hdd_list = [s for s in hdd_list if s["capacity"] in selected_capacity]
    if selected_rpm:
        hdd_list = [s for s in hdd_list if s["rpm"] in selected_rpm]
    if selected_cache:
        hdd_list = [s for s in hdd_list if s["cache"] in selected_cache]
    if selected_interface:
        hdd_list = [s for s in hdd_list if s["interface"] in selected_interface]
    if selected_min_price is not None:
        hdd_list = [s for s in hdd_list if s["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        hdd_list = [s for s in hdd_list if s["price_num"] <= selected_max_price]


    if selected_sort == "low":
        hdd_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        hdd_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        hdd_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        hdd_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({s["brand"] for s in hdd_list})
    unique_conditions = sorted({s["condition"] for s in hdd_list})
    unique_capacity = sorted({s["capacity"] for s in hdd_list})
    unique_rpm = sorted({s["rpm"] for s in hdd_list})
    unique_cache = sorted({s["cache"] for s in hdd_list})
    unique_interface = sorted({s["interface"] for s in hdd_list})

    return render_template(
        "hdd.html",
        hddd=hdd_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_capacity=unique_capacity,
        unique_rpm=unique_rpm,
        unique_cache=unique_cache,
        unique_interface=unique_interface,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_capacity=selected_capacity,
        selected_rpm=selected_rpm,
        selected_cache=selected_cache,
        selected_interface=selected_interface,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )


@app.route("/ssd")
def ssd():
    raw_ssds = get_products_by_ssd()

    ssd_list = []
    for s in raw_ssds:
        try:
            price = float(str(s.get("price", 0)).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            price = 0.0

        ssd_list.append({
            "id": s.get("id"),
            "name": s.get("name", "Unknown SSD"),
            "description": s.get("description", ""),
            "price": price,
            "price_num": price,
            "image": s.get("image", "placeholder.png"),
            "brand": (s.get("brand") or "Unknown").upper(),
            "condition": (s.get("condition") or "Unknown").lower(),
            "capacity": str(s.get("capacity")) if s.get("capacity") else "Unknown",
            "read_speed": s.get("read_speed") or "Unknown",
            "write_speed": s.get("write_speed") or "Unknown",
            "interface": s.get("interface") or "Unknown",
            "stock": s.get("stock"),
        })


    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_capacity = request.args.getlist("capacity")
    selected_read_speed = request.args.getlist("read_speed")
    selected_write_speed = request.args.getlist("write_speed")
    selected_interface = request.args.getlist("interface")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        ssd_list = [s for s in ssd_list if s["brand"] in selected_brands]
    if selected_conditions:
        ssd_list = [s for s in ssd_list if s["condition"] in selected_conditions]
    if selected_capacity:
        ssd_list = [s for s in ssd_list if s["capacity"] in selected_capacity]
    if selected_read_speed:
        ssd_list = [s for s in ssd_list if s["read_speed"] in selected_read_speed]
    if selected_write_speed:
        ssd_list = [s for s in ssd_list if s["write_speed"] in selected_write_speed]
    if selected_interface:
        ssd_list = [s for s in ssd_list if s["interface"] in selected_interface]
    if selected_min_price is not None:
        ssd_list = [s for s in ssd_list if s["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        ssd_list = [s for s in ssd_list if s["price_num"] <= selected_max_price]


    if selected_sort == "low":
        ssd_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        ssd_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        ssd_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        ssd_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({s["brand"] for s in ssd_list})
    unique_conditions = sorted({s["condition"] for s in ssd_list})
    unique_capacity = sorted({s["capacity"] for s in ssd_list})
    unique_read_speed = sorted({s["read_speed"] for s in ssd_list})
    unique_write_speed = sorted({s["write_speed"] for s in ssd_list})
    unique_interface = sorted({s["interface"] for s in ssd_list})

    return render_template(
        "ssd.html",
        ssdd=ssd_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_capacity=unique_capacity,
        unique_read_speed=unique_read_speed,
        unique_write_speed=unique_write_speed,
        unique_interface=unique_interface,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_capacity=selected_capacity,
        selected_read_speed=selected_read_speed,
        selected_write_speed=selected_write_speed,
        selected_interface=selected_interface,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )


@app.route("/m2")
def m2():
    items = M2.query.all()

    m2_list = []
    for m in items:
        
        price_raw = getattr(m, "price", 0) 
        if price_raw is None:
            price_num = 0.0
        else:
            
            try:
                price_num = float(str(price_raw).replace("$", "").replace(",", "").strip())
            except ValueError:
                price_num = 0.0

        m2_list.append({
            "id": m.id,
            "name": m.name or "Unknown",
            "price": m.price,   
            "price_num": m.price,      
            "image": m.img or "placeholder.png",
            "brand": (m.brand or "Unknown").upper(),
            "condition": (m.condition or "Unknown").lower(),
            "capacity": m.capacity or "Unknown",
            "read_speed": m.read_speed or "Unknown",
            "write_speed": m.write_speed or "Unknown",
            "interface": m.interface or "Unknown",
            "stock": m.stock,
        })

    
    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_capacity = request.args.getlist("capacity")
    selected_read_speed = request.args.getlist("read_speed")
    selected_write_speed = request.args.getlist("write_speed")
    selected_interface = request.args.getlist("interface")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")

    
    if selected_brands:
        m2_list = [m for m in m2_list if m["brand"] in selected_brands]
    if selected_conditions:
        m2_list = [m for m in m2_list if m["condition"] in selected_conditions]
    if selected_capacity:
        m2_list = [m for m in m2_list if m["capacity"] in selected_capacity]
    if selected_read_speed:
        m2_list = [m for m in m2_list if m["read_speed"] in selected_read_speed]
    if selected_write_speed:
        m2_list = [m for m in m2_list if m["write_speed"] in selected_write_speed]
    if selected_interface:
        m2_list = [m for m in m2_list if m["interface"] in selected_interface]
    if selected_min_price is not None:
        m2_list = [m for m in m2_list if m["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        m2_list = [m for m in m2_list if m["price_num"] <= selected_max_price]


    if selected_sort == "low":
        m2_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        m2_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        m2_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        m2_list.sort(key=lambda x: x.get("id", 0), reverse=True)

    unique_brands = sorted({m["brand"] for m in m2_list})
    unique_conditions = sorted({m["condition"] for m in m2_list})
    unique_capacity = sorted({m["capacity"] for m in m2_list})
    unique_read_speed = sorted({m["read_speed"] for m in m2_list})
    unique_write_speed = sorted({m["write_speed"] for m in m2_list})
    unique_interface = sorted({m["interface"] for m in m2_list})

    return render_template(
        "m2.html",
        mm2=m2_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_capacity=unique_capacity,
        unique_read_speed=unique_read_speed,
        unique_write_speed=unique_write_speed,
        unique_interface=unique_interface,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_capacity=selected_capacity,
        selected_read_speed=selected_read_speed,
        selected_write_speed=selected_write_speed,
        selected_interface=selected_interface,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )



@app.route("/cases")
def cases():

    cases = CaseItem.query.all()

    case_list = []
    for idx, c in enumerate(cases):
        case_list.append({
            "number": idx,
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "price": c.price,   
            "price_num": c.price,   
            "image": c.img,
            "brand": c.brand or "Unknown",
            "condition": c.condition or "Unknown",
            "casetype": c.casetype or "Unknown",
            "color": c.color or "Unknown",
            "compatability": c.compatability or "Unknown",
            "stock": c.stock,
        })



    selected_brands = [b.strip().upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.strip().lower() for c in request.args.getlist("condition")]
    selected_casetypes = request.args.getlist("casetype")
    selected_colors = request.args.getlist("color")
    selected_compat = request.args.getlist("compatability")
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")


    if selected_brands:
        case_list = [c for c in case_list if c["brand"].upper() in selected_brands]
    if selected_conditions:
        case_list = [c for c in case_list if c["condition"].lower() in selected_conditions]
    if selected_casetypes:
        case_list = [c for c in case_list if c["casetype"] in selected_casetypes]
    if selected_colors:
        case_list = [c for c in case_list if c["color"] in selected_colors]
    if selected_compat:
        case_list = [c for c in case_list if c["compatability"] in selected_compat]
    if selected_min_price is not None:
        case_list = [c for c in case_list if c["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        case_list = [c for c in case_list if c["price_num"] <= selected_max_price]


    if selected_sort == "low":
        case_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        case_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        case_list.sort(key=lambda x: x.get("id", 0))
    elif selected_sort == "newest":
        case_list.sort(key=lambda x: x.get("id", 0), reverse=True)


    unique_brands = sorted({c["brand"] for c in case_list})
    unique_conditions = sorted({c["condition"] for c in case_list})
    unique_casetypes = sorted({c["casetype"] for c in case_list})
    unique_colors = sorted({c["color"] for c in case_list})
    unique_compat = sorted({c["compatability"] for c in case_list})

    return render_template(
        "cases.html",
        case=case_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_casetypes=unique_casetypes,
        unique_colors=unique_colors,
        unique_compat=unique_compat,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_casetypes=selected_casetypes,
        selected_colors=selected_colors,
        selected_compat=selected_compat,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )


@app.route("/casefan")
def casefan():
    raw_coolers = Cooler.query.all()

    cooler_list = []
    for idx, c in enumerate(raw_coolers):
        cooler_list.append({
            "number": idx,
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "price": float(c.price),
            "price_num": float(c.price),
            "image": c.img,
            "brand": c.brand or "Unknown",
            "numoffans": str(c.numoffans) if c.numoffans is not None else "Unknown",
            "size": c.size or "Unknown",
            "lighting": c.lighting or "Unknown",
            "color": c.color or "Unknown",
            "condition": c.condition or "Unknown",
            "stock": c.stock,
        })


   
    selected_brands = [b.upper() for b in request.args.getlist("brand")]
    selected_conditions = [c.lower() for c in request.args.getlist("condition")]
    selected_numoffans = request.args.getlist("numoffans")
    selected_sizes = [s.upper() for s in request.args.getlist("size")]
    selected_lighting = [l.upper() for l in request.args.getlist("lighting")]
    selected_colors = [c.upper() for c in request.args.getlist("color")]
    selected_min_price = request.args.get("min_price", type=float)
    selected_max_price = request.args.get("max_price", type=float)
    selected_sort = request.args.get("sort")

    
    if selected_brands:
        cooler_list = [c for c in cooler_list if c["brand"].upper() in selected_brands]
    if selected_conditions:
        cooler_list = [c for c in cooler_list if c["condition"].lower() in selected_conditions]
    if selected_numoffans:
        cooler_list = [c for c in cooler_list if c["numoffans"] in selected_numoffans]
    if selected_sizes:
        cooler_list = [c for c in cooler_list if c["size"].upper() in selected_sizes]
    if selected_lighting:
        cooler_list = [c for c in cooler_list if c["lighting"].upper() in selected_lighting]
    if selected_colors:
        cooler_list = [c for c in cooler_list if c["color"].upper() in selected_colors]
    if selected_min_price is not None:
        cooler_list = [c for c in cooler_list if c["price_num"] >= selected_min_price]
    if selected_max_price is not None:
        cooler_list = [c for c in cooler_list if c["price_num"] <= selected_max_price]

  
    if selected_sort == "low":
        cooler_list.sort(key=lambda x: x["price_num"])
    elif selected_sort == "high":
        cooler_list.sort(key=lambda x: x["price_num"], reverse=True)
    elif selected_sort == "latest":
        cooler_list.sort(key=lambda x: x["id"])
    elif selected_sort == "newest":
        cooler_list.sort(key=lambda x: x["id"], reverse=True)

  
    unique_brands = sorted({c["brand"] for c in cooler_list if c["brand"]})
    unique_conditions = sorted({c["condition"] for c in cooler_list if c["condition"]})
    unique_numoffans = sorted({c["numoffans"] for c in cooler_list if c["numoffans"]})
    unique_sizes = sorted({c["size"] for c in cooler_list if c["size"]})
    unique_lighting = sorted({c["lighting"] for c in cooler_list if c["lighting"]})
    unique_colors = sorted({c["color"] for c in cooler_list if c["color"]})

    return render_template(
        "casefan.html",
        fans=cooler_list,
        unique_brands=unique_brands,
        unique_conditions=unique_conditions,
        unique_numoffans=unique_numoffans,
        unique_sizes=unique_sizes,
        unique_lighting=unique_lighting,
        unique_colors=unique_colors,
        selected_brands=selected_brands,
        selected_conditions=selected_conditions,
        selected_numoffans=selected_numoffans,
        selected_sizes=selected_sizes,
        selected_lighting=selected_lighting,
        selected_colors=selected_colors,
        selected_min_price=selected_min_price,
        selected_max_price=selected_max_price,
        selected_sort=selected_sort
    )


@app.route("/parts")
def parts():
    return render_template("parts.html" )

@app.route("/wishlist")
def wishlist():
    if not current_user.is_authenticated:
        flash("Login required.", "danger")
        return redirect(url_for("login"))

    wishlist_items_db = WishlistItem.query.filter_by(user_id=current_user.id).all()

    product_models = {
        'motherboard': Motherboard,
        'cpu': CPU,
        'gpu': GPU,
        'ram': RAM,
        'psu': PSU,
        'cpucooler': CpuCooler,
        'casefan': Cooler,
        'hdd': HDD,
        'ssd': SSD,
        'm2': M2,
        'cases': CaseItem
    }

    wishlist_items = []
    for item in wishlist_items_db:
        model = product_models.get(item.product_type)
        product = model.query.get(item.product_id) if model else None

        wishlist_items.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_type": item.product_type,
            "stock": product.stock,
            "name": product.description if product else item.name,
            "price": product.price if product else item.price,
            "img": product.img if product else "placeholder.png"
        })

    return render_template("wishlist.html", wishlist_items=wishlist_items)


@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    if not current_user.is_authenticated:
        flash("Login required.", "danger")
        return redirect(url_for("login"))

    user_id = current_user.id
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    price = request.form.get('price')
    product_type = request.form.get('product_type')

    try:
        product_id = int(product_id)
        price = float(price)
    except (TypeError, ValueError):
        flash("Invalid product data.", "danger")
        return redirect(request.referrer)

    if not product_type:
        flash("Invalid product type.", "danger")
        return redirect(request.referrer)

 
    wishlist_item = WishlistItem.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        product_type=product_type
    ).first()

    if wishlist_item:
        flash(f"{name} is already in your wishlist 💖", "warning")
    else:
        wishlist_item = WishlistItem(
            user_id=user_id,
            product_type=product_type,
            product_id=product_id,
            name=name,
            price=price
        )
        db.session.add(wishlist_item)
        db.session.commit()
        flash(f"{name} added to wishlist 💖", "success")

    return redirect(request.referrer)

product_models = {
    'motherboard': Motherboard,
    'cpu': CPU,
    'gpu': GPU,
    'ram': RAM,
    'psu': PSU,
    'cpucooler': CpuCooler,
    'casefan': Cooler,
    'hdd': HDD,
    'ssd': SSD,
    'm2': M2,
    'cases': CaseItem
}

def get_product_by_type_and_id(product_type, product_id):
    Model = product_models.get(product_type)
    if not Model:
        return None
    return Model.query.get(product_id)


@app.route('/checkout_from_wishlist', methods=['POST'])
@login_required
def checkout_from_wishlist():
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()

    
    moved = 0
    not_in_stock = []

    for w in wishlist_items:
        product = get_product_by_type_and_id(w.product_type, w.product_id)

        if not product:
            not_in_stock.append(w.name)
            continue

        stock = getattr(product, "stock", None)

        if stock is None or int(stock) <= 0:
            not_in_stock.append(w.name)
            continue

        existing = CartItem.query.filter_by(
            user_id=current_user.id,
            product_type=w.product_type,
            product_id=w.product_id
        ).first()

        if existing:
            if hasattr(existing, "quantity"):
                existing.quantity = min((existing.quantity or 1) + 1, int(stock))
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_type=w.product_type,
                product_id=w.product_id,
                name=w.name,
                price=w.price
            )

            if hasattr(cart_item, "quantity"):
                cart_item.quantity = 1

            db.session.add(cart_item)

        db.session.delete(w)
        moved += 1

    db.session.commit()

    if moved == 1:
        flash(" item moved to cart ", "success")
    elif moved:
        flash(f"{moved} items moved to cart ", "success")

    if not_in_stock:
        flash(
            "These Items were not in stock: " + ", ".join(not_in_stock),
            "warning"
        )

    return redirect(url_for('cart'))

@app.route('/remove_from_wishlist/<int:wishlist_item_id>', methods=['POST'])
@login_required
def remove_from_wishlist(wishlist_item_id):
    item = WishlistItem.query.get_or_404(wishlist_item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item removed from wishlist", "success")
    return redirect(url_for('wishlist'))

@app.route('/cart/move_to_wishlist/<int:cart_item_id>', methods=['POST'])
@login_required
def move_to_wishlist(cart_item_id):

    cart_item = CartItem.query.get_or_404(cart_item_id)

    existing_wishlist_item = WishlistItem.query.filter_by(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        product_type=cart_item.product_type
    ).first()

    if existing_wishlist_item:
        flash(f"{cart_item.name} is already in your wishlist!", "warning")
    else:
        wishlist_item = WishlistItem(
            user_id=current_user.id,
            product_id=cart_item.product_id,
            product_type=cart_item.product_type,    
            name=cart_item.name,
            price=cart_item.price,
        )
        db.session.add(wishlist_item)
        flash(f"{cart_item.name} moved to wishlist!", "success")

    db.session.delete(cart_item)
    db.session.commit()

    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash(f"Removed {cart_item.name} from cart.", "danger")
    return redirect(url_for('cart'))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    product_models = {
        "motherboard": Motherboard,
        "cpu": CPU,
        "gpu": GPU,
        "ram": RAM,
        "psu": PSU,
        "cpucooler": CpuCooler,
        "casefan": Cooler,
        "hdd": HDD,
        "ssd": SSD,
        "m2": M2,
        "cases": CaseItem
    }

    buy_now_item = session.get("buy_now")

    if request.method == "GET":
        if buy_now_item:
            items = [buy_now_item]
            total = buy_now_item["price"] * buy_now_item["quantity"]
        else:
            items = CartItem.query.filter_by(user_id=current_user.id).all()
            if not items:
                flash("Your cart is empty.", "warning")
                return redirect(url_for("cart"))
            total = sum(item.price * item.quantity for item in items)

        return render_template("checkout.html", items=items, total=total)

    order = Order(user_id=current_user.id, status="paid")
    db.session.add(order)
    db.session.flush()

    total = 0

    if buy_now_item:
        ptype = buy_now_item.get("product_type")
        pid = buy_now_item.get("product_id")

        model = product_models.get(ptype)
        product = model.query.get(pid) if (model and pid is not None) else None

        img_val = (getattr(product, "img", None) or getattr(product, "image", None)) if product else None
        if not img_val:
            img_val = buy_now_item.get("img") or buy_now_item.get("image") or "placeholder.png"

        name_val = getattr(product, "description", None) if product else None
        if not name_val:
            name_val = buy_now_item.get("name", "Unknown item")

        oi = OrderItem(
            order_id=order.id,
            product_type=ptype,
            product_id=pid,
            name_snapshot=name_val,
            price_snapshot=float(buy_now_item["price"]),
            quantity=int(buy_now_item["quantity"]),
            image_snapshot=img_val
        )
        db.session.add(oi)

        total = float(buy_now_item["price"]) * int(buy_now_item["quantity"])
        session.pop("buy_now", None)

    else:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            flash("Your cart is empty.", "warning")
            return redirect(url_for("cart"))

        for item in items:
            model = product_models.get(item.product_type)
            product = model.query.get(item.product_id) if model else None

            img_val = (getattr(product, "img", None) or getattr(product, "image", None)) if product else None
            if not img_val:
                img_val = "placeholder.png"

            name_val = getattr(product, "description", None) if product else None
            if not name_val:
                name_val = item.name

            oi = OrderItem(
                order_id=order.id,
                product_type=item.product_type,
                product_id=item.product_id,
                name_snapshot=name_val,
                price_snapshot=float(item.price),
                quantity=int(item.quantity),
                image_snapshot=img_val
            )
            db.session.add(oi)

            total += float(item.price) * int(item.quantity)

        for item in items:
            db.session.delete(item)

    order.total_price = total
    db.session.commit()

    flash(f"Checkout complete! Total paid: ${total:.2f}", "success")
    return redirect(url_for("myprofile"))


@app.route('/buy_now', methods=['POST'])
def buy_now():
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    user_id = current_user.id

    product_id = int(request.form.get('product_id'))
    name = request.form.get('name')
    price = float(request.form.get('price'))
    product_type = request.form.get('product_type')
    quantity = int(request.form.get('quantity', 1))

    cart_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        product_type=product_type
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            product_type=product_type,
            name=name,
            price=price,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    flash("Item added. Complete your purchase below 👇", "success")
    return redirect(url_for('cart'))


@app.route('/cart')

def cart():

    if  not current_user.is_authenticated:
        flash("Login Required.", "danger")
        return redirect(url_for("login"))
    
    user_id = current_user.id
    items = CartItem.query.filter_by(user_id=user_id).all()

    cart = []
    total = 0.0

    product_models = {
        'motherboard': Motherboard,
        'cpu': CPU,
        'gpu': GPU,
        'ram': RAM,
        'psu': PSU,
        'cpucooler': CpuCooler,
        'casefan': Cooler,
        'hdd': HDD,
        'ssd': SSD,
        'm2': M2,
        'cases': CaseItem
    }

    for item in items:

        model = product_models.get(item.product_type)
        product = model.query.get(item.product_id) if model else None

        cart.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_type": item.product_type,
            "name": product.description if product else item.name,
            "stock": product.stock,
            "price": item.price,
            "quantity": item.quantity,
            "img": product.img if product else "placeholder.png"
        })
        total += item.price * item.quantity
        

    return render_template('cart.html', cart=cart, total=total)

@app.route('/cart/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_quantity(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    try:
        new_quantity = int(request.form.get('quantity', 1))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        flash("Invalid quantity.", "danger")
        return redirect(request.referrer)

    cart_item.quantity = new_quantity
    db.session.commit()
    flash(f"{cart_item.name} quantity updated!", "success")
    return redirect(url_for('cart'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    if  not current_user.is_authenticated:
        flash("Login Required.", "danger")
        return redirect(url_for("login"))
    
    user_id = current_user.id

    product_id = request.form.get('product_id')
    name = request.form.get('name')
    price = request.form.get('price')
    product_type = request.form.get('product_type')
    quantity = request.form.get('quantity', 1)

    try:
        product_id = int(product_id)
        price = float(price)
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except (TypeError, ValueError):
        flash("Invalid product data.", "danger")
        return redirect(request.referrer)

    if not product_type:
        flash("Invalid product type.", "danger")
        return redirect(request.referrer)

    cart_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        product_type=product_type
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_type=product_type,
            product_id=product_id,
            name=name,
            price=price,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()
    flash(f"{name} added to cart 🛒", "success")
    return redirect(request.referrer)

@app.route("/myprofile", methods=["GET", "POST"])
def myprofile():

    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()

    if request.method == "POST":
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")

        new_password = request.form.get("password")
        if new_password:
            current_user.password = generate_password_hash(new_password)

        img = request.files.get("image")
        if img and img.filename:
            filename = f"{uuid.uuid4().hex}_{secure_filename(img.filename)}"
            path = os.path.join(app.static_folder, "images", filename)
            img.save(path)
            current_user.image = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("myprofile"))

    return render_template("myprofile.html", profile=current_user, orders=orders)


@app.route("/profiles")
def profiles():
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    elif current_user.role != "Admin":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("home"))
    
    return render_template("profiles.html", profiles=User.query.all() )

@app.route("/delete_profile/<int:profile_id>")
def delete_profile(profile_id):
    profile = User.query.get(profile_id)

    db.session.delete(profile)
    db.session.commit()

    flash("Profile Deleted", "danger")
    return redirect("/")

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()

    results = {
        "motherboard": [],
        "cpu": [],
        "cpucooler": [],
        "ram": [],
        "gpu": [],
        "psu": [],
        "hdd": [],
        "m2": [],
        "ssd": [],
        "cases": [],
        "casefan": [],
    }

    if q:
        results["motherboard"] = Motherboard.query.filter(
            Motherboard.name.ilike(f"%{q}%")
        ).all()
        results["cpu"] = CPU.query.filter(CPU.name.ilike(f"%{q}%")).all()
        results["cpucooler"] = CpuCooler.query.filter(CpuCooler.name.ilike(f"%{q}%")).all()
        results["ram"] = RAM.query.filter(RAM.name.ilike(f"%{q}%")).all()
        results["gpu"] = GPU.query.filter(GPU.name.ilike(f"%{q}%")).all()
        results["psu"] = PSU.query.filter(PSU.name.ilike(f"%{q}%")).all()
        results["hdd"] = HDD.query.filter(HDD.name.ilike(f"%{q}%")).all()
        results["m2"] = M2.query.filter(M2.name.ilike(f"%{q}%")).all()
        results["ssd"] = SSD.query.filter(SSD.name.ilike(f"%{q}%")).all()
        results["cases"] = CaseItem.query.filter(CaseItem.name.ilike(f"%{q}%")).all()
        results["casefan"] = Cooler.query.filter(Cooler.name.ilike(f"%{q}%")).all()

    return render_template("search.html", q=q, results=results)



@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html" )

@app.route("/contact")
def contact():
    return render_template("contact.html" )
@app.route("/")
def home():
    return render_template("main.html",)

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()

        if existing_user:
            flash("Username or email already registered!", "warning")
            return redirect("/register")  


        new_user = User(
            username=form.username.data,
            password=form.password.data,  
            email=form.email.data
        )

        db.session.add(new_user)
        db.session.commit()

        flash("User registered successfully!", "success")
        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Logged In", "info")
            return redirect("/")

        flash("Invalid username or password", "danger")


    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()

    flash("Logged Out", "info")
    return redirect("/")



@app.get("/ai")
def ai_page():
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    elif current_user.role != "Admin":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("home"))
    return render_template("ai.html")

@app.context_processor
def inject_counts():
    if current_user.is_authenticated:
        cart_count = int(CartItem.query.filter_by(user_id=current_user.id).count())
        wishlist_count = int(WishlistItem.query.filter_by(user_id=current_user.id).count())
    else:
        cart_count = 0
        wishlist_count = 0

    return dict(cart_count=cart_count, wishlist_count=wishlist_count)