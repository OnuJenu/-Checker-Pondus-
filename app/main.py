# Entry point of the application to start the server

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
