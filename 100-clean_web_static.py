#!/usr/bin/env python3
"""
Fabric script to delete out-of-date archives
"""

from fabric.api import env, run, local
from datetime import datetime
from os.path import exists

# Define web servers
env.hosts = ['34.203.33.59', '18.233.67.31']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_clean(number=0):
    """
    Deletes out-of-date archives

    Args:
        number: Number of archives to keep (including the most recent)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Clean local archives
        local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

        # Clean remote archives
        run("ls -t /data/web_static/releases | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(number + 1))
        
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    result = do_clean(number=2)  # Example: Keep the two most recent versions
    if result:
        print("Cleanup successful.")
    else:
        print("Cleanup failed.")
