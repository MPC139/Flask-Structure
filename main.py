import os
from app import create_app

app = create_app('default') 

if __name__=='__main__':
    print(os.environ.get('SECRET_KEY'))
    app.run(port= 8000)