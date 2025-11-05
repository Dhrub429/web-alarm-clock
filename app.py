from flask import Flask, render_template, request
from datetime import datetime, timedelta
import threading, time

app = Flask(__name__)

def alarm_thread(target_dt_str, snooze_seconds):
    target_dt = datetime.strptime(target_dt_str, "%Y-%m-%d %H:%M:%S")
    while True:
        now = datetime.now()
        if now >= target_dt:
            print("⏰ Alarm Triggered!")
            time.sleep(snooze_seconds)
            print("🔁 Snooze Over - Alarm again!")
            break
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        alarm_input = request.form["alarm_time"]
        snooze_h = int(request.form["snooze_hours"])
        snooze_m = int(request.form["snooze_minutes"])
        snooze_s = int(request.form["snooze_seconds"])

        try:
            dt_input = datetime.strptime(alarm_input, "%I:%M:%S %p").time()
        except ValueError:
            message = "❌ Invalid format! Use HH:MM:SS AM/PM"
            return render_template("index.html", message=message)

        today = datetime.now().date()
        target_dt = datetime.combine(today, dt_input)
        if target_dt < datetime.now():
            target_dt += timedelta(days=1)

        threading.Thread(
            target=alarm_thread,
            args=(target_dt.strftime("%Y-%m-%d %H:%M:%S"),
                  snooze_h*3600 + snooze_m*60 + snooze_s)
        ).start()

        message = f"✅ Alarm set for {alarm_input}. Snooze: {snooze_h}h {snooze_m}m {snooze_s}s"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
