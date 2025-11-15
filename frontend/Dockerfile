# ---------- STAGE 1: build ----------
FROM node:20-alpine AS build

WORKDIR /app

# Копируем package.json/lock — для кеша npm install
COPY package*.json ./

# Устанавливаем зависимости (можно добавить --omit=dev если не нужны dev-зависиимости)
RUN npm install

# Копируем исходники
COPY . .

# Сборка Angular в прод-режиме
# Если проект не в корне, поправь имя проекта: ng build <project-name>
RUN npm run build -- --configuration production

# После этого статические файлы будут в /app/dist/<project-name>


# ---------- STAGE 2: nginx для отдачи статики ----------
FROM nginx:1.27-alpine

# Удалим дефолтный конфиг, если хотим свой
RUN rm /etc/nginx/conf.d/default.conf

# Свой простой конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist/max-app /usr/share/nginx/html

# COPY cert.pem /etc/nginx/certs/cert.pem
# COPY key.pem  /etc/nginx/certs/key.pem

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
