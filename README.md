# 🏥 Smart Health Monitoring System

**Option B – Health Monitoring System**
**Student:** Joel Saravia – Universidad Anáhuac Mayab

---

# 🔗 Useful Links

* 📊 **Dashboard (Node-RED):** [https://nodered.savimind.com/ui](https://nodered.savimind.com/ui)
* 🔌 **REST + GraphQL API:** [https://industrialapi.savimind.com](https://industrialapi.savimind.com)
* 🧪 **Health Check:** [https://industrialapi.savimind.com/api/health](https://industrialapi.savimind.com/api/health)
* 🎥 **YouTube Demo Video:** [Watch Full Demo](ytlink)

---

# 📹 Demo Overview

The video demonstrates the full end-to-end system:

* Node-RED → REST API → MongoDB Atlas → GraphQL → Dashboard
* Login + JWT authentication
* Real-time vital signs via GraphQL Subscriptions
* Alerts and threshold handling
* CSV export
* Cloud deployment (Azure + Railway + Atlas)
* Dashboard UX walkthrough

---

# ⚙️ Setup Instructions (Local Development)

Although the entire system is deployed in the cloud, the following steps reproduce the environment locally for grading and testing.

## 1️⃣ Install Dependencies

### Backend (FastAPI)

```bash
pip install -r requirements.txt
```

### Node-RED

```bash
npm install -g node-red
```

---

# ▶️ Running the System Locally

## 2️⃣ Run FastAPI

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Local API:
[http://localhost:8000](http://localhost:8000)

Swagger UI:
[http://localhost:8000/docs](http://localhost:8000/docs)

GraphQL Playground:
[http://localhost:8000/graphql](http://localhost:8000/graphql)

---

## 3️⃣ Run Node-RED

```bash
node-red
```

Dashboard (local):
[http://localhost:1880/ui](http://localhost:1880/ui)

Import flow JSON from:
`flows/health_monitoring.json`

Update URLs to local endpoints:

* REST → `http://localhost:8000`
* WebSocket → `ws://localhost:8000/graphql`

---

# 🔑 Default Credentials

These credentials are valid for both the cloud deployment and local testing:

```
username: franciscososa
password: franciscososa
```

Used for:

* Login on dashboard
* JWT authentication
* Accessing protected REST endpoints
* GraphQL queries/subscriptions

---

# 🧰 Technologies Used

### 🖥 Backend

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

### 📊 Dashboard

| Technology              | Purpose                                 |
| ----------------------- | --------------------------------------- |
| **Node-RED**            | Visual flow-based dashboard platform    |
| **Node-RED Dashboard**  | UI components: gauges, charts, controls |
| **Node-RED ui_chart**   | Built-in charting (not Chart.js)       |
| **WebSocket/GraphQL**   | Real-time streaming of vital signs      |
| **HTTP Request nodes**  | REST API integration and data fetching  |

### ☁️ Cloud & Deployment

| Platform              | Role                                              |
| --------------------- | ------------------------------------------------- |
| **Azure App Service** | Production hosting for FastAPI + GraphQL          |
| **Railway.app**       | Hosting for Node-RED (Docker container)          |
| **MongoDB Atlas M0**  | Free-tier cloud database (512MB storage)         |
| **GitHub Actions**    | CI/CD pipeline for automated Azure deployment    |
| **Custom Domains**    | industrialapi.savimind.com / nodered.savimind.com |

---

# 🧪 Testing (Manual)

### Health Endpoint

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
├── config/               # Settings, constants, env config
├── domain/               # Core logic, models, and services
├── infrastructure/       # Database connections (MongoDB)
├── flows/                # Node-RED flows (JSON)
├── screenshots/          # Demo screenshots for documentation
├── main.py               # FastAPI entry point
├── architecture.md       # Cloud mapping + schema (separate document)
├── README.md             # Setup + instructions (this file)
└── requirements.txt
```

# 📧 Contact

**Joel Saravia**
Email: [joel.saravia@anahuac.mx](mailto:joel.saravia@anahuac.mx)
GitHub: [https://github.com/josaraviam](https://github.com/josaraviam)

---