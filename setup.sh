#!/bin/bash

# Streamlit Cloud setup script
# This runs automatically when deploying to Streamlit Cloud

# Create necessary directories
mkdir -p ~/.streamlit/

# Configure Streamlit
echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
" > ~/.streamlit/config.toml
