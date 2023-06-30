# Lumovex IT Company Task Manager
The Lumovex IT Company Task Manager is a tool designed for managing projects, tasks, employees, and task types within the IT company Lumovex.

### Features of Lumovex IT Company Task Manager:

* User Authentication: The system is built on the Django authentication system (django.contrib.auth.models.AbstractUser), which handles user registration, login, and access control.
* Company Homepage for All Users: The company's main homepage is accessible to all users for viewing.
* Personal Employee Dashboard: Upon authorization, each employee is directed to their personal dashboard, displaying their assigned projects and tasks.
* Task Search Filter: Employees can use a filter to search for tasks based on specific criteria.
* Access to Lists: Employees have access to lists of all positions, task types, projects, and employees.
* Adding, Deleting, and Editing Data: Projects, tasks, employees, positions, and task types can be added, deleted, and edited.


### Usage:
Key elements and their relationships within the Lumovex IT Company Task Manager:
* Project: Each project has a name, description, deadline, and a list of assigned workers. Projects are used to organize and manage tasks.
* Task: Tasks are created within projects and represent specific assignments. They contain information such as name, description, creation date, deadline, completion status, priority, task type, assigned workers, and the project they belong to.
* Worker: Workers are employees of the IT company. Each worker has a name, position, and can be assigned to projects and tasks.
* Position: Positions represent different roles or job positions within the company. Each worker is associated with a specific position.
* TaskType: Task types categorize tasks based on different types or categories.


##### DB structure
![db_structure](db_structure.png)


### Getting Started:
To start using the Lumovex IT Company Task Manager, follow these steps:


1. Install the necessary dependencies and ensure Django is properly configured.
2. Configure the database parameters in the project's settings.py file.
3. Perform database migrations to create the required tables for the models.
4. Configure user authentication and registration functionality if needed.
5. Integrate the provided models and their relationships into your Django project.
6. Customize and extend the functionality according to your project requirements.
 
 
### Access Control:

* The company's main homepage is accessible to all users.
* The rest of the functionality is accessible only to authorized employees of the company.
* Upon authorization, employees are directed to their personal page displaying their projects and tasks.
* 

### Data Editing:

Projects, tasks, employees, positions, and task types can be added, deleted, and edited.


### Pages images
##### 1. Login page
![login](img/login.png)
##### 2. Home page
![home](img/home.png)
##### 3. Project list page
![project_list](img/project_list.png)
##### 4. Worker list page
![worker_list](img/worker_list.png)
##### 5. Position list page
![position_list](img/position_list.png)
##### 6. Task Type list page
![task_type_list](img/task_type_list.png)
##### 7. Account page
![account](img/account.png)
##### 8. Project detail page 
![project_detail](img/project_detail.png)
![project_detail](img/project_detail_1.png)
##### 9. Task detail page
![task_detail](img/task_detail.png)
##### 10. Project add page
![create_project](img/create_project.png)
##### 11. Task add page
![create_task](img/create_task.png)
##### 12. Worker add page
![create_worker](img/creater_worker.png)
##### 13. Position add page
![create_position](img/create_position.png)
##### 14. Task type add page
![create_task_type](img/create_task_type.png)
##### 15 Confirm delete Project page
![delete_project](img/delete_project.png)
##### 16. Confirm delete Worker page
![delete_worker](img/delete_worker.png)
##### 17. Confirm delete Task page
![delete_task](img/delete_task.png)
##### 18. Confirm delete Position page
![delete_position](img/delete_position.png)
##### 19. Confirm delete Task Type page
![delete_task_type](img/delete_task_type.png)
##### 20. Update Project page
![update_project](img/update_project.png)
##### 21. Update Task page page
![update_task_type](img/update_task_type.png)
##### 22. Update Position page
![update_position](img/update_position.png)
##### 23. Update Task page
![update_task](img/update_task.png)
##### 24. Update Worker page on worker list
![update_worker](img/update_worker.png)
##### 24. Account options
![account_options](img/account_settings.png)
##### 24. Account update
![account_update](img/account_update.png)