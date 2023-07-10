from app import create_app
app = create_app()

# The run command of the flask script starts the development server
# It replaces the Flask.run() method in most cases, and is recommended from
# Flask 0.11 onwards
#
#if __name__ == '__main__':
#    app.run()