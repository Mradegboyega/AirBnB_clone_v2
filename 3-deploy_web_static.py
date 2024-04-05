#!/usr/bin/env python3
"""
Fabric script to create and distribute an archive to web servers
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import exists

# Define web servers
env.hosts = ['34.203.33.59', '34.396.82.54']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder

    Returns:
        Archive path if successfully generated, None otherwise
    """
    try:
        # Create versions directory if it doesn't exist
        local("mkdir -p versions")

        # Create archive name based on current time
        time_format = "%Y%m%d%H%M%S"
        current_time = datetime.now().strftime(time_format)
        archive_name = "web_static_{}.tgz".format(current_time)

        # Compress web_static folder into archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        archive_path = "versions/{}".format(archive_name)
        return archive_path
    except Exception as e:
        return None


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

        # Extract archive to /data/web_static/releases/<archive filename>
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


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    result = deploy()
    if result:
        print("Deployment successful.")
    else:
        print("Deployment failed.")
