#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! dpkg -s nginx >/dev/null 2>&1; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories
web_static_dir="/data/web_static"
test_dir="$web_static_dir/releases/test"
shared_dir="$web_static_dir/shared"
current_dir="$web_static_dir/current"

mkdir -p "$test_dir" "$shared_dir"

# Create fake HTML file
echo "<html>
  <head></head>
  <body>Holberton School</body>
</html>" > "$test_dir/index.html"

# Create symbolic link
if [ -L "$current_dir" ]; then
    rm -f "$current_dir"
fi
ln -s "$test_dir" "$current_dir"

# Give ownership of /data/ folder to ubuntu user and group
chown -R ubuntu:ubuntu "$web_static_dir"

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
nginx_config="location /hbnb_static {
    alias $current_dir/;
}"

# Check if nginx_config already exists in the config file
if ! grep -qF "$nginx_config" "$config_file"; then
    sed -i "/^\s*server_name _;/a $nginx_config" "$config_file"
fi

# Restart Nginx
service nginx restart

exit 0
