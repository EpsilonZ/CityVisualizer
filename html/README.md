# SET UP 

To set this up you will only need to copy this html/ directory to your /var/www/html directory! Please, be aware that you will need to install apache2 if you haven't yet:

```
sudo apt-get update //not needed but updating is always good:)
sudo apt-get install apache2
```

Now that we've installed apache2 we'll be able to copy all html contents to your html directory:

```
sudo cp -R html/ /var/www/html
```

Please note that installing apache2 is not a must but it's easier. If you have it installed already or don't want to install it you can do the following:

```
cd html/
python -m SimpleHTTPServer
```

And a server will be created at 8080 port (if you want another you can specify it)


## TROUBLESHOOTING

In js/config.js you will be able to modify parameters of require.js library. waitSeconds is required to not get a load timeout error.
If you want to improve you visualization speed (note that the improvement is based on your hard drive, if it's an SSD you won't see that much of a difference) do the following:
```
mkdir /tmp/cityvisualizer
sudo mount -t tmpfs -o size=1024m tmpfs /tmp/cityvisualizer
cp /var/www/html/Data/nameOfYourTraceunificado* /tmp/cityvisualizer/
```
sizevalue is determined by your traces size. For example if it's 1GB it would be 1024

__Now when loading your traces file go into the /tmp/cityvisualizer/ directory and choose it from there__
