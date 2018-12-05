from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime, timedelta
import pymysql
import pymysql.cursors

conn= pymysql.connect(host='localhost', user='root', password='Rainbow.86', db='Project')
app = Flask(__name__)

counterMatIndent = 4
sequencecounterMatIndent = 0
Ndays = 10
orderidcounter = 5
sequencecounterPurchaseOrder = 0
receiptID = 5

@app.route('/AdminHome')
def AdminHome():
    return render_template('adminhome.html')

@app.route('/AdminChangeInfo', methods = ['GET', 'POST'])
def AdminChangeInfo():
    a = conn.cursor()
    error = None
    if request.method == 'POST':
        Name = request.form['Username']
        Password = request.form['Pass']
        FName = request.form['FName']
        LName = request.form['LName']
        Email = request.form['Email']
        Address = request.form['Address']
        ContactDetail = request.form['ContactDetail']
        Gender = request.form['Gender']
        changesql = 'UPDATE UserTable Set FName = %s, LName = %s, Email = %s, HomeAddress = %s, ContactDetail = %s, Gender = %s WHERE Username = %s AND Pass = %s'
        a.execute(changesql, (FName, LName, Email, Address, ContactDetail, Gender, Name, Password))
        conn.commit()
        return redirect(url_for('AdminHome'))
    return render_template('adminchangeinfo.html')

@app.route('/AdminUpdatePass', methods = ['GET', 'POST'])
def AdminUpdate():
    a = conn.cursor()
    error = None
    if request.method =='POST':
        Name = request.form['Username']
        Password = request.form['Pass']
        passupsql = 'UPDATE UserTable SET Pass = %s WHERE Username = %s'
        a.execute(passupsql, (Password, Name))
        conn.commit()
        return redirect(url_for('AdminHome'))
    return render_template('adminupdate.html', error = error)

@app.route('/AdminAdd', methods = ['GET', 'POST'])
def AdminAdd():
    a = conn.cursor()
    error = None
    if request.method =='POST':
        Name = request.form['Username']
        Password = request.form['Pass']
        Role = request.form['UserRole']
        FName = request.form['FName']
        LName = request.form['LName']
        Email = request.form['Email']
        Address = request.form['Address']
        ContactDetail = request.form['ContactDetail']
        Gender = request.form['Gender']
        addsql = 'INSERT INTO UserTable VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        a.execute(addsql, (Name, Password, Role, FName, LName, Email, Address, ContactDetail, Gender))
        conn.commit()
        return redirect(url_for('AdminHome'))
    return render_template('adminadd.html', error = error)

####################################################
@app.route('/ManagerHome')
def ManagerHome():
    return render_template('managerhome.html')

####################################################
#counterMatIndent = 4
#sequencecounterMatIndent = 0
#Ndays = 10
#orderidcounter = 5
#sequencecounterPurchaseOrder = 0
#receiptID = 5

@app.route('/ShopHome')
def ShopHome():
    return render_template('shophome.html')


@app.route('/search', methods =['GET', 'POST'])
def ShopSearch():
    global counterMatIndent
    global sequencecounterMatIndent
    global Ndays
    Date_N_Days_From_Now = datetime.now() + timedelta(days=Ndays)
    a = conn.cursor()
    error = None
    if request.method == 'POST':
        item = request.form['searchitem']
        vendorname = request.form['searchvendor']
        quantity = request.form['quantity']
        altitembool = request.form['altitem']
        print(item)
        print(vendorname)
        sql = 'SELECT * FROM Item HAVING ItemName = %s AND VendorName = %s'
        a.execute(sql, (item, vendorname))
        results = a.fetchone()
        print(results)
        N1 = results[0]
        sql2 = 'INSERT INTO MaterialIndent VALUES (%s, %s, %s, %s, %s, %s)'
        a.execute(sql2, (counterMatIndent, sequencecounterMatIndent, N1, Date_N_Days_From_Now.date(), quantity, altitembool))
        conn.commit()
        #print(results)
        return redirect(url_for('PurchaseOrderCreate'))
    return render_template('fancysearch.html', error = error)

