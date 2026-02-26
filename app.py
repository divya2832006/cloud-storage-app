import os
import boto3
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask import Flask, redirect, session, url_for, request
from authlib.integrations.flask_client import OAuth
from botocore.client import Config

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

# -----------------------------
# S3 CLIENT CONFIG
# -----------------------------
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "virtual"}
    )
)

# -----------------------------
# FLASK APP
# -----------------------------
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = "fixed_super_secret_key_123456"

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# -----------------------------
# COGNITO CONFIGURATION
# -----------------------------
CLIENT_ID = "72o5f3o7cfdu1i85echsc6nkch"
CLIENT_SECRET = "1l9m6fncl84o8pvfk5l4h17uqhsp7hh90rcbhg1nk5sv79t6tjo8"
REGION = "eu-north-1"
USER_POOL_ID = "eu-north-1_IDWVHuh3X"
DOMAIN_PREFIX = "eu-north-1idwvhuh3x"

COGNITO_DOMAIN = f"https://{DOMAIN_PREFIX}.auth.{REGION}.amazoncognito.com"
ISSUER = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"

oauth = OAuth(app)

oauth.register(
    name="cognito",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{ISSUER}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email"},
    token_endpoint_auth_method="client_secret_post"
)

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    if "user" not in session:
        return """
        <div style="display:flex;justify-content:center;align-items:center;height:100vh;background:linear-gradient(135deg,#667eea,#764ba2);color:white;">
            <div style="text-align:center;">
                <h1>Cloud Storage App</h1>
                <a href="/login" style="padding:10px 20px;background:white;color:#764ba2;border-radius:8px;text-decoration:none;font-weight:bold;">Login with Cognito</a>
            </div>
        </div>
        """

    user_folder = session["user"]

    files = s3.list_objects_v2(
        Bucket=S3_BUCKET,
        Prefix=f"{user_folder}/"
    )

    rows = ""

    for obj in files.get("Contents", []):
        file_name = obj["Key"].split("/", 1)[1]
        size_kb = round(obj["Size"] / 1024, 2)
        upload_time = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")

        rows += f"""
        <tr>
            <td><i class="bi bi-file-earmark"></i> {file_name}</td>
            <td>{size_kb} KB</td>
            <td>{upload_time}</td>
            <td>
                <a href='/download/{file_name}' class="btn btn-sm btn-success">Download</a>
                <a href='/delete/{file_name}' class="btn btn-sm btn-outline-danger">Delete</a>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Storage</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">

        <style>
            body {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                font-family: 'Segoe UI', sans-serif;
            }}

            .glass-card {{
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(12px);
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                padding: 30px;
                color: white;
            }}

            .table {{
                color: white;
            }}

            .table thead {{
                border-bottom: 2px solid rgba(255,255,255,0.4);
            }}

            .btn-success {{
                background-color: #00c853;
                border: none;
            }}

            .btn-success:hover {{
                background-color: #00b248;
            }}
        </style>
    </head>

    <body>

    <div class="container py-5">

        <div class="glass-card">

            <div class="d-flex justify-content-between align-items-center mb-4">
                <h3><i class="bi bi-cloud-fill"></i> Cloud Storage</h3>
                <a href='/logout' class="btn btn-light btn-sm">Logout</a>
            </div>

            <p><strong>User:</strong> {session['user']}</p>

            <form action="/upload" method="post" enctype="multipart/form-data" class="mb-4">
                <div class="input-group">
                    <input type="file" name="file" class="form-control" required>
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-upload"></i> Upload
                    </button>
                </div>
            </form>

            <div class="table-responsive">
                <table class="table table-borderless align-middle">
                    <thead>
                        <tr>
                            <th>File</th>
                            <th>Size</th>
                            <th>Uploaded</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows if rows else '<tr><td colspan="4">No files uploaded yet.</td></tr>'}
                    </tbody>
                </table>
            </div>

        </div>

    </div>

    </body>
    </html>
    """
# -----------------------------
# LOGIN ROUTE
# -----------------------------
@app.route("/login")
def login():
    return oauth.cognito.authorize_redirect(
        "https://cloud-storage-app.duckdns.org/callback"
    )

# -----------------------------
# CALLBACK ROUTE
# -----------------------------
@app.route("/callback")
def callback():
    token = oauth.cognito.authorize_access_token()
    user_info = token["userinfo"]
    session["user"] = user_info["email"]
    return redirect(url_for("home"))

# -----------------------------
# LOGOUT ROUTE
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    logout_url = (
        f"{COGNITO_DOMAIN}/logout"
        f"?client_id={CLIENT_ID}"
        f"&logout_uri=https://cloud-storage-app.duckdns.org"
    )
    return redirect(logout_url)

# -----------------------------
# UPLOAD ROUTE
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect("/")

    file = request.files["file"]
    filename = secure_filename(file.filename)

    user_folder = session["user"]
    s3_key = f"{user_folder}/{filename}"

    s3.upload_fileobj(file, S3_BUCKET, s3_key)

    return redirect("/")

# -----------------------------
# DOWNLOAD ROUTE
# -----------------------------
@app.route("/download/<path:filename>")
def download(filename):
    if "user" not in session:
        return redirect("/")

    user_folder = session["user"]
    s3_key = f"{user_folder}/{filename}"

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": s3_key
        },
        ExpiresIn=300
    )

    return redirect(url)

# -----------------------------
# DELETE ROUTE
# -----------------------------
@app.route("/delete/<path:filename>")
def delete(filename):
    if "user" not in session:
        return redirect("/")

    user_folder = session["user"]
    s3_key = f"{user_folder}/{filename}"

    s3.delete_object(
        Bucket=S3_BUCKET,
        Key=s3_key
    )

    return redirect("/")

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)