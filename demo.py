from flask import Flask,redirect,url_for, request #importing the module
app=Flask(__name__) #initiating flask object
@app.route('/welcome/<name>') #defining a route in the application
def greet(name):
    return f"Welcome to PythonGeeke, {name}!"
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('greet',name = user))
   else:
      user = request.args.get('name')
      return redirect(url_for('greet',name = user))
if __name__=='__main__': #calling  main 
       app.debug=True #setting the debugging option for the application instance
       app.run() #launching the flask's integrated development webserver