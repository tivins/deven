# Deven

Dockerized development environment

## Configure

Copy `.env.sample` to `.env` and edit values to match with your environment.

```
APP_ROOT=/data/projects/web/
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
```

also :

```shell
cd $(deven cd)
```

