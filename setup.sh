mkdir -p ~/.streamlit
echo "\
[server]\n\
headless = true\n\
enableCORS = true\n\
port = $PORT\n\
[theme]\n\
base=\"light\"\n\
primaryColor=\"#FF4B4B\"\n\
backgroundColor=\"#FFFFFF\"\n\
secondaryBackgroundColor=\"#F0F2F6\"\n\
textColor=\"#303030\"\n\n\
" > ~/.streamlit/config.toml