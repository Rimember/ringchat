FROM node:20.16.0-alpine

WORKDIR /workdir/frontend

COPY package.json package-lock.json ./

RUN npm install --frozen-lockfile

COPY . .

RUN npm run build

RUN npm prune --production

EXPOSE 3000

CMD ["npm", "run", "start"]
