import os
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default') 

@app.shell_context_processor
def make_shell_context():       
    return dict(db=db, User=User, Role=Role) 
#This decorator allow us execute our Flask App on shell context. Then we can do some test on Database or whatever we need to do but -
# it's necessary to add the variables that it will use 
# For example, in this case, I going to export db(database variable), User(class Model), Role(Class Model)
# We can run this shell context following this steps:
# 1- export FlASK_APP=main.py
# 2- export FLASK_ENV=development
# 3- flask shell
# Then you will see that variable db, User and Role were declared.



if __name__=='__main__':
    print(os.environ.get('SECRET_KEY'))
    app.run(port= 9000)