FROM node:18 as build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install -g pm2

COPY . ./
RUN npm run build

#CMD ["pm2-runtime", "start", "./build/index.js", "--env", "production"]
