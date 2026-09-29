# Solar-system-nbody

An N-body gravitational simulation of the Solar System, written in Python. It also runs the famous periodic three-body "choreographies" (Figure-8, Butterfly, Moth, Yarn and others). A Tkinter GUI lets you choose the bodies, the ODE solver and the physical constants. The simulation integrates Newton's law of gravitation with `scipy.integrate.solve_ivp`, then:

- plots the orbits (2D and 3D);
- plots the kinetic, potential and total energy, and the linear and angular momentum, as conservation checks;
- reports how far the total energy drifted, which is a quick measure of how trustworthy the run is;
- optionally renders an animated video of the orbits.

The core code works for any number of bodies. Anything added to `init_objects.py` can be simulated. A separate script plots the effective potential and the Lagrange points of a two-body system.

<img width="1440" alt="The N-body simulation GUI" src="https://user-images.githubusercontent.com/42693405/127939202-c0c0e964-7b76-4a69-87e1-fdcdcb287dfd.png">

## Quick start

```bash
pip install -r requirements.txt        # numpy, scipy, matplotlib
python "Simulation (GUI).py"           # opens the GUI
```

For the video, install [FFmpeg](https://ffmpeg.org/) as well (`brew install ffmpeg`, `conda install ffmpeg` or `sudo apt install ffmpeg`). Without it, the animation is saved as a GIF instead of an MP4.

### Using the GUI

1. **Choose the bodies.** Either tick individual planets (at least two) **or** pick one ready-made configuration. Don't mix the two. The planets are the eight in our Solar System, plus an optional extra star (`External_Planet`).
2. **Choose the ODE solver.** See the [solve_ivp documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) for the differences between them.
3. **Set the constants:** G, the length of one time period, the number of periods, iterations per period, and the solver tolerances (`rtol`, `atol`).
4. Optionally tick **Render orbit animation**, then press **Run simulation**.

If nothing is selected, it simulates the Solar System over 100 years with RK45.

### Command line / headless

The same simulation runs without the GUI. That's useful on a server, or for scripting:

```bash
python "Simulation (GUI).py" --no-gui                                   # Solar System, 100 years
python "Simulation (GUI).py" --no-gui --config Figure_8 --animate       # Figure-8 plus an MP4
python "Simulation (GUI).py" --no-gui --config Butterfly_I --n-periods 3 --frames 600
python "Simulation (GUI).py" --help                                     # every option
```

Each `--config` fills in sensible defaults from the table below. Any flag you pass (`--G`, `--time-period`, `--n-periods`, `--iterations`, `--solver`, `--rtol`, `--atol`) overrides them. The plots and the video are written to `Plots Generated/`.

## How it works

The state of N bodies is one flat vector of 6N numbers: every position `[x1, y1, z1, x2, …]` followed by every velocity. `solve_ivp` evolves that vector through time by repeatedly calling `SolarSystem.ThreeBodyEquations`, which returns its time derivative:

- **d(position)/dt = velocity**
- **d(velocity)/dt = acceleration**, from Newton's law: body *i* is pulled towards each body *j* with acceleration G·mⱼ·(rⱼ − rᵢ)/|rⱼ − rᵢ|³.

The accelerations are vectorised with NumPy. Broadcasting `x.T - x` builds an N × N matrix of every pairwise separation in one step. That matrix is combined with the 1/r³ factors and then matrix-multiplied by the mass vector, so no Python loop over pairs is needed. The self-interaction terms (r = 0) are left at zero.

`solve_ivp` picks its own step size to hit the requested tolerances, so the output times are **not evenly spaced**. After integrating, the positions are moved into the centre-of-mass frame. `SolarSystem.getEnergy` then computes the energies and momenta at every output step, and these are plotted. Total energy should stay flat. The script reports the first step where it drifts by more than 1%.

### Rendering the animation (`render.py`)

1. **Resample in time.** The adaptive-step output is linearly interpolated onto an evenly spaced grid of `--frames` points (300 by default). Every frame therefore covers the same amount of simulated time and the bodies move at a steady speed.
2. **Build the figure once.** Each body gets one trail line and one marker. The axis limits are fixed from the whole trajectory, so the view does not jump.
3. **Update, don't redraw.** Each frame only changes the data of those existing artists (`set_data_3d`).
4. **Stream to the encoder.** `FuncAnimation.save` draws each frame and pipes its pixels straight into FFmpeg (H.264, `yuv420p`). Memory stays flat regardless of video length. The writer is chosen explicitly. If FFmpeg is missing, the output is a GIF via Pillow and a warning explains why.

A 300-frame, 960×960 MP4 of the Solar System renders in about 45 seconds on a Raspberry Pi 5.

## Files

| File | Purpose |
| --- | --- |
| `Simulation (GUI).py` | **Entry point.** Reads the GUI / command-line settings, integrates, analyses, plots and optionally animates. |
| `n_body_app.py` | The Tkinter GUI. |
| `Objects.py` | `Objects` class: one body's name, mass, initial position and velocity, plus per-step energy / momentum history. |
| `init_objects.py` | Every body and configuration that can be simulated, with initial conditions (planets from NASA JPL Horizons ephemerides, converted from AU and AU/day to SI units). |
| `solar.py` | `SolarSystem`: the equations of motion for the integrator, and the energy / momentum calculations. |
| `render.py` | Turns the solution into an MP4 (or GIF) animation. |
| `Lagrange Points.py` | Standalone: effective potential and Lagrange points of a two-body system, with mass ratio `mu = m2 / (m1 + m2)`. Change the two masses in the `mass` array near the top (equal masses give mu = 0.5). |

## Initial conditions which produce sensible orbits

Three-body choreographies use G = 1 and unit masses. They are unstable orbits: small numerical errors grow quickly, so they need a high-order solver with tight tolerances. With RK45 at `rtol = 1e-3`, Butterfly I loses energy conservation within the first tenth of a period.

| N body system | Time Period | Number of Periods | G | Iterations Per Period | ODE Solver | rtol / atol |
| :-----------: | :---------: | :---------------: | :-: | :-----------------: | :--------: | :---------: |
| Solar System | 31536000 (1 year, s) | 100 | 6.6743015e-11 | 25 | RK45 | 1e-3 / 1e-6 |
| Figure of Eight | 6.32591398 | 0.5 | 1 | 25 | RK45 | 1e-3 / 1e-6 |
| butterfly_I | 6.235641 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| butterfly_II | 7.0039 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| butterfly_III | 13.8658 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| moth_I | 14.8939 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| moth_II | 28.6703 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| moth_III | 25.8406 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| bumblebee | 63.5345 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| goggles | 10.4668 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| dragonfly | 21.2710 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| yarn | 55.5018 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |
| yin_yang_I_a | 17.3284 | 1 | 1 | 200 | DOP853 | 1e-9 / 1e-9 |

The choreography initial velocities and periods are from Šuvakov & Dmitrašinović, *Three Classes of Newtonian Three-Body Planar Periodic Orbits*, Phys. Rev. Lett. 110, 114301 (2013).

## Future updates

- [ ] Improved GUI
- [ ] Plots whose line colour varies with velocity
- [ ] Add more periodic orbits
- [ ] Monitor the evolution of star clusters
- [ ] Link the Lagrange script with the simulation

## Author

**Harry Spratt** — [GitHub](https://github.com/hsspratt "Harry")

Give a ⭐️ if you like this project!
