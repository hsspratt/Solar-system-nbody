# Welcome to Solar-system-nbody

Solar-system-nbody is a n body simulation written in python. There is a GUI which enables the user to add a limited number of configurations, howvever the core code can work for as many objects as needed, they just have to be initialised first. The code as it is computes the position data for the planets initialised and then procedes to analyse the data by plotting a number of graphs including the 2D orbit, KE, PE and Momentum of the system. The code uses scipy.integrate.solve_ivp which is a nifty integrator which automatically detects the time steps at which to compute the integration. However all important aspects of the integrator can be changed in the GUI such as the time step (max_steps) and the tolerances (r_tol & a_tol). The objective of Solar_system_nbody is to produce an accurate simulation of the solar system, ideally at quick speeds.

## How it works

Firstly, check that you have these Python libraries: TKinter, NumPy, Matplotlib. If you have not installed python, I recommend using the Anaconda installer with Visual Studio Code as an IDE. Although spyder is typically the main IDE, i find that compatability with spyder and tkinter on MacOSX unreliable at times. 

After downloading the code folder the program can be started by running **Simulation (GUI).py** in the main directory. This will launch the GUI from which you will be able to change a number of variables. The GUI will look like the image given below. 

![GUI](/images/logo.png)
<img width="1440" alt="Screenshot 2021-07-30 at 12 35 36" src="https://user-images.githubusercontent.com/42693405/127648456-35bf2221-8500-4fc5-a0f4-aa54e52c4e1b.png">






  
| N body system | Time Period | Number of Periods | Gravitational Constants | Iterations Per Period | ODE Solver |
| :-----------: | :------------: | :------------: | :-----------: | :------------: | :------------: |
| Solar System   |   31536000   |    100 | 6.6743015e-11 | 25 | RK45 |
| Figure of Eight  |    6.32591398    |      10 | 1 | 25 | RK45 |
| butterfly_I     |    6.2356    |      10 | 1 | 25 | RK45 |
| butterfly_II     |    7.0039    |      10 | 1 | 25 | RK45 |
| butterfly_III     |    13.8658    |      10 | 1 | 25 | RK45 |
| moth_I     |    14.8939    |      10 | 1 | 25 | RK45 |
| moth_II     |    28.6703    |      10 | 1 | 25 | RK45 |
| moth_III     |    25.8406    |      10 | 1 | 25 | RK45 |
| bumblebee    |    63.5345    |      10 | 1 | 25 | RK45 |

  

## Links

- [Repo](https://github.com/hsspratt/Solar-system-nbody "<N Body Simulation> Repo")


## Screenshots

![Home Page](/screenshots/1.png "Home Page")

![](/screenshots/2.png)

![](/screenshots/3.png)

## Available Commands

In the project directory, you can run:

### `npm start" : "react-scripts start"`,

The app is built using `create-react-app` so this command Runs the app in Development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser. You also need to run the server file as well to completely run the app. The page will reload if you make edits.
You will also see any lint errors in the console.

### `"npm run build": "react-scripts build"`,

Builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance. The build is minified and the filenames include the hashes. Your app will be ready to deploy!

### `"npm run test": "react-scripts test"`,

Launches the test runner in the interactive watch mode.

### `"npm run dev": "concurrently "nodemon server" "npm run start"`,

For running the server and app together I am using concurrently this helps a lot in the MERN application as it runs both the server (client and server) concurrently. So you can work on them both together.

### `"serve": "node server"`

For running the server file on you can use this command.

### `npm run serve`

## Built With

- JavaScript
- Node
- NPM
- Webpack
- HTML
- CSS

## Future Updates

- [ ] Reliable Storage

## Author

**Rohit Jain**

- [Profile](https://github.com/rohit19060 "Rohit jain")
- [Email](mailto:rohitjain19060@gmail.com?subject=Hi "Hi!")
- [Website](https://kingtechnologies.in "Welcome")

## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!
