# 🏥 Smart Health Monitoring System

**Option B – Health Monitoring System**
**Student:** Joel Antonio Saravia Monreal - Anahuac Mayab University - School of Engineering

---

# 🔗 Useful Links

* 📊 **Dashboard (Node-RED):** [https://nodered.savimind.com/ui](https://nodered.savimind.com/ui)
* 🔌 **REST + GraphQL API:** [https://industrialapi.savimind.com](https://industrialapi.savimind.com)
* 🧪 **Health Check:** [https://industrialapi.savimind.com/api/health](https://industrialapi.savimind.com/api/health)
* 🎥 **YouTube Demo Video:** [Watch Full Demo](https://youtu.be/rAdTeCjZlCo)

---

# 🚀 Pre-requisites and Setup

## System Requirements

- **Python:** 3.12+
- **Node.js:** 16+ (for Node-RED)
- **MongoDB Atlas Account** (free tier works)

---

## 📋 Initial Setup (Once)

### 1️⃣ Extract the Project

Extract the ZIP file to your desired location:
```bash
# Example location
C:\Projects\ordinary4threvolution\
```

Navigate to the folder:
```bash
cd ordinary4threvolution
```

### 2️⃣ Create Python Virtual Environment
```bash
python -m venv venv

# Activate virtual environment:
# Linux/Mac:
source venv/bin/activate

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
.\venv\Scripts\activate.bat
```

### 3️⃣ Install Dependencies (Python)
```bash
pip install -r requirements.txt
```

### 4️⃣ MongoDB Atlas Configuration

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or use a local DB.
2. Create a new cluster (M0 Free tier works fine)
3. Create a database user with read/write permissions
4. Whitelist your IP address (or use `0.0.0.0/0` for testing)
5. Get your connection string from Atlas (click **Connect → Drivers → MongoDB for VS Code**)

### 5️⃣ Environment Variables Setup

Create a `.env` file in the project root directory:
```bash
# .env
MONGODB_URL=mongodb+srv://<db_username>:<db_password>@clustername-cluster.r8pes.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=health_monitoring
JWT_SECRET_KEY=secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 
```

**⚠️ Important:** Replace `<username>`, `<password>`, and `<cluster>` with your actual MongoDB Atlas credentials.

**Example:**
```bash
MONGODB_URL=mongodb+srv://username:password@savimindai-cluster.r8pes.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=health_monitoring
JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 # Or wathever you feel like
```

### 6️⃣ Database Initialization

The system will automatically create the required collections on first run:
- `patients`
- `vitals`
- `alerts`
- `users`

### 7️⃣ Install Node-RED (If needed)
```bash
npm install -g node-red
```

---

## ▶️ Running the System Locally

### Start the Backend (FastAPI)
```bash
# Make sure the virtual environment is activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Available endpoints:**
- 🏠 API Root: [http://localhost:8000](http://localhost:8000)
- 📚 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- 🔍 GraphQL Playground: [http://localhost:8000/graphql](http://localhost:8000/graphql)

### Start Node-RED Dashboard

In a **new terminal window**:
```bash
node-red
```

**Configure Node-RED:**

1. Open Node-RED editor: [http://localhost:1880](http://localhost:1880)
2. Import the flow: **Menu (☰) → Import → Select file** → `flows/health_monitoring.json`
3. **Update endpoint URLs** in HTTP Request and WebSocket nodes:
   - REST API: `http://localhost:8000`
   - GraphQL WebSocket: `ws://localhost:8000/graphql`
4. Click **Deploy** (top right)
5. Access dashboard: [http://localhost:1880/ui](http://localhost:1880/ui)

---

# 🔑 Authentication Credentials

### For Local Development:
Use the credentials you created in step 6 (Database Initialization).

### For Cloud Demo (Using Deployed System):
```
username: franciscososa
password: franciscososa
```

**⚠️ Note:** The `franciscososa` user **only exists in the cloud deployment** at:
- API: [https://industrialapi.savimind.com](https://industrialapi.savimind.com)
- Dashboard: [https://nodered.savimind.com/ui](https://nodered.savimind.com/ui)

If you're running locally, you **must create your own user** using the `create_user.py` script.

---

## 🧪 Verify Installation

### 1. Check Backend Health:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Test Authentication:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"yourusername\",\"password\":\"yourpassword\"}"
```

You should receive a JWT token in the response.

### 3. Test GraphQL:
Visit [http://localhost:8000/graphql](http://localhost:8000/graphql) and run:
```graphql
query {
  patients {
    id
    name
    age
  }
}
```

---

## Troubleshooting

### "Connection refused" or "Database connection failed":
- Verify MongoDB connection string in `.env`
- Check if MongoDB Atlas IP whitelist includes your IP
- Ensure database user has read/write permissions

### "Module not found" errors:
- Ensure virtual environment is activated (and that you are using it to avoid conflicts)
- Run `pip install -r requirements.txt` again
- Try `pip install --upgrade pip` first

### Node-RED dashboard not showing:
- Install dashboard nodes: `npm install -g node-red-dashboard`
- Restart Node-RED after installing new nodes
- Check browser console (F12) for WebSocket errors

### Authentication failures:
- Verify user was created in MongoDB (check Atlas web interface)
- Check `JWT_SECRET_KEY` matches in `.env`
- Ensure you ran `create_user.py` successfully

### Port already in use (8000 or 1880):
```bash
# Windows - kill process on port 8000:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

---

# Technologies Used

### Backend

| Technology             | Purpose                                                        |
| ---------------------- | -------------------------------------------------------------- |
| **FastAPI**            | REST API for patients, vitals, alerts, reports, authentication |
| **Strawberry GraphQL** | Handles queries + real-time `liveVitals` subscription          |
| **MongoDB Atlas**      | Cloud NoSQL database for all system collections                |
| **Motor**              | Async MongoDB driver for FastAPI integration                   |
| **PyMongo**            | Sync MongoDB driver (backup for complex queries)              |
| **Pydantic**           | Data validation and settings management                        |
| **python-jose**        | JWT token creation and verification                            |
| **bcrypt + passlib**   | Secure password hashing and validation                        |
| **uvicorn**            | ASGI server for running FastAPI in production                 |
| **gunicorn**           | Process manager for production deployment                      |

### Dashboard

| Technology              | Purpose                                 |
| ----------------------- | --------------------------------------- |
| **Node-RED**            | Visual flow-based dashboard platform    |
| **Node-RED Dashboard**  | UI components: gauges, charts, controls |
| **Node-RED ui_chart**   | Built-in charting (not Chart.js)       |
| **WebSocket/GraphQL**   | Real-time streaming of vital signs      |
| **HTTP Request nodes**  | REST API integration and data fetching  |

### Cloud & Deployment

| Platform              | Role                                              |
| --------------------- | ------------------------------------------------- |
| **Azure App Service** | Production hosting for FastAPI + GraphQL          |
| **Railway.app**       | Hosting for Node-RED (Docker container)          |
| **MongoDB Atlas M0**  | Free-tier cloud database (512MB storage)         |
| **GitHub Actions**    | CI/CD pipeline for automated Azure deployment    |
| **Custom Domains**    | industrialapi.savimind.com / nodered.savimind.com |

---

# Testing (Manual)
### Cloud Endpoints

### Health Check
```bash
curl https://industrialapi.savimind.com/api/health
```

### Login
```bash
curl -X POST https://industrialapi.savimind.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"franciscososa","password":"franciscososa"}'
```

### Authorized Example (patients list)
```bash
curl https://industrialapi.savimind.com/api/patients \
  -H "Authorization: Bearer <token>"
```

### GraphQL Query
```graphql
query {
  patients {
    id
    name
    heartRate
  }
}
```

### GraphQL Subscription
```graphql
subscription {
  liveVitals {
    heartRate
    oxygenLevel
    timestamp
  }
}
```

---

# 📁 Project Structure
```
ORDINARY4THREVOLUTION/
├── api/                  # REST + GraphQL routers
├── config/               # Settings, constants, config
├── domain/               # Core logic, models, and services
├── infrastructure/       # Database (MongoDB)
├── flows/                # Node-RED flows (JSON)
│   └── health_monitoring.json
├── screenshots/          # Demo screenshots for documentation
├── create_user.py       # User creation script
├── main.py              # FastAPI entry point
├── architecture.md      # Cloud mapping + schema (separate document)
├── README.md            # Setup + instructions (this file)
├── requirements.txt     # Python dependencies
└── .env.example         # Example environment variables
```

---

# 📧 Contact

**Joel Saravia**
Email: [joel.saravia@anahuac.mx](mailto:joel.saravia@anahuac.mx)
GitHub: [https://github.com/josaraviam](https://github.com/josaraviam)

---