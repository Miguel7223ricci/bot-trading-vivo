
🧠 INSTRUCCIONES PARA REENTRENAR EL MODELO COMPATIBLE CON RENDER

1. Abre una terminal y navega a la carpeta donde tienes tu bot (BOT 2).
2. Crea un nuevo entorno virtual (opcional pero recomendado):

   python -m venv venv
   venv\Scripts\activate   (en Windows)
   source venv/bin/activate (en Linux/Mac)

3. Instala las versiones compatibles:

   pip install -r requirements_compatibles.txt

4. Ejecuta el script de entrenamiento:

   python entrenar_modelo_pro.py

5. Verifica que se generó el archivo:

   modelo_trained_rf_pro.pkl

6. Sube el archivo al repositorio:

   git add modelo_trained_rf_pro.pkl
   git commit -m "Modelo reentrenado con versiones compatibles con Render"
   git push

🔁 Render hará el despliegue automáticamente y cargará el modelo correctamente.
