# ──────────────────────────────────────────────────────────────
# Stage 1: Build — Node 20 + Vite
# ──────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (layer caching)
COPY package.json package-lock.json ./
RUN npm ci

# Copy all source
COPY . .

# Build the React/Vite app
RUN npm run build

# ──────────────────────────────────────────────────────────────
# Stage 2: Serve — Nginx (lightweight static server)
# ──────────────────────────────────────────────────────────────
FROM nginx:alpine

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy Vite build output to Nginx webroot
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx config for React SPA (handles client-side routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
