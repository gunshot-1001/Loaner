# Step 1: Build React app
FROM node:18 AS build
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build production React app
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

# Copy React build to nginx html folder
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
