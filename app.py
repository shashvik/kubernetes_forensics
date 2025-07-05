from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>CommandRunner.com — Search Anything (Literally)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
        }
        header {
            background: #2c3e50;
            color: white;
            width: 100%;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        main {
            margin-top: 60px;
            text-align: center;
        }
        h2 {
            color: #333;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            width: 400px;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 25px;
            border: 1px solid #ccc;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            outline: none;
        }
        input[type="submit"] {
            padding: 12px 25px;
            font-size: 16px;
            border-radius: 25px;
            border: none;
            background-color: #3498db;
            color: white;
            margin-left: 10px;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input[type="submit"]:hover {
            background-color: #2980b9;
        }
        pre {
            background: #fff;
            padding: 20px;
            margin-top: 30px;
            width: 80%;
            max-width: 800px;
            border-radius: 10px;
            border: 1px solid #ddd;
            text-align: left;
            overflow-x: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        footer {
            margin-top: auto;
            padding: 20px;
            text-align: center;
            color: #888;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <header>🔍 CommandRunner.com</header>
    <main>
        <h2>Type Anything… We’ll Run It 🚀</h2>
        <form method="post">
            <input name="cmd" type="text" placeholder="Search or run a command... (e.g., ls -la)" />
            <input type="submit" value="Run">
        </form>
        {% if output %}
        <pre>{{ output }}</pre>
        {% endif %}
    </main>
    <footer>⚠️ For demo purposes only — anything you type is executed in the container.</footer>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        cmd = request.form.get('cmd')
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5, text=True)
        except Exception as e:
            output = str(e)
    return render_template_string(HTML, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
