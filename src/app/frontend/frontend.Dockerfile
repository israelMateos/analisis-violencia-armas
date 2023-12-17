FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY src/app/frontend/index.html .
COPY src/app/frontend/cargarGraficos.js .
COPY src/app/frontend/estilos/estilos.css ./estilos/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]