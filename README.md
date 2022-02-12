# drone

This project uses both Node.JS and Python

You need to have Node.js & npm & Python & Python required libraries installed 
to run the code follow these steps:

1. run the command "npm install"
2. run the command "node app.js"
3. Follow the command prompt to get the port, and open the browser in the port. 
 http://localhost:<port>
4. Fill drone speed and height and click "submit"
5. click on the image, the position you click is the start position.
6. click the arrows buttons to simulate drone moving
7. When you want to stop click "Enter" button
7. the program will crop the frames the drone see and push it to the folder "public\images"
8. after saving the cropped images - the program will run the python code
9. The .csv output path is "public/csv/distances.csv"

- If you want to change image or parameters you can do it in the file "public/js/main.js"
- The project has unfinished code snippets to allow uploading image.