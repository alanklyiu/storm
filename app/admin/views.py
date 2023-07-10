from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from io import StringIO
import csv

from . import admin_bp
from .forms import DepartmentForm, RoleForm, UploadForm
from .. import db
from ..models import Department, Role


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin_bp.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()
    form = UploadForm()

    if form.validate_on_submit():

        csv_file = StringIO()

        try:
            # request.files returns an ImmutableMultiDict containing the file as
            # a FileStorage object.
            #
            # bytes.decode() returns a string decoded from the given bytes where
            # default encoding is 'utf-8'.
            #
            # It is possible to use a str or bytes-like object as a file for reading &
            # writing. For strings StringIO can be used like a file opened in text mode.
            csv_file = StringIO(request.files['upload'].read().decode())

            csv_content = csv.DictReader(csv_file)

            for row in csv_content:
                department = Department(name=row['name'], description=row['description'])
                db.session.add(department)
            db.session.commit()
            flash('You have successfully imported the new department(s).')

        except UnicodeDecodeError:
            flash('Unicode Decode Error')

        except:
            db.session.rollback()
            flash('Error')

        finally:
            csv_file.close()

        return redirect(url_for('admin.list_departments'))

    return render_template('admin/departments/departments.html', form=form,
                           departments=departments, title="Departments")


@admin_bp.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    form = DepartmentForm()
    if form.validate_on_submit():
        # Populates the attributes of the passed department obj with data from the form's fields
        #department = Department(name=form.name.data, description=form.description.data)
        department = Department()
        form.populate_obj(department)

        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add", form=form,
                           title="Add Department")


@admin_bp.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    department = Department.query.get_or_404(id)
    # The obj parameter is used to populate form defaults on the initial view.
    # If there is any POST data at all, then the object data is ignored.
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        #department.name = form.name.data
        #department.description = form.description.data
        form.populate_obj(department)

        try:
            db.session.commit()
            flash('You have successfully edited the department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # To prevent a refresh from duplicating form submissions, POST requests are
        # responded with a redirect instead of a normal response. When the browser
        # receives this response, it issues a GET request for the redirect URL.
        # This is a best-practice associated w/ the Post/Redirect/Get design pattern.
        return redirect(url_for('admin.list_departments'))

    #form.description.data = department.description
    #form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit", form=form,
                           title="Edit Department")


@admin_bp.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))


# Role Views


@admin_bp.route('/roles')
@login_required
def list_roles():
    """
    List all roles
    """
    check_admin()

    roles = Role.query.all()

    return render_template('admin/roles/roles.html', roles=roles, title='Roles')


@admin_bp.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    form = RoleForm()
    if form.validate_on_submit():
        #role = Role(name=form.name.data, description=form.description.data)
        role = Role()
        form.populate_obj(role)
        
        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', action="Add", form=form,
                           title='Add Role')


@admin_bp.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        #role.name = form.name.data
        #role.description = form.description.data
        form.populate_obj(role)

        try:
            db.session.commit()
            flash('You have successfully edited the role.')
        except:
            # in case department name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    #form.description.data = role.description
    #form.name.data = role.name
    return render_template('admin/roles/role.html', action="Edit", form=form,
                           title="Edit Role")


@admin_bp.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))