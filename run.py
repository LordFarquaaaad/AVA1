from backend import create_app, db
import os

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
