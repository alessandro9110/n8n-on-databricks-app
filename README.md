# n8n-on-databricks-app

Databricks App for deploying n8n Community Edition with enterprise-grade features and scalability in the Databricks environment.

## 🚀 Databricks Deployment

### Prerequisites
- Access to a Databricks workspace
- Permissions to create and deploy custom apps
- Node.js runtime available in the Databricks environment

### Installation

#### 1. Upload Source Code
Copy the entire contents of this repository to a folder in your Databricks workspace:

```bash
# Option 1: Direct clone in workspace
git clone <repository-url> /Workspace/Users/<your-username>/n8n-databricks-app

# Option 2: Manual upload via Databricks UI
# - Download repository as ZIP
# - Import files into workspace through web interface
```

#### 2. Create a Custom Databricks App
1. Go to **Compute** > **Apps** menu
2. Click **"Create app"**
3. Select **"Custom app"**
4.  Assign a name to your app (e.g., "n8n-workflow-automation")

#### 3. Configure Deployment
1. In the **"Deploy"** section of the created app
2.  Modify the **"Source code"** field
3. Point to the project's `app/` folder:
   ```
   /Workspace/Users/<your-username>/n8n-databricks-app/app/
   ```

#### 4. Deploy the App
1. Click **"Deploy"** to start the process
2.  Databricks will automatically install Node.js dependencies
3. The app will be available on port 5678

## 📋 Project Structure

```
n8n-databricks-app/
├── app/                    # Main application folder
│   ├── app.py             # App entry point (if present)
│   ├── app.yaml           # Databricks App configuration
│   ├── package.json       # Node.js dependencies
│   └── src/               # n8n source code
├── README.md              # This file
└── .gitignore
```

## ⚙️ Configuration

### Environment Variables
Configure the following variables through the Databricks interface or in the `app.yaml` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_PORT` | Listening port | `5678` |
| `N8N_BASIC_AUTH_ACTIVE` | Enable basic authentication | `true` |
| `N8N_BASIC_AUTH_USER` | Access username | `admin` |
| `N8N_BASIC_AUTH_PASSWORD` | Password (change it!) | `changeme` |
| `N8N_ENCRYPTION_KEY` | Encryption key | `auto-generated` |
| `DB_TYPE` | Database type | `sqlite` |
| `GENERIC_TIMEZONE` | Workflow timezone | `UTC` |

### Security
- **Always change** the default password
- Use **Databricks Secret Manager** for sensitive credentials
- Keep `N8N_ENCRYPTION_KEY` stable to preserve encrypted data

## 🔧 Management and Monitoring

### App Access
After deployment, the app will be available through:
- **Internal URL**: Provided by the Databricks Apps interface
- **Port**: 5678 (configurable)

### Logs and Debugging
- View logs through the app's "Logs" section in Databricks
- Monitor app status from the Apps panel

### Updates
1. Update the code in the Databricks workspace
2. Go to the app's "Deploy" section
3. Click "Redeploy" to apply changes

## 📚 Additional Resources

- [Databricks Apps Documentation](https://docs.databricks.com/en/dev-tools/databricks-apps/)
- [n8n Documentation](https://docs.n8n.io/)
- [Deployment Best Practices](https://apps-cookbook.dev/docs/deploy/)

## 🆘 Troubleshooting

### Common Issues
- **App won't start**: Verify Node.js is available in the environment
- **Dependency errors**: Check `package.json` file and Node.js versions
- **Authentication problems**: Verify auth environment variables

### Support
For specific issues, check the app logs in the Databricks Apps panel. 

---

> **Note**: This is an enterprise solution for integrating n8n into the Databricks ecosystem. For local use or development, refer to the documentation in the `n8n-app/` folder. 
