# Website Monitoring and Recovery
This is a python based website monitoring tool. If you have a web application running on a cloud server platfrom like Linode, you can monitor it using the python script defined in `monitor-wesite.py`. In case the application doesn't return a status code 200, the python script, restarts it by sshing into the server. It basically restarts the docker container. In case there is no response from the web-app or an unexpected error, the script reboots the remote server using the ``linode_api4`` module. Whenever the website is down, the script sends an email notification using the smtplib `module`. The script uses the `schedule` module to send requests to the server every 5 minutes to check whether it is running.

Note: For simplicity I have hardcoded the public-ip address of my server and the linode-id in the python script. It can also be passed via environment variables.

## How to use this project
1. Install the virtual env by executing `uv sync`
2. Run the script using `uv run monitor-website.py`