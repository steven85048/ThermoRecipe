 Development Setup: [Ubuntu]

 - Install Node.js (14.x) [https://github.com/nodesource/distributions/blob/master/README.md]
    - `curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -`
    - `sudo apt-get install -y nodejs`

 - Install yarn (node package manager): https://linuxize.com/post/how-to-install-yarn-on-ubuntu-18-04/
    
 - Add npm dependencies (if not added): `sudo yarn add --save next react react-dom`
    - Note that all yarn commands must be run with sudo

- Docker setup through WSL: https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly
    - Note that you must expose the Docker Windows daemon running outside of WSL through the environment variable for the docker daemon to be visible
    - To test that docker is running: `docker info` or `docker ps`

Build Setup:

[ While docker daemon is running ]
- In the thermorecipe/app folder:
- `docker build -t <username>/<image-name>`
- Test that the image exists with the most recent version: `docker images`
- Run the docker image: `docker run -d -p 3333:3000 <username>/<image-name>:latest`
- Test the docker image running locally: `localhost:3333` ( image has port 3000 within the container, but is forwarded to globally accessible port 3333 )
- Shutdown the docker image `docker stop <container-id>`