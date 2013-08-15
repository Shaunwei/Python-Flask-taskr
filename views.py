#views.py

from flasktaskr import app, db
from flask import flash, redirect, render_template, request, \
                    session, url_for
from functools import wraps
from flasktaskr.forms import AddTask
from flasktaskr.models import FTasks


#decorator function to control login    
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

    
#logout    
@app.route('/logout/')
def logout():
    session.pop('logged_in',None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

    
#main login    
@app.route('/',methods=['POST','GET'])
def login():
    error = None
    if request.method =="POST":
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('tasks'))
    return render_template('login.html', error=error)


#Task fetch all from db    
@app.route('/tasks/')
@login_required
def tasks(error=None):
    error = error
    open_tasks = db.session.query(FTasks).filter_by(status='1').order_by(FTasks.due_date.asc())
    closed_tasks = db.session.query(FTasks).filter_by(status='0').order_by(FTasks.due_date.asc())
    return render_template('tasks.html',form = AddTask(request.form),
            open_tasks=open_tasks, closed_tasks = closed_tasks, error=error)


#Add new tasks:
@app.route('/add/',methods=['POST'])
@login_required
def new_task():
    form = AddTask(request.form)
    error = None
    if form.validate():
        new_task = FTasks(
                    form.name.data,
                    form.due_date.data,
                    form.priority.data,
                    '1'
                    )
        db.session.add(new_task)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
    else:
        error = 'Invalid data. Please try again :) '
        return tasks(error)
    return redirect(url_for('tasks'))

        
#Mark tasks as complete:
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).update({"status":"0"})
    db.session.commit()
    flash('The task was marked as complete. Nice.')
    return redirect(url_for('tasks'))
    

#Delete Tasks:
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task was deleted. Why not add a new one?')
    return redirect(url_for('tasks'))

    
#Uncomplete the closed tasks:
@app.route('/uncomplete/<int:task_id>/',)
@login_required
def uncomplete(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).update({'status':'1'})
    db.session.commit()
    flash('The task was marked as uncomplete.')
    return redirect(url_for('tasks'))
    