@app.route('/PurchaseOrderCreate', methods =['GET', 'POST'])
def PurchaseOrderCreate():
    a = conn.cursor()
    error = None
    if request.method == 'POST':
        global counterMatIndent
        global sequencecounterMatIndent
        global orderidcounter
        global sequencecounterPurchaseOrder
        VendorNameSql = request.form['VendorName']
        print(VendorNameSql)
        sql = 'INSERT INTO PurchaseOrder VALUES (%s, %s, %s, %s, %s)'
        a.execute(sql, (orderidcounter, sequencecounterPurchaseOrder, counterMatIndent, sequencecounterMatIndent, VendorNameSql))
        conn.commit()
        sequencecounterMatIndent = sequencecounterMatIndent + 1
        sequencecounterPurchaseOrder = sequencecounterPurchaseOrder + 1
        return redirect(url_for('OrderMoreItems'))
    return render_template('purchaseordervendorfill.html', error = error)

@app.route('/OrderMoreItems')
def OrderMoreItems():
    print(sequencecounterMatIndent)
    return render_template('shophomeaftersearch.html')

@app.route('/CreateNewIndent', methods = ['GET', 'POST'])
def CreateNewIndent():
    global counterMatIndent
    counterMatIndent = counterMatIndent + 1
    global sequencecounterMatIndent
    sequencecounterMatIndent = 0
    global Ndays
    Date_N_Days_From_Now = datetime.now() + timedelta(days=Ndays)
    a = conn.cursor()
    error = None
    if request.method == 'POST':
        item = request.form['searchitem']
        vendorname = request.form['searchvendor']
        quantity = request.form['quantity']
        altitembool = request.form['altitem']
        print(item)
        print(vendorname)
        sql = 'SELECT * FROM Item HAVING ItemName = %s AND VendorName = %s'
        a.execute(sql, (item, vendorname))
        results = a.fetchone()
        print(results)
        N1 = results[0]
        sql2 = 'INSERT INTO MaterialIndent VALUES (%s, %s, %s, %s, %s, %s)'
        a.execute(sql2, (counterMatIndent, sequencecounterMatIndent, N1, Date_N_Days_From_Now.date(), quantity, altitembool))
        conn.commit()
        # print(results)
        return redirect(url_for('OrderMoreItems'))
    return render_template('fancysearch.html', error=error)


@app.route('/AddANewPurchaseOrder')
def AddANewPurchaseOrder():
    global orderidcounter
    global sequencecounterPurchaseOrder
    global receiptID
    dateoforder = datetime.now()
    print(dateoforder)
    a = conn.cursor()
    sqldatainsert = 'INSERT INTO GoodsReceipt VALUES (%s, %s, %s, %s, %s, %s, %s)'
    a.execute(sqldatainsert, (receiptID, orderidcounter, dateoforder.date(), 'Pending', 'Address', 'Payment', 0.00))
    conn.commit()
    receiptID = receiptID + 1
    orderidcounter = orderidcounter + 1
    sequencecounterPurchaseOrder = 0
    return render_template('shopcreateanotherpurchaseorder.html')

@app.route('/CreateGoodsReceipt')
def CreateGoodsReceipt():
    global receiptID
    a = conn.cursor()
    sql = 'SELECT * FROM GoodsReceipt WHERE ReceiptID = %s'
    a.execute(sql, (receiptID))
    conn.commit()
    return(redirect(url_for('ShopHome')))
######################################

@app.route('/VendorHome')
def VendorHome():
    return render_template('vendorhome.html')

@app.route('/VendorAdd', methods = ['GET', 'POST'])
def VendorAdd():
    a = conn.cursor()
    error = None
    if request.method =='POST':
        vname = request.form['VendorName']
        #print(vname)
        minquant = request.form['MinOrderQuant']
        quality = request.form['Quality']
        email = request.form['Email']
        phoneno = request.form['PhoneNo']
        addsql = 'INSERT INTO Vendor VALUES (%s, %s, %s, %s, %s)'
        a.execute(addsql, (vname, minquant, quality, email, phoneno))
        conn.commit()
        return redirect(url_for('VendorHome'))
    return render_template('vendoradd.html', error = error)

#######################################
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usern = request.form['username']
        passw = request.form['password']
        a = conn.cursor()
        sql = 'SELECT * FROM UserTable WHERE Username = %s AND Pass = %s'
        a.execute(sql, (usern, passw))
        data = a.fetchone()
        if data[2] == "Admin":
            return redirect(url_for('AdminHome'))
        elif data[2] == "Shop":
            return redirect(url_for('ShopHome'))
        elif data[2] == 'Manager':
            return redirect(url_for('ManagerHome'))
        elif data[2] == "Vendor":
            return redirect(url_for('VendorHome'))
        #....
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('fancylogin.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)


