from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.log import Log
from flask_app.models.user import User

@app.route('/logs/add')
def new_log():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    return render_template('add_log.html', user = User.get_by_id(data))

@app.route('/logs/create', methods = ['POST'])
def create_log():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Log.validate_log(request.form):
        return redirect('/logs/add')
    data = {
        'weight' : request.form['weight'],
        'description' : request.form['description'],
        'exercise_name' : request.form['exercise_name'],
        'exercise_sets' : request.form['exercise_sets'],
        'exercise_set_1' : request.form['exercise_set_1'],
        'exercise_set_2' : request.form['exercise_set_2'],
        'exercise_set_3' : request.form['exercise_set_3'],
        'exercise_set_4' : request.form['exercise_set_4'],
        'user_id' : request.form['user_id']
    }
    Log.save(data)
    return redirect('/dashboard')

@app.route('/logs/edit/<int:id>')
def edit_log(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('edit_log.html', edit = Log.get_one(data), user = User.get_by_id(user_data))

@app.route('/logs/update', methods = ['POST'])
def update_log():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Log.validate_log(request.form):
        return redirect(f"/logs/edit/{request.form['id']}")
    data = {
        'weight' : request.form['weight'],
        'description' : request.form['description'],
        'exercise_name' : request.form['exercise_name'],
        'exercise_sets' : request.form['exercise_sets'],
        'exercise_set_1' : request.form['exercise_set_1'],
        'exercise_set_2' : request.form['exercise_set_2'],
        'exercise_set_3' : request.form['exercise_set_3'],
        'exercise_set_4' : request.form['exercise_set_4'],
        'id' : request.form['id']
    }
    Log.update(data)
    return redirect('/dashboard')

@app.route('/logs/<int:id>') #need to make logs.html page
def show_log(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("logs.html",log=Log.get_one(data),user=User.get_by_id(user_data))

@app.route('/logs/destroy/<int:id>')
def destroy_log(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Log.destroy(data)
    return redirect('/dashboard')