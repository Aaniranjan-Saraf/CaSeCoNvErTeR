from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Define the file upload form
class FileUploadForm(FlaskForm):
    file = FileField('Upload File')
    submit = SubmitField('Convert')

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    form = FileUploadForm()

    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            converted_filepath = convert_case_file(filepath)

            return send_file(converted_filepath, as_attachment=True)

    return render_template('home.html', form=form)

# Function to convert case and return the modified file path
def convert_case_file(filepath):
    file_name, file_extension = os.path.splitext(filepath)
    output_file = file_name + 'Changed' + file_extension

    with open(filepath, 'r') as file:
        content = file.read()

    converted_content = convert_case(content)

    with open(output_file, 'w') as file:
        file.write(converted_content)

    return output_file

# Function to convert the case of text
def convert_case(text):
    converted_text = ""
    for char in text:
        if char.isupper():
            converted_text += char.lower()
        elif char.islower():
            converted_text += char.upper()
        else:
            converted_text += char
    return converted_text

if __name__ == '__main__':
    app.run(debug=True)
