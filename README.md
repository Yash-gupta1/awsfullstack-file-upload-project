# Aws-mini-projects
File upload gallery hosted on AWS EC2 with S3 storage 

### ☁️ AWS Services Used

| Service | Purpose |
|---|---|
| EC2 | Hosts the website and Flask backend |
| S3 | Stores all uploaded files permanently |
| IAM Role | Gives EC2 secure access to S3 |
| VPC | Private network for all resources |
| Public Subnet | Network segment where EC2 lives |
| Internet Gateway | Connects VPC to the internet |
| Route Table | Directs traffic to internet gateway |
| Security Group | Firewall — allows ports 80, 22, 443 |

## 🔄 Complete File Upload Workflow

### Step 1 — User Opens Website
```
User types http://YOUR-IP in browser
Request travels through internet
Hits Internet Gateway (door to AWS)
Route Table directs to Public Subnet
Security Group checks port 80 ✅
EC2 receives the request
Apache (port 80) receives it first
Apache forwards to Flask (port 5000)
Flask sends back the HTML page
User sees the website ✅
```

### Step 2 — User Selects and Uploads File
```
User clicks "Choose File"
Selects a file from their computer
Clicks "Upload" button
JavaScript packages the file
JavaScript sends to Flask /upload route
```

### Step 3 — Flask Receives the File
```
Flask /upload route receives the file
file = request.files["file"]
Flask has the file in memory now
Ready to send to S3
```

### Step 4 — boto3 Uploads to S3
```
Flask calls boto3
boto3 checks IAM Role attached to EC2
IAM Role has AmazonS3FullAccess ✅
boto3 connects to S3 in eu-north-1
s3.upload_fileobj(file, BUCKET, filename)
File gets uploaded to S3 bucket ✅
```

### Step 5 — Success Response
```
S3 confirms upload successful
Flask sends success message to browser
JavaScript shows "File uploaded!" ✅
```

### Step 6 — Gallery Shows Files
```
JavaScript calls Flask /files route
Flask asks S3 for list of all files
S3 returns list of filenames
Flask generates presigned URL for each file
  (temporary secure link — valid 1 hour)
Flask sends URLs back to browser
Browser creates <img> tags with URLs
Files appear in gallery ✅
```

---

## 🔐 Security

| Feature | How |
|---|---|
| No hardcoded AWS keys | IAM Role attached to EC2 |
| Files are private | S3 bucket not public |
| Secure file access | Presigned URLs (expire in 1 hour) |
| Port control | Security Group only opens 80, 22, 443 |
| Hidden Flask | Apache reverse proxy hides port 5000 |

---

## ⚙️ How Apache and Flask Work Together
```
User visits port 80 (Apache)
         ↓
Apache ProxyPass → forwards to port 5000 (Flask)
         ↓
Flask processes the request
         ↓
Flask sends response back to Apache
         ↓
Apache sends response back to user

User never knows Flask exists!
Flask is safely hidden from outside world
```

---

## 🚀 Setup Steps

### 1. EC2 Setup
- Launch Ubuntu EC2 instance (t3.micro)
- Attach IAM Role with S3 access
- Configure Security Group (ports 80, 22, 443)

### 2. Network Setup
- Create VPC with public subnet
- Attach Internet Gateway
- Add 0.0.0.0/0 route in Route Table

### 3. Install Dependencies
```bash
sudo apt update && sudo apt install python3-pip apache2 -y
pip3 install flask boto3 --break-system-packages
sudo a2enmod proxy proxy_http
```

### 4. Configure Apache
```bash
sudo bash -c 'cat > /etc/apache2/sites-available/000-default.conf << EOF
<VirtualHost *:80>
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
</VirtualHost>
EOF'
sudo systemctl restart apache2
```

### 5. Run Flask App
```bash
cd /home/ubuntu/gallery && python3 app.py &
```

---

## 🧠 Key Concepts Learned

- EC2 instance setup and configuration
- S3 bucket creation and file storage
- IAM Role for secure service communication
- VPC networking — subnets, route tables, IGW
- Apache reverse proxy configuration
- Flask backend development
- boto3 AWS Python SDK
- Presigned URLs for secure file sharing
- Git and GitHub for version control

---

## 🤖 Note
Flask backend code was developed with Claude AI assistance.
AWS infrastructure was configured manually as part of learning.

---

*Part of my AWS learning journey 🚀*
