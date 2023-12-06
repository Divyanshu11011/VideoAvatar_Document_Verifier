from flask import Flask, render_template, request, jsonify
import mimetypes
import os
import re
from flask import Response

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'  # Adjust this to your actual upload folder

# Your existing routes...

# Add the following after_request handler
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

# Add the send_file_partial function
def send_file_partial(path):
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path)

    size = os.path.getsize(path)
    byte1, byte2 = 0, None

    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()

    if g[0]:
        byte1 = int(g[0])
    if g[1]:
        byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1

    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(
        data,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True
    )
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv

# Use send_file_partial in your video serving route
@app.route('/static/<filename>')
def serve_video(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file_partial(path)

# Your existing /process route...

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    action = data.get('action')

    if action == 'upload':
        # Call Python script for upload
        subprocess.run(['python', 'pan_read.py'])
        message = 'Upload Document action completed'
    elif action == 'point':
        # Call Python script for pointing to the camera
        subprocess.run(['python', 'aadhaar_read.py'])
        message = 'Point to Camera action completed'
    else:
        message = 'Invalid action'

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)