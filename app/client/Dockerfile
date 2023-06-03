# base image
FROM node:18.16-alpine as build-stage

# Set working directory
WORKDIR /client

# install and cache client dependencies
COPY ./client/*.js .
COPY ./client/*.json .
COPY ./client/public ./public
COPY ./client/src ./src
COPY ./client/tests ./tests
COPY ./client/.editorconfig .

# add `/client/node_modules/.bin` to $PATH
# ENV PATH /app/client/node_modules/.bin:$PATH

RUN npm install -g npm@9.6.7
RUN npm install --omit=dev --force
RUN npm install @vue/cli --force

# build client
RUN npm run build

# Start nginx to serve Vue client
FROM nginx as production-stage
EXPOSE 8080
RUN mkdir /client
COPY ./client/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /client /client