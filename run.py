<<<<<<< HEAD
#!venv/bin/python
=======
#!venv/bin/python3
>>>>>>> 3154d0c51705b23759b09e5f882c24a6f857f0ec
from app import app
import os

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '8080')))