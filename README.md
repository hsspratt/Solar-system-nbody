# Welcome to Solar-system-nbody

Solar-system-nbody is a n body simulation written in python. There is a GUI which enables the user to add a limited number of configurations, howvever the core code can work for as many objects as needed, they just have to be initialised first. The code as it is computes the position data for the planets initialised and then procedes to analyse the data by plotting a number of graphs including the 2D orbit, KE, PE and Momentum of the system. The code uses scipy.integrate.solve_ivp which is a nifty integrator which automatically detects the time steps at which to compute the integration. However all important aspects of the integrator can be changed in the GUI such as the time step (max_steps) and the tolerances (r_tol & a_tol). The objective of Solar_system_nbody is to produce an accurate simulation of the solar system, ideally at quick speeds. In addition to the simulation there is also a plotting of the effective potential and the lagrange points which can be run.

## How it works

Firstly, check that you have these Python libraries: TKinter, NumPy, Matplotlib. If you have not installed python, I recommend using the Anaconda installer with Visual Studio Code as an IDE. Although spyder is typically the main IDE, i find that compatability with spyder and tkinter on MacOSX unreliable at times. 

After downloading the code folder the program can be started by running **Simulation (GUI).py** in the main directory. This will launch the GUI from which you will be able to change a number of variables. The GUI will look like the image given below. 

<img width="1440" alt="Screenshot 2021-08-03 at 01 04 24" src="https://user-images.githubusercontent.com/42693405/127939202-c0c0e964-7b76-4a69-87e1-fdcdcb287dfd.png">

1. Choose what planets / configuration you want to simulate. Either individual planets can be added **or** configurations otherwise the simulation will not operate as expected. The planets you cann add are ones that resuide in our solar system with the addition of pluto (no longer a planet) and an additional star. For the configurations these are mainly made up of know analytical soliutions the initial conditions of which are loisted below. 
2. The type of ODE integrator used can also be changed. Any questions about the differences can be found [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html). 
3. The final configurations you can make to this simulation in the GUI are constansts such a G, time period, number of time periods, atol, rtol and interations per time period. All these configurations will be passed through and applied to the script giving you quite a lot of contorl over the simulation. 

## Initial conditions which produce sensible orbits
  
| N body system | Time Period | Number of Periods | Gravitational Constants | Iterations Per Period | ODE Solver |
| :-----------: | :------------: | :------------: | :-----------: | :------------: | :------------: |
| Solar System   |   31536000   |    100 | 6.6743015e-11 | 25 | RK45 |
| Figure of Eight  |    6.32591398    |      0.5 | 1 | 25 | RK45 |
| butterfly_I     |    6.235641    |      1 | 1 | 25 | RK45 |
| butterfly_II     |    7.0039    |      1 | 1 | 25 | RK45 |
| butterfly_III     |    13.8658    |      10 | 1 | 25 | RK45 |
| moth_I     |    14.8939    |      1 | 1 | 25 | RK45 |
| moth_II     |    28.6703    |      1 | 1 | 25 | RK45 |
| moth_III     |    25.8406    |      1 | 1 | 25 | RK45 |
| bumblebee    |    63.5345    |      1 | 1 | 25 | RK45 |
| goggles    |    10.4668    |      1 | 1 | 25 | RK45 |
| dragonfly    |    21.2710    |      1 | 1 | 25 | RK45 |
| yarn    |    63.5345    |      1 | 1 | 25 | RK45 |
| yin_yang_I_a    |    4.2517    |      1 | 1 | 25 | RK45 |


## Links

- [Repo](https://github.com/hsspratt/Solar-system-nbody "<N Body Simulation> Repo")

## Built With

- Python

## Future Updates

- [ ] Improved GUI
- [ ] Plotting with Pygame for better visualisation
- [ ] Add more unique orbits
- [ ] Have plots which lines vary with velocity gradient

## Author

**Harry Spratt**

- [Profile](https://github.com/hsspratt "Rohit jain")
- [Email](mailto:ppyhss@nottingham.ac.uk?subject=Hi "Hi!")
- [Website](to add "Welcome")

## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!
