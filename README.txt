 Development Setup: [Ubuntu]

 - Install Node.js (14.x) [https://github.com/nodesource/distributions/blob/master/README.md]
    - `curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -`
    - `sudo apt-get install -y nodejs`

 - Install yarn (node package manager): https://linuxize.com/post/how-to-install-yarn-on-ubuntu-18-04/
    
 - Add npm dependencies (if not added): `sudo yarn add --save next react react-dom`
    - Note that all yarn commands must be run with sudo

