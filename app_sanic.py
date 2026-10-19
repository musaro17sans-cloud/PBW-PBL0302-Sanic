from sanic import Sanic
from sanic.response import redirect, text
from sanic_ext import render
from peewee import *

app = Sanic("CarProject")
app.static('/static', './static') 
appType = 'Sanic Framework'
database = SqliteDatabase('carsweb.db')

class BaseModel(Model):
     class Meta:
        database = database

class TBCars(BaseModel):
    carname = TextField()
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with database:
        database.create_tables([TBCars])

@app.route('/')
async def indeks(request):
    return redirect(app.url_for('readcar'))

@app.route('/readcar', methods=['GET', 'POST'])
async def readcar(request):
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        # Jika ada keyword, simpan nilai keyword untuk ditampilkan di form pencarian
        rows = list(TBCars.select().where(TBCars.carname.contains(keyword)))
    else:
        rows = list(TBCars.select())
    # Mengirimkan keyword ke template agar tetap tampil di form pencarian
    return await render('readcar.html', context={"rows": rows, "appType": appType, "keyword": keyword})

@app.route('/createcar')
async def createcar(request):
    return await render('createcar.html', context={"appType": appType})

@app.route('/createcarsave', methods=['POST'])
async def createcarsave(request):
    fName = request.form.get('carName')
    fBrand = request.form.get('carBrand')
    fModel = request.form.get('carModel')
    fPrice = request.form.get('carPrice')
    TBCars.create(carname=fName, carbrand=fBrand, carmodel=fModel, carprice=fPrice)
    return redirect(app.url_for('readcar'))

@app.route('/updatecar')
async def updatecar(request):
    car_id = request.args.get('id')
    # Ambil data spesifik berdasarkan ID
    car_data = TBCars.get(TBCars.id == car_id)
    return await render('updatecar.html', context={"appType": appType, "car": car_data})

@app.route('/updatecarsave', methods=['POST'])
async def updatecarsave(request):
    car_id = request.form.get('id')
    fName = request.form.get('carName')
    fBrand = request.form.get('carBrand')
    fModel = request.form.get('carModel')
    fPrice = request.form.get('carPrice')
    # Update berdasarkan ID, bukan nama
    query = TBCars.update(carname=fName, carbrand=fBrand, carmodel=fModel, carprice=fPrice).where(TBCars.id == car_id)
    query.execute()
    return redirect(app.url_for('readcar'))

@app.route('/deletecar')
async def deletecar(request):
    car_id = request.args.get('id')
    # Ambil data spesifik berdasarkan ID
    car_data = TBCars.get(TBCars.id == car_id)
    return await render('deletecar.html', context={"appType": appType, "car": car_data})

@app.route('/deletecarsave', methods=['POST'])
async def deletecarsave(request):
    car_id = request.form.get('id')
    # Hapus berdasarkan ID
    car_delete = TBCars.delete().where(TBCars.id == car_id)
    car_delete.execute()
    return redirect(app.url_for('readcar'))

@app.route('/help')
async def help(request):
    return text("ini halaman Helps")

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=8000, dev=True)