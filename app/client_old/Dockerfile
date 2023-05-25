# base image
FROM node:12.2.0-alpine

# Set working directory
WORKDIR /client

# install and cache client dependencies
COPY ./client/*.js /client
COPY ./client/*.json /client
COPY ./client/public /client/public
COPY ./client/src /client/src
COPY ./client/tests /client/tests
COPY ./client/.editorconfig /client/.editorconfig

# add `/client/node_modules/.bin` to $PATH
ENV PATH /app/client/node_modules/.bin:$PATH

RUN npm install
RUN npm install @vue/cli

# start client
CMD ["npm", "run", "serve"]