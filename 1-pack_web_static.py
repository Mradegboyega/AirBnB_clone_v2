#!/usr/bin/env python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

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

        archive_path = os.path.join("versions", archive_name)
        return archive_path
    except Exception as e:
        return None

if __name__ == "__main__":
    result = do_pack()
    if result:
        print("Archive created:", result)
    else:
        print("Failed to create archive.")
