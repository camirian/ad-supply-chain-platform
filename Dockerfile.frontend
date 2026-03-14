FROM node:20-alpine AS builder

WORKDIR /app
COPY web/package*.json ./
RUN npm ci

COPY web/ ./

# .env.production is already in web/ — Vite reads it automatically during build
RUN npm run build

# Production runtime container
FROM node:20-alpine
WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./dist

# Cloud Run injects $PORT (usually 8080)
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "serve -s dist -l tcp://0.0.0.0:${PORT}"]
