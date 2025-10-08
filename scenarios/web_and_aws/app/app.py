from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        cmd = request.form.get("cmd", "").strip()
        result = subprocess.check_output(cmd, shell=True, text=True)
    
    return render_template_string("""
        <h2>CMD!??!?!?</h2>
        <form method="POST">
            <input name="cmd" style="width:300px">
            <button type="submit">submit</button>
        </form>
        <pre>{{ result }}</pre>
    """, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8009)
