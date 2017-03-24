## A demo aiohttp server project
Well, this project is inspired by this [slide](http://igordavydenko.com/talks/lvivpy-4/#slide-1).  
Where I wrote this very simple demo project with aiohttp, I missed Flask and Django for every second. Still not finished yet!


#### deployment guiude
with gunicorn:
```
    gunicorn -b 0.0.0.0:8000 -k aiohttp.worker.GunicornWebWorker -w 9 -t 60 todo.app:app
```
