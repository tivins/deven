# Deven

Dockerized development environment for PHP, MariaDB, Node, Typescript, Python.

## Configure

* Copy `.env.sample` to `.env` and edit values to match your environment.
* Copy `docker/web/apache/sites.conf.sample` to `docker/web/apache/sites.conf` and add virtual hosts.

```shell
cp .env.sample .env
cp docker/web/apache/sites.conf.sample docker/web/apache/sites.conf
```


### `.env` example

```dotenv
APP_ROOT=/data/projects/web/
HTTP_PORT=80
MARIADB_PORT=3306
ADMINER_PORT=8080
```

### `sites.conf` example
This file configures the Apache virtual hosts.
```apacheconf
# Use Site [hostname] [path inside container]
Use Site my-project.local /sites/my-project/public/
Use Site my-other-app.local /sites/my-app/src/
```


> [!IMPORTANT]
> When you modify `sites.conf`, you must restart Deven:
> ```shell
> deven restart
> ```

## CLI

**Installation**

By default, you need to `cd /path/to/deven`, and run `./deven`.

To make the `deven` command available everywhere, create a symbolic link: 

```shell
cd /usr/local/bin
sudo ln -s /path/to/deven deven
```

### Available commands

```shell
deven start     # Start containers (build if required)
deven restart   # Restart containers 
deven bash      # Open a bash shell inside the web container
deven bash [container] # Open a bash shell inside the [container] container. Ex: `deven bash db`.
deven cd        # Display the Deven folder path. Use with: cd $(deven cd)
deven list      # Display the list of configured sites
deven edit      # Edit the configuration file with vim
deven dump      # Create SQL dumps of all databases. Uses the BACKUP_DIR variable from .env.
```

> [!TIP]
> You can quickly move to Deven’s directory with:
> ```shell
> cd $(deven cd)
> ```

## Containers

* **web**: based on php:8.4-apache
* **db**: based on mariadb
* **adminer**: adminer image

## To do

* [x] Dump databases script
* [ ] Direct composer access