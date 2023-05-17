# base image
FROM node:12.2.0-alpine

# Set working directory
WORKDIR /app

# add `/client/node_modules/.bin` to $PATH
ENV PATH /app/client/node_modules/.bin:$PATH

# install and cache client dependencies
COPY client/package.json package.json
RUN npm install
RUN npm install @vue/cli

# start client
CMD ["npm", "run", "serve"]