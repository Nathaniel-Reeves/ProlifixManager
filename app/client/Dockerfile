# base image
FROM node:12.2.0-alpine

# Set working directory
WORKDIR /app

# add `/client/node_modules/.bin` to $PATH
ENV PATH /app/client/node_modules/.bin:$PATH

# install and cache client dependencies
COPY client/package.json package.json
COPY client/tsconfig.json tsconfig.json
COPY client/vue.config.js vue.config.js
COPY client/cypress.json cypress.json
COPY client/babel.config.js bable.config.js
COPY client/.editorconfig .editorconfig
COPY client/public public
COPY client/src src
COPY client/public public
COPY client/tests tests
RUN npm install
RUN npm install @vue/cli

# start client
CMD ["npm", "run", "serve"]