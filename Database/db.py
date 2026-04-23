from flask import Flask, request, redirect
import psycopg
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_db():
    return psycopg.connect(os.getenv("DATABASE_URL"))

@app.route("/track")
def track():
    token = request.args.get("token")
    destination = request.args.get("redirect", "https://yoursite.com")

    if token:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "UPDATE link_clicks SET clicked_at = %s WHERE token = %s AND clicked_at IS NULL",
                (datetime.utcnow(), token)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"DB error: {e}")

    return redirect(destination)

if __name__ == "__main__":
    app.run(port=5000)