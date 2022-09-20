![Group 1](https://user-images.githubusercontent.com/33139843/190897807-dba2bc8a-6984-4595-87cd-9cd86d336006.jpg)


<h1 align="center">
  <br />
  Noteation
</h1>

<p align="center">
 Noteation allows musicians to effortlessly turn pages with facial gestures and annotate virtual sheet music. 
</p>

<p align="center">
 Built for Hack the North 2022 and finished as finalists!
</p>

# Technologies: 
- [AdHawk's MindLink](https://sites.google.com/adhawkmicrosystems.com/hack-the-north-help-center/hardware) 
- [TypeScript](https://www.typescriptlang.org/) ([React](https://reactjs.org/))
- [Python](https://www.python.org/) ([Flask](https://flask.palletsprojects.com/en/2.2.x/))
- [CockroachDB](https://www.cockroachlabs.com/)

# Setup

Both the frontend and backend are implemented in this repository in the ``frontend`` and ``backend`` directories respectively, and can be set up independently as outlined below

## Frontend

To install the dependencies, run: 

```sh
$ cd frontend
$ yarn install
```

To run the application, run: 
```sh
$ yarn start
```

Then head to http://localhost:3000 on a browser to see the frontend! 

![image](https://user-images.githubusercontent.com/33139843/190898131-d1b78b2c-0623-490d-8146-6a70f017e886.png)
![image](https://user-images.githubusercontent.com/33139843/190898212-8f785c02-1b75-49ca-8078-90682cf662df.png)

 
## Backend

To create a virtual environment and install dependencies, run:
```sh
$ python3 -m venv venv
$ source venv/bin/activate # Unix-like systems
$ source venv/Scripts/activate # Windows
$ pip install -r requirements.txt
```

Once you have tehse dependencies set up, you can  run the backend. To run the flask application that interfaces with our CockroachDB database:

```sh
$ python -m flask run
```

The part of our project that actually interfaces with the AdHawk SDK is in `backend/src/main.py`. To run, you must first install the AdHawk vision SDK, which is outside the scope of this readme but see [here](https://www.adhawkmicrosystems.com/api_doc) for documentation. Once that is running, simply call 

```sh
$ python ./main.py
```
And events will start being streamed to the CockroachDB database. 

# Contributors
Built by [Xander Naumenko](https://www.linkedin.com/in/xander-naumenko/), [Renu Rajamagesh](https://www.linkedin.com/in/renu-rajamagesh/), and [Prayus Shrestha](https://www.linkedin.com/in/prayus-shrestha/). 


# Credits
Credits to <a href="https://www.vecteezy.com/free-vector/website">Website Vectors by Vecteezy</a> for the logos, [AdHawk](https://www.adhawkmicrosystems.com) for the awesome glasses, and the entire Hack the North team for putting together an amazing event. 



