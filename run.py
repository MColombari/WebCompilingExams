# This file has been used to test the application,
# the following are useful command to compile and run the docker.

# "docker build -t web_app ."
# "docker run -p 5000:5000 -v $(pwd):/app web_app"

from webcompilingexams import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
