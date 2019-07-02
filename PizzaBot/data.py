import sqlite3
from pbwrap import Pastebin
import ast

conn = sqlite3.connect('userinfo.db')
c = conn.cursor()
pastebin = Pastebin(PASTEBIN TOKEN) 
user_id = pastebin.authenticate(PASTEBIN US, PASTEBIN PASS)

def begin():
    global conn
    global c
    conn = sqlite3.connect('userinfo.db')
    c = conn.cursor() 

def end():
    c.close()
    conn.close()

def create():
    begin()
    c.execute('CREATE TABLE IF NOT EXISTS userInfo(user INTEGER, fname TEXT, lname TEXT, phone INTEGER, email TEXT, address TEXT, credit TEXT, items TEXT, paytype TEXT)')
    end()

def checkexists(id):
    begin()
    c.execute(f'SELECT user FROM userInfo WHERE user={id}') 
    if c.fetchone() is None:
        c.execute(f"INSERT INTO userInfo VALUES({id}, '', '', ?, '', '', '', '[]', '')", (None,))

def showvals(ctx):
    checkexists(ctx.author.id)
    c.execute(f"SELECT * FROM userInfo WHERE user={ctx.author.id}")
    x=c.fetchone()
    end()
    return x 

def setname(ctx, fname, lname):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET fname='{fname}' WHERE user={ctx.author.id}")
    c.execute(f"UPDATE userInfo SET lname='{lname}' WHERE user={ctx.author.id}")
    conn.commit()
    end()

def setphone(ctx, phone):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET phone={phone} WHERE user={ctx.author.id}")
    conn.commit()
    end()

def setemail(ctx, mail):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET email='{mail}' WHERE user={ctx.author.id}")
    conn.commit()
    end()

def setaddress(ctx, addr):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET address='{addr}' WHERE user={ctx.author.id}")
    conn.commit()
    end()

def getaddress(ctx):
    checkexists(ctx.author.id)
    c.execute(f"SELECT address FROM userInfo WHERE user={ctx.author.id}")
    dat = c.fetchone()
    if dat[0] is None or dat[0]=='':
        end()
        return False 
    else:
        end()
        return dat[0]

def pastemenu(paste):
    url = pastebin.create_paste(paste, api_paste_private=1, api_paste_name='Menu', api_paste_expire_date='10M', api_paste_format=None)
    return url

def setcredit(ctx, car, exp, cvv, zipc):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET credit='{car}, {exp}, {cvv}, {zipc}' WHERE user={ctx.author.id}")
    conn.commit()
    end()

def clear(ctx):
    checkexists(ctx.author.id)
    c.execute(f"DELETE FROM userInfo WHERE user={ctx.author.id}")
    conn.commit()
    end()

def vcust(val):
    if val[1]=='' or val[3] is None or val[4]=='' or val[5]=='':
        return False
    else:
        return True

def additem(ctx, code):
    begin()
    c.execute(f'SELECT items FROM userInfo WHERE user={ctx.author.id}') 
    x=c.fetchone()[0]
    lst=ast.literal_eval(x)
    if code in lst: 
        end()
        return False
    else:
        lst.append(code)
        c.execute(f"UPDATE userInfo SET items=? WHERE user={ctx.author.id}", (str(lst),))
        conn.commit()
        end()
        return True

def removeitem(ctx, code):
    begin()
    c.execute(f'SELECT items FROM userInfo WHERE user={ctx.author.id}') 
    x=c.fetchone()[0]
    lst=ast.literal_eval(x)
    if code not in lst:
        end()
        return False
    else:
        lst.remove(code)
        c.execute(f"UPDATE userInfo SET items=? WHERE user={ctx.author.id}", (str(lst),))
        conn.commit()
        end()
        return True

def setpaytype(ctx, typ):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET paytype='{typ}' WHERE user={ctx.author.id}")
    conn.commit()
    end()

def checkcredit(ctx):
    checkexists(ctx.author.id)
    c.execute(f"SELECT credit FROM userInfo WHERE user={ctx.author.id}")
    dat = c.fetchone()
    if dat[0] is None or dat[0]=='':
        end()
        return False 
    else:
        end()
        return dat[0]

def showorder(ctx):
    checkexists(ctx.author.id)
    c.execute(f'SELECT items FROM userInfo WHERE user={ctx.author.id}') 
    x=c.fetchone()[0]
    lst=ast.literal_eval(x)
    end()
    return lst

def clearorder(ctx):
    checkexists(ctx.author.id)
    c.execute(f"UPDATE userInfo SET items='[]' WHERE user={ctx.author.id}")
    conn.commit()
    end()
