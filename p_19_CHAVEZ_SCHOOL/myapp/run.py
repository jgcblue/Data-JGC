from app import create_app, db
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db}
# Add more sobjects later. This being here is like a seed for doing others. 

if __name__ == '__main__':
    app.run(debug=True)

