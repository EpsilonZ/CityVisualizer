# Step to step execution

## REQUIREMENTS

To execute this you will need to have set up an OSRM server since this is the server we'll use to generate routes. It uses a really simple API so it'll be perfect for our use. Please head to:

Docker: https://github.com/Project-OSRM/osrm-backend/wiki/Docker-Recipes (__This is what I've built so if you go for it I can help you__) 
Non-docker: https://github.com/Project-OSRM/osrm-backend
AWS: You can use their cloudformation template from https://github.com/Project-OSRM/osrm-backend. Be aware that this requires an AWS account and it might exceed free tier usage.

You also will need the latest version of Chrome. __Other browsers have not been tested.__

# EXECUTING SCENARIO

To generate the city first you will have to give execution permissions:

```
chmod +x *.sh
```

Once you've done this you are set to start creating your city:

```
./generate_city.sh
```
__NOTE:__ This may take 20min+ (depending on your cpu, bandwith connection to your server) 

For illustration, this is what generate_city.sh will do automatically (watch out for step 2, this is the only step that needs your input):

1. Create scheduled routes. When creating scheduled routes you will see this image:

 ![Allt text](../media/generatingFirstStep.png)

2. Download translated GPS points to Canvas points from your localhost webpage you've set up. You will have to manually enter the http://localhost/GeneradorPruebas.html to manually start to execution. Once this is done you will be free to close the browser and keep the execution. Program will automatically copy the generated files to your current directory.

 ![Allt text](../media/generatingSecondStep2.1.png)

__NOTE: If you see that an error occured downloading just refresh the page and delete the temporary downloads from your Downloads folder__

3. Create smoother paths. Since doing this at browser is an issue, I wanted to execute this locally.

 ![Allt text](../media/generatingSecondStep2.2.png)

4. Execution to file. This will take some time so please be patient...

5. Generate heat map.

6. Unify heat map and execution file to boost performance on visualization and analytics.

7. Generate line sizes

8. Move the needed files to /var/www/html/Data for you to be available to visualize them at http://localhost/SimulacionFinal.html

If during the process you've had a RAM issue you can go to GSmootherPath/genera_intermedios.py and change this line:

```
                                puntosIntermedios = 10
```
__To a lower number. This will result in a less intermediate points so less smoothing is applied to the route.__
__You can always mount a temporary higher swap to execute this__

## Visualizing results

Once you have generated your city you can travel to http://localhost/SimulacionFinal.html to watch your simulation. Be aware that you'll have to select it through the interface on http://localhost/SimulacionFinal.html clicking on "Seleccionar archivo" and navigating to /var/www/html/Data directory. 

Also, if you want to analyze your traces, go to https://github.com/EpsilonZ/TrafficVisualizer and copy your generated file (no need to include sizes.txt) there to further analysis.


## TROUBLESHOOTING

ValueError: could not convert string to float: '\ufeff541' --> when generating schedules file a character is added to the beggining. To fix this just nano into the file and press 'Supr' and save it
