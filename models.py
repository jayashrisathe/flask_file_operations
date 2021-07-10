from flask import Flask, render_template
from flask import request
import chardet
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = Flask(__name__)


def get_encoding(file):
    """
    description - Used to get encoding of given file
    params - file name
    returns - returns encoding type of file
    """
    with open(file, 'rb') as f:
        txt_code = chardet.detect(f.read())['encoding']
        if txt_code == 'ascii':
            return 'utf-8'
        return txt_code


@app.route("/<filename>/",  methods=['GET'])
def render_file_data(filename="file1.txt"):
    """
    description - Render the data according to URL inputs by user.
    params - file name
    returns - file data template with requested data
    """
    txt_code = get_encoding(filename)
    with open(filename, 'r', encoding=txt_code) as f:
        file_data = f.readlines()
        from_line = int(request.args.get("from_line", 0))
        to_line = int(request.args.get("to_line", len(file_data) - 1))
        logging.debug(f"\n\nReading data from file:{filename}, start line: {from_line}, end line: {to_line}\n\n")
        data_to_render = "".join(file_data[from_line:to_line+1])
        return render_template('file_data_template.html', text=data_to_render)


@app.route("/")
def index():
    """
    description - Used to set the default route
    """
    return "Well come in file data reader"


@app.errorhandler(Exception)
def all_exception_handler(error):
    """
        description - Used to handle all exceptions
        @returns - correct URL format
        """
    return f"Error: {error.code}, " \
           f"Please recheck URL, format should be: /filename/?from_line='from_line_no'?to_line='to_line_no'", 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)