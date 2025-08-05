# Use a lightweight web server image
FROM nginx:alpine

# Copy HTML templates to the default Nginx web directory
COPY templates/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80
