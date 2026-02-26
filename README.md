# 📦 Cloud Storage App (AWS + Cognito + S3 + EC2)

## 🚀 Live Demo

🔗 [https://cloud-storage-app.duckdns.org](https://cloud-storage-app.duckdns.org)

---

## 📌 Project Overview

Cloud Storage App is a secure web application that allows authenticated users to upload, download, and delete files in their own private storage space using AWS services.

The application uses:

* 🔐 Amazon Cognito for authentication
* ☁ Amazon S3 for file storage
* 🖥 Amazon EC2 for hosting
* 🌐 Nginx as reverse proxy
* 🔒 Let’s Encrypt SSL (HTTPS)
* 🐍 Flask + Gunicorn backend

Each user has an isolated S3 folder based on their email ID.

---

## ✨ Features

* Secure login using Amazon Cognito (OAuth 2.0 Authorization Code Grant)
* Per-user isolated storage
* File upload
* File download (via pre-signed URLs)
* File delete
* HTTPS secured domain
* Reverse proxy configuration using Nginx
* Production-style deployment with Gunicorn

---

## 🏗 Architecture

```
User (Browser)
        ↓
DuckDNS Domain
        ↓
Nginx (Reverse Proxy + SSL)
        ↓
Gunicorn
        ↓
Flask Application
        ↓
Amazon Cognito (Authentication)
        ↓
Amazon S3 (Private Storage)
```

---

## 🛠 Tech Stack

| Layer          | Technology                     |
| -------------- | ------------------------------ |
| Frontend       | HTML, CSS                      |
| Backend        | Python (Flask)                 |
| Authentication | Amazon Cognito                 |
| Storage        | Amazon S3                      |
| Hosting        | Amazon EC2 (Amazon Linux 2023) |
| Reverse Proxy  | Nginx                          |
| WSGI Server    | Gunicorn                       |
| SSL            | Let’s Encrypt                  |
| DNS            | DuckDNS                        |

---

## 🔐 Authentication Flow

1. User clicks Login.
2. User is redirected to Amazon Cognito Hosted UI.
3. After successful login, Cognito redirects to `/callback`.
4. Flask verifies token and stores user session.
5. User can access their private S3 folder.

OAuth Flow Used:
Authorization Code Grant with OpenID Connect.

---

## 📂 Folder Structure

```
cloud-storage-app/
│
├── app.py
├── requirements.txt
├── .env (not committed)
├── README.md
└── nginx configuration
```

---

## ⚙ Environment Variables (.env)

```
AWS_REGION=eu-north-1
S3_BUCKET_NAME=your-bucket-name
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
USER_POOL_ID=your-user-pool-id
```

---

## ☁ Deployment Steps (High-Level)

1. Launch EC2 instance
2. Install Python, Nginx, Gunicorn
3. Configure S3 bucket
4. Configure Cognito User Pool
5. Set up DuckDNS domain
6. Install SSL using Certbot
7. Configure Nginx reverse proxy
8. Run Gunicorn
9. Access via HTTPS

---

## 🔒 Security Best Practices Implemented

* HTTPS enforced via SSL
* S3 private bucket
* Pre-signed URLs for secure downloads
* No public S3 access
* Environment variables used for secrets
* Session-based authentication
* IAM role recommended for EC2 access

---

## 📈 Future Improvements

* Drag & drop upload
* File preview support
* Folder creation
* Storage quota limit
* File sharing with expiry
* CI/CD pipeline
* Docker containerization

---

## 🎓 Internship Project Highlights

This project demonstrates:

* AWS Cloud architecture understanding
* OAuth 2.0 integration
* Reverse proxy configuration
* SSL certificate management
* Production deployment practices
* Secure file handling in cloud
* Real-world cloud engineering concepts

---

## 👩‍💻 Author

Divyadharshini P
B.Tech – Artificial Intelligence and Data Science
Cloud / DevOps Enthusiast
divyaprakash2836@gmail.com
https://linkedin.com/in/divya-dharshini-1728dd 

---


