FROM node:20.16.0-alpine AS builder

WORKDIR /workdir/frontend

COPY package.json package-lock.json ./

RUN npm install --frozen-lockfile

COPY . .

RUN npm run build

FROM node:20.16.0-alpine

ENV NODE_ENV=production

WORKDIR /workdir/frontend

COPY package.json package-lock.json ./

RUN npm install --frozen-lockfile --production

COPY --from=builder /workdir/frontend/.next ./.next
COPY --from=builder /workdir/frontend/public ./public
COPY --from=builder /workdir/frontend/next.config.mjs ./next.config.mjs

EXPOSE 3000

CMD ["npm", "run", "start"]
