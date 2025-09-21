# Deven

🚀 **Dockerized development environment** for PHP, MariaDB, Node.js, TypeScript, and Python projects.

Deven provides a complete development stack with Apache, MariaDB, and Adminer, making it easy to set up and manage multiple web projects locally.

## ✨ Features

- **PHP 8.4** with Apache web server
- **MariaDB** database with Adminer interface
- **Multi-site support** with virtual hosts
- **CLI tool** for easy management
- **Database backup** functionality
- **Composer** pre-installed
- **ImageMagick** support

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tivins/deven
   cd deven
   ```

2. Make the `deven` command available system-wide:

    ```bash
    # Linux/macOS
    sudo ln -s /path/to/deven /usr/local/bin/deven
    
    # Or add to your PATH
    export PATH="/path/to/deven:$PATH"
    ```

3. **Configure environment:**
   ```bash
   cp .env.sample .env
   ```

4. **Configure virtual hosts:**
   ```bash
   cp docker/web/apache/sites.conf.sample docker/web/apache/sites.conf
   # Edit sites.conf to add your projects
   ```

5. **Start the environment:**
   ```bash
   deven build
   ```

## ⚙️ Configuration

### Environment Variables (.env)


```dotenv
# Project root directory (mounted to /sites in container)
APP_ROOT=/data/projects/web

# Database backup directory
BACKUP_DIR=/data/dumps

# Port mappings
HTTP_PORT=80
MARIADB_PORT=3306
ADMINER_PORT=8080

# Database credentials
DB_ROOT_PASSWORD=your_secure_password
```

### Virtual Hosts (sites.conf)

Configure your projects in `docker/web/apache/sites.conf`:

```apacheconf
# Use Site [hostname] [path inside container]
Use Site my-project.local /sites/my-project/public/
Use Site api.local /sites/my-api/src/
Use Site admin.local /sites/admin-panel/dist/
```

> [!TIP]
> Use the CLI to edit configuration: 
> `deven edit`

## 🛠️ CLI Commands


| Command | Description |
|---------|-------------|
| `deven build` | Build and start containers |
| `deven restart` | Restart all containers |
| `deven stop` | Stop all containers |
| `deven ps` | Show running containers |
| `deven bash` | Open bash shell in web container |
| `deven bash <container>` | Open bash in specific container (e.g., `deven bash db`) |
| `deven cd` | Display Deven directory path |
| `deven list` | List configured sites |
| `deven edit` | Edit sites.conf with vim |
| `deven dump [database]` | Create database backup(s) |

### Quick Navigation

```bash
# Move to Deven directory
cd $(deven cd)

# Quick access to project directory
cd $(deven cd)/sites
```

## 🐳 Containers

| Container | Image | Purpose |
|-----------|-------|---------|
| **web** | `php:8.4-apache` | Web server with PHP, Apache, Composer |
| **db** | `mariadb:latest` | MariaDB database server |
| **adminer** | `adminer:latest` | Database administration interface |

## 🔧 Usage Examples

1. Setting up a new PHP project

2. Add your project to `sites.conf`:
   ```apacheconf
   Use Site myapp.local /sites/myapp/public/
   ```

2. Restart Deven:
   ```bash
   deven restart
   ```

3. Access your project at `http://myapp.local`

### Database management
* Access database via Adminer
  Open http://localhost:8080 in your browser (NB: 8080 is defined in .env)

* Create database backup
    ```bash
    deven dump my_database
    ```

### Working with Composer

```bash
deven bash # Access web container
cd /sites/your_project
composer install # Install dependencies
```

## 🚨 Important Notes

- **Restart required**: After modifying `sites.conf`, run `deven restart`
- **Port conflicts**: Ensure ports 80, 3306, and 8080 are available
- **File permissions**: The web container runs as your user (UID 1000)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.