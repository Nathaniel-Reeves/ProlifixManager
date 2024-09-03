# base image
FROM node:18.16-alpine as builder

# Set working directory
WORKDIR /client_build

# Copy the package.json and install dependencies
COPY ./client/package*.json .

RUN npm install -g npm@9.6.7
RUN npm install --omit=dev --force
RUN npm install @vue/cli --force

# install and cache client dependencies
COPY ./client .

# build client
RUN npm run build


# Start nginx to serve Vue client
FROM nginx:stable-alpine as production-build

COPY ./client/nginx.conf /etc/nginx/nginx.conf

# Copy files from builder stage
COPY --from=builder /client_build/dist /var/www

EXPOSE 80
EXPOSE 81
EXPOSE 443
ENTRYPOINT ["nginx", "-g", "daemon off;"]