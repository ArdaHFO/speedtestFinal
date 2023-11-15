from flask import Flask, render_template
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix = "/views")
#----------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')
#----------------------------------------------------------------------------------------------------   
@app.route('/ping')
def ping():
    return 'Pong'
#----------------------------------------------------------------------------------------------------   
@app.route('/upload')
def upload():
    if 'file' not in request.files:
        return 'File not found.'

    file = request.files['file']

    if file.filename == '':
        return 'Filename is empty.'

    file.save('uploads/' + file.filename)
    return 'The file has been uploaded successfully: ' + file.filename
#----------------------------------------------------------------------------------------------------   
if __name__ == '__main__':
    app.run(debug=True, port=8000,host='0.0.0.0')
#----------------------------------------------------------------------------------------------------
