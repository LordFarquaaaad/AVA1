from app import create_app, db
import os

app = create_app()

print("🔍 Current working directory:", os.getcwd())
print("🔍 Templates folder contents:", os.listdir("templates"))


if __name__ == "__main__":
    app.run(debug=True)
