from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Employee, Seller, Project, Expense, Revenue
from forms import EmployeeForm, ProjectForm, ExpenseForm, RevenueForm
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

routes = Blueprint('routes', __name__)

# Home
@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    form = EmployeeForm()
    employees = Employee.query.all()

    # Handle form submission
    if form.validate_on_submit():
        employee = Employee(name=form.name.data, designation=form.designation.data)
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('routes.manage_employees'))

    return render_template('employees.html', form=form, employees=employees)

@routes.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        employee.name = form.name.data
        employee.designation = form.designation.data
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('routes.manage_employees'))

    return render_template('edit_employee.html', form=form, employee=employee)

@routes.route('/employees/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'danger')
    return redirect(url_for('routes.manage_employees'))

@routes.route('/expenses', methods=['GET', 'POST'])
def log_expenses():
    form = ExpenseForm()

    # Populate dropdowns
    form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]
    form.employee_id.choices = [(e.id, e.name) for e in Employee.query.all()]

    if form.validate_on_submit():
        try:
            # Handle Seller
            seller_name = form.seller_name.data
            gstn = form.gstn.data
            print(f"Trying to find seller with GSTN: {gstn}")
            
            # Find seller or create a new one
            seller = Seller.query.filter_by(gstn=gstn).first()
            if not seller:
                print(f"Seller not found, creating a new seller: {seller_name}, GSTN: {gstn}")
                seller = Seller(name=seller_name, gstn=gstn)
                db.session.add(seller)
                db.session.commit()
                print(f"Seller created: {seller.name}, GSTN: {seller.gstn}")

            # Calculate the total amount
            total_amount = (form.unit_price.data * form.quantity.data) + form.gst_amount.data

            # Create and save the expense
            expense = Expense(
                expense_type=form.expense_type.data,
                quantity=form.quantity.data,
                item_name=form.item_name.data,
                unit_price=form.unit_price.data,
                gst_amount=form.gst_amount.data,
                total_amount=total_amount,
                invoice_number=form.invoice_number.data,
                seller_id=seller.id,
                employee_id=form.employee_id.data,
                project_id=form.project_id.data
            )

            db.session.add(expense)
            db.session.commit()  # Commit the transaction
            flash('Expense logged successfully!', 'success')
            return redirect(url_for('routes.log_expenses'))
            

        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            print(f"Error while committing: {str(e)}")  # Print error message
            flash(f"Error: {e}", 'danger')  # Show error to the user
            return redirect(url_for('routes.log_expenses'))
      
    # Fetch all expenses for displaying
    expenses = Expense.query.all()
    return render_template('expenses.html', form=form, expenses=expenses)
    
@routes.route('/revenue', methods=['GET', 'POST'])
def log_revenue():
    form = RevenueForm()

    # Populate dropdowns
    form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]
    form.employee_id.choices = [(e.id, e.name) for e in Employee.query.all()]

    if form.validate_on_submit():
        try:
            # Create and save the revenue
            revenue = Revenue(
                project_id=form.project_id.data,
                total_estimated_revenue=form.total_estimated_revenue.data,
                employee_id=form.employee_id.data
            )
            db.session.add(revenue)
            db.session.commit()
            flash('Revenue logged successfully!', 'success')
            return redirect(url_for('routes.log_revenue'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", 'danger')

    # Fetch and display all revenues
    revenues = Revenue.query.all()
    return render_template('revenue.html', form=form, revenues=revenues)


@routes.route('/projects', methods=['GET', 'POST'])
def manage_projects():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data)
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('routes.manage_projects'))

    projects = Project.query.all()
    return render_template('projects.html', form=form, projects=projects)

@routes.route('/projects/<int:id>')
def view_project(id):
    project = Project.query.get_or_404(id)
    expenses = Expense.query.filter_by(project_id=id).all()
    revenues = Revenue.query.filter_by(project_id=id).all()
    total_expenses = sum(e.total_amount for e in expenses)
    total_revenues = sum(r.total_estimated_revenue for r in revenues)
    return render_template('view_project.html', project=project, expenses=expenses,
                           revenues=revenues, total_expenses=total_expenses,
                           total_revenues=total_revenues)

@routes.route('/report')
def report():
    projects = Project.query.all()

    project_reports = []
    for project in projects:
        total_expenses = sum(expense.total_amount for expense in project.expenses)
        total_revenues = sum(revenue.total_estimated_revenue for revenue in project.revenues)

        # Debugging
        print(f"Project: {project.name}, Total Expenses: {total_expenses}, Total Revenues: {total_revenues}")

        project_reports.append({
            'name': project.name,
            'total_expenses': total_expenses,
            'total_revenues': total_revenues
        })

    sellers = Seller.query.all()
    items = Expense.query.distinct(Expense.item_name).all()

    return render_template('report.html', project_reports=project_reports, sellers=sellers, items=items)


@routes.route('/forecast')
def forecast():
    data = [expense.total_amount for expense in Expense.query.all()]
    
    if len(data) < 3:  # Ensure enough data points for ARIMA
        flash("Not enough data for forecasting", "warning")
        return redirect(url_for('routes.index'))

    # Create a time series and fit ARIMA model
    series = pd.Series(data)
    model = ARIMA(series, order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast next 3 months
    forecast = model_fit.forecast(steps=3)

    return render_template('forecast.html', forecast=forecast, enumerate=enumerate)  # Pass enumerate to the template
