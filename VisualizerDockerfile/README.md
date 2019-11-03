# Building the visualizer docker

To build your Docker you'll just have to do the following:

```
cp -R ../html/ .
sudo docker build -t visualizer .
```

And now, you'll have prepared your visualizer. Note that you'll have to copy the files you want to visualize into the Docker!

If you want to run the docker:

```
sudo docker run -d --rm --name=cityvisualizer visualizer
```

Look for the IP so you can enter into the site:

```
docker inspect cityvisualizer
```

And look for the field IPAddress. Once you've found it go into your browser and write that IP.

If you want to commit changes to the docker image:

```
sudo docker exec -it cityvisualizer bash
```

And then, once you've made the changes use the docker commit command. 
