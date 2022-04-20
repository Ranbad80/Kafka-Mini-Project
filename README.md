# Airflow Mini-Project DAG Scheduling
 
 we use Docker to establish the airflow platform:
 
 we down load springboard_airflow folder which include (docker-compose.yml,docker file,mmnt(airflow file and cfg,...))
 
 Copy my .py file (dag) to mnt/airflow/dags directory
 
 Then execute ./start.sh script. This should build and start all the services.
 
![dag](https://user-images.githubusercontent.com/83798130/164130704-01f30fde-7009-400a-9b4f-f924513835c9.jpeg)

Execute docker-compose ps and you should see below


![dag2](https://user-images.githubusercontent.com/83798130/164130964-c9123667-dbec-4b98-b03e-a7be3d284474.jpeg)

go to localhost:8080 - we will be presented with the web UI

![q](https://user-images.githubusercontent.com/83798130/164131355-9a89c804-546f-48f7-87c8-6811c7430b1f.jpeg)

we can trigger our dag in dag.py![dag1](https://user-images.githubusercontent.com/83798130/164131545-246f3a32-262d-4cd9-b85b-bc74f2c010ac.jpeg)

After completing you can use ./stop.sh to stop the services
./reset.sh to completely wipe out all the images 
