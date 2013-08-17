#views.py

from app import app, db
from flask import flash, redirect, render_template, request, \
                    session, url_for
from functools import wraps
from app.forms import AddTask, RegisterForm, LoginForm
from app.models import FTasks, User
from sqlalchemy.exc import IntegrityError


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
    session.pop('user_id',None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

    
#main login    
@app.route('/',methods=['POST','GET'])
def login():
    error = None
    if request.method =="POST":
        name = request.form['username']
        password = request.form['password']
        #u = User.query.filter_by(name=name,password=password).first()
        u = db.session.query(User).filter_by(name=name,password=password).first()
        if u is None:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            flash('You are logged in. Go Crazy.')
            return redirect(url_for('tasks'))
    return render_template('login.html', form=LoginForm(request.form),error=error)


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
@app.route('/add/',methods=['POST','GET'])
@login_required
def new_task():
    form = AddTask(request.form)
    error = None
    if form.validate():
        new_task = FTasks(
                    form.name.data,
                    form.due_date.data,
                    form.priority.data,
                    form.posted_date.data,
                    '1',
                    session['user_id']
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
    
    
#for new user to register
@app.route('/register/', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if form.validate():
        new_user = User(
                form.name.data,
                form.email.data,
                form.password.data,
                )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        except IntegrityError:
            error = 'Oh no! That username and/or email already exist. Please try again.'
    else:
        if request.method == "POST" :
            flash_errors(form)    
    return render_template('register.html', form = form, error=error)
    

#display error messages on template
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash (u"Error in the %s field - %s"%(
                    getattr(form,field).label.text, error),'error')
    

#errorhandler

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),500
    
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'),400
    
    