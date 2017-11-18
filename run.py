from app import create_app

app = create_app("development")

@app.route('/')
def index():
    return 'Index Page'

@app.route('/status')
def hello_world():
    return 'Ok!'

if __name__ == '__main__':
    app.run()