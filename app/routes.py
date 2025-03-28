from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Workout, db
from .forms import WorkoutForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    workouts = Workout.query.all()
    return render_template('index.html', workouts=workouts)

@main.route('/home')
@login_required
def home():
    workouts = current_user.workouts
    return render_template('home.html', workouts=workouts, user=current_user)

@main.route('/workouts', methods=['GET', 'POST'])
@login_required
def manage_workouts():
    form = WorkoutForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_workout = Workout(
            type=form.type.data,
            duration=form.duration.data,
            user_id=current_user.id  # Auto-calculates calories
        )
        try:
            db.session.add(new_workout)
            db.session.commit()
            flash('Workout added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding workout: {e}", 'error')
        return redirect(url_for('main.home'))
    
    return render_template('workout_details.html', form=form)


@main.route('/workouts/<int:workout_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@login_required
def manage_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    
    if request.method == 'GET':
        return jsonify(workout.to_dict())
    
    # For PUT and PATCH, only allow updates to type and duration (calories_burned is auto-calculated)
    elif request.method in ['PUT', 'PATCH']:
        data = request.get_json()
        
        if 'type' in data:
            workout.type = data['type']
        if 'duration' in data:
            workout.duration = data['duration']
        
        # Since calories_burned is auto-calculated, no need to update it directly
        workout.calories_burned = workout.calculate_calories()  # Recalculate calories based on new data
        
        db.session.commit()
        return jsonify(workout.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return '', 204

    
@main.route('/delete_workout/<int:workout_id>', methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('You do not have permission to delete this workout.', 'error')
        return redirect(url_for('main.home'))
    
    try:
        db.session.delete(workout)
        db.session.commit()
        flash('Workout deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting workout: {e}", 'error')
    
    return redirect(url_for('main.home'))
