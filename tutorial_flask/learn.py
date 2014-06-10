from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello World!'

from flask import render_template
@app.route('/hello2/')
@app.route('/hello2/<name>')
def hello2(name=None):
    return render_template('hello.html',name=name)



@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

#@app.route('/login')
#def login()
#   return


##################################
from flask import request

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        #do_the_login()
        return 'POSt!!!'
    else:
        #show_the_login_form()
        return 'GET!!!'

  
########################################
with app.test_request_context('/hello',method='POST'):
    #print url_for('login')
    assert request.path == '/hello'
    assert request.method == 'POST'

if __name__ == '__main__':
    app.run(debug=True)


