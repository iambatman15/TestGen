from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Configuration dictionary
config = {
    "sections": [],
    "pyq_upload": None,
    "content_upload": None,
    "focus_topics": None
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get section data
        num_sections = int(request.form["num_sections"])
        sections = []
        for i in range(num_sections):
            section = {
                "type": request.form[f"section_{i}_type"],
                "num_questions": request.form[f"section_{i}_num_questions"],
                "marks": request.form[f"section_{i}_marks"]
            }
            sections.append(section)

        # Get PYQ upload
        pyq_file = request.files["pyq_upload"]
        if pyq_file:
            pyq_filename = secure_filename(pyq_file.filename)
            pyq_file.save(os.path.join(app.config["UPLOAD_FOLDER"], pyq_filename))
            config["pyq_upload"] = pyq_filename

        # Get content upload
        content_file = request.files["content_upload"]
        if content_file:
            content_filename = secure_filename(content_file.filename)
            content_file.save(os.path.join(app.config["UPLOAD_FOLDER"], content_filename))
            config["content_upload"] = content_filename

        # Get focus topics
        focus_topics = request.form["focus_topics"]
        if focus_topics:
            config["focus_topics"] = focus_topics

        # Get weightage for PYQs
        pyq_weightage = request.form["pyq_weightage"]
        if pyq_weightage:
            config["pyq_weightage"] = pyq_weightage

        # Store configuration
        config["sections"] = sections

        # Save configuration
        if request.form["action"] == "save_config":
            with open("config.json", "w") as f:
                json.dump(config, f)
            return "Configuration saved successfully!"

        # Generate question paper
        elif request.form["action"] == "generate_qp":
            # Logic to generate question paper goes here
            return "Question paper generated successfully!"

    return render_template("ipscan.html")


if __name__ == "__main__":
    app.run(debug=True)