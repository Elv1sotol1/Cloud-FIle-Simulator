from flask import Flask, render_template, request, redirect, url_for, flash
from database_setup import initialize_database
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Initialize database
db_manager = initialize_database()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
       
        if action == 'upload':
            filename = request.form.get('filename')
            if filename:
                upload_time = str(datetime.datetime.now())
                db_manager.insert_file(filename, upload_time)
                flash(f'File {filename} uploaded successfully!', 'success')
       
        elif action == 'update':
            old_filename = request.form.get('old_filename')
            new_filename = request.form.get('new_filename')
            if old_filename and new_filename:
                db_manager.update_filename(old_filename, new_filename)
                flash(f'Filename updated from {old_filename} to {new_filename}', 'success')
       
        elif action == 'delete':
            filename = request.form.get('filename')
            if filename:
                db_manager.delete_file(filename)
                flash(f'File {filename} deleted successfully!', 'danger')
       
        return redirect(url_for('index'))
   
    # Retrieve files from database
    files = db_manager.get_all_files()
    return render_template('index.html', files=files)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if request.method == 'POST':
        new_filename = request.form.get('new_filename')
        if filename and new_filename:
            db_manager.update_filename(filename, new_filename)
            flash(f'Filename updated from {filename} to {new_filename}', 'success')
        return redirect(url_for('index'))
   
    return render_template('edit.html', filename=filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    if filename:
        db_manager.delete_file(filename)
        flash(f'File {filename} deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)