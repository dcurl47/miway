from flask import request, Flask
app = Flask(__name__)

@app.route('/action', methods=['POST', 'GET'])
def helloworld():
    x = "Hello " + request.form['firstname']
    return(x)

@app.route('/start')
def initpage():
    x = "<html>"
    x = x + "<body>"
    x = x + "<form name='foo' action='http://127.0.0.1:5000/action' method='post'>"
    x = x + "Firstname <input type='text' name='firstname'>"
    x = x + "<input type=submit name=submit value=submit>"
    x = x + "</form></body></html>"
    return (x)

app.run()

