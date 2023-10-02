# API for resolve powerplant-coding-challenge 

This API-REST is based on Tornado (https://www.tornadoweb.org/) and try to resolve the powerplant-coding-challenge published at https://github.com/gem-spaas/powerplant-coding-challenge
It is build with Python 3.9

## Installation as Docker
After uncompress you will find next content:
* app: folder including all the code 
* Dockerfile: file with commands to build do Docker image 
* requeriments.txt: file with python package required versions
* README.md: this file :-)

To execute next commands, you have to be inside folder containing 'app, Dockerfile, requiremenst,txt and README.md'.

To build the docker image execute next command:
- `docker build -t jigo/api-powerplant-coding-challenge:1.0 .`

By default, api is published at port 8888. So, to run the container, if you want to publish api at port 9999 (for example), you have to execute:
- `docker run --name jigo-api-powerplant-coding-challenge -p 9999:8888 -d jigo/api-powerplant-coding-challenge:1.0`

After that api will be available at http://X.X.X.X:9999/productionplan

## Responses
The API-REST performs some basic checks on the received BODY. If the format of the BODY is correct and the data is consistent, the api returns 2 types of response depending on whether the request is resolvable (the desired power can be reached) or not.
If the request is resolvable the API returns an api like the following:
```{
    "resolution": "success",
    "result": [
        {
            "name": "gasfiredbig1",
            "p": 460.0
        },
        {
            "name": "gasfiredbig2",
            "p": 445.7
        },
        {
            "name": "gasfiredsomewhatsmaller",
            "p": 0.0
        },
        {
            "name": "tj1",
            "p": 0.0
        },
        {
            "name": "windpark1",
            "p": 0.0
        },
        {
            "name": "windpark2",
            "p": 0.0
        }
    ]
}
```

If request is not resolvable, the answer will include max load available:
```
{
    "resolution": "not possible",
    "max load possible": 570.1
}
```

## Parameters
At `app/config/config.cfg` you can find all parameters that can be modified:
```
[api]
port = 8888
main_processes = 1
version = 1.0
built = 28/09/2023

[log]
folder = '/var/log/api/'
days_for_rotate = 10
main_file = api.log

[worker]
workers = 4
```

## Log
By default, logs are stored at `var/log/api/api.log`
Inside folder you can find any exception as ERROR and every request received including method, path, status code returned and execution time in miliseconds.

Examples:
```
2023-09-29 08:35:10,382 INFO [POST] -- /productionplan 200 16.993999ms
2023-09-29 08:48:57,319 INFO [POST] -- /productionplan 200 9.422779ms
2023-09-29 08:48:58,561 INFO [POST] -- /productionplan 200 2.692699ms
2023-09-29 08:48:59,305 INFO [POST] -- /productionplan 200 4.079103ms
```

If raise any exception, log information include file affected, function affected, arguments received at function, line affected and error description.

Example:
```
2023-09-29 08:52:03,905 ERROR tmc.py -- function extract_data -- args () --kwargs {'json_body': {'load': 480, 'fuel': {'gas(euro/MWh)': 13.4, 'kerosine(euro/MWh)': 50.8, 'co2(euro/ton)': 20, 'wind(%)': 0}, 'powerplants': [{'name': 'gasfiredbig1', 'type': 'gasfired', 'efficiency': 0.53, 'pmin': 100, 'pmax': 460}, {'name': 'gasfiredbig2', 'type': 'gasfired', 'efficiency': 0.53, 'pmin': 100, 'pmax': 460}, {'name': 'gasfiredsomewhatsmaller', 'type': 'gasfired', 'efficiency': 0.37, 'pmin': 40, 'pmax': 210}, {'name': 'tj1', 'type': 'turbojet', 'efficiency': 0.3, 'pmin': 0, 'pmax': 16}, {'name': 'windpark1', 'type': 'windturbine', 'efficiency': 1, 'pmin': 0, 'pmax': 150}, {'name': 'windpark2', 'type': 'windturbine', 'efficiency': 1, 'pmin': 0, 'pmax': 36}]}} -- line 12: 'fuels'
```
