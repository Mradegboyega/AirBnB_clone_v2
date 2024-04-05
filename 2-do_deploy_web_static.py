#!/usr/bin/env python3
"""
Fabric script to distribute an archive to web servers and deploy it
"""

from fabric.api import env, put, run, sudo
from os.path import exists
from datetime import datetime

# Define web servers
env.hosts = ['34.203.33.59', '34.396.82.54']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it

    Args:
        archive_path: Path to the archive to deploy

    Returns:
        True if all operations have been done correctly, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory of web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive_filename>
        filename = archive_path.split('/')[-1]
        folder_name = filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, folder_name))

        # Delete archive from web server
        run('rm /tmp/{}'.format(filename))

        # Move extracted files to current deployment
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))

        # Delete symbolic link
        run('rm -rf /data/web_static/current')

        # Create new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    # Example usage:
    archive_path = "versions/web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    result = do_deploy(archive_path)
    if result:
        print("Deployment successful.")
    else:
        print("Deployment failed.")
