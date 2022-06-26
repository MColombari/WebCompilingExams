from flask import Flask, render_template
import os

# "docker build -t web_app ."
# "docker run -p 5000:5000 -v $(pwd):/app web_app"

app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template("user_login.html")


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)