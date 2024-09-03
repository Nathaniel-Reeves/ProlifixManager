# base image
FROM node:18.16-alpine AS builder

# Set working directory
WORKDIR /client_build

# Copy the package.json and install dependencies
COPY ./client/package*.json .

# install and cache client dependencies
RUN npm install -g --omit=dev --force
RUN npm install @vue/cli --force
COPY ./client .

# build client
RUN npm run build


# Start nginx to serve Vue client
FROM nginx:stable-alpine AS production-build

COPY ./client/nginx.conf /etc/nginx/nginx.conf

# Copy files from builder stage
COPY --from=builder /client_build/dist /var/www
COPY --from=builder /client_build/dist /usr/share/nginx/html

EXPOSE 80
EXPOSE 81
EXPOSE 443
ENTRYPOINT ["nginx", "-g", "daemon off;"]