# Deven

Dockerized development environment

## Configure

Copy `.env.sample` to `.env` and edit values to match with your environment.

```
APP_ROOT=/data/projects/web/
HTTP_PORT=80
MARIADB_PORT=3306
ADMINER_PORT=8080
```

## Install 

By default, you have to `cd /path/to/deven`, then use `./deven`.

Create a symbolic link to enable the use of `deven` everywhere. 

```shell
cd /usr/local/bin
sudo ln -s /path/to/deven deven
```

### CLI commands

```shell
deven start     # start containers (build if required)
deven restart   # restart containers 
deven bash      # connect to web container
deven cd        # display the deven folder. Use `cd $(deven cd)`.
deven list      # display the list of configured sites.
deven edit      # vim configuration file
```

also :

```shell
cd $(deven cd)
```

