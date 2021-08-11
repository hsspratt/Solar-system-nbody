import numpy as np
from Objects import Objects

"""This Script initialises all the possible particles in the simulation"""
"""If used the GUI will import them into the simulation"""

au = 149597870.700e3
v_factor = 1731460

Sun = Objects('Sun',
              1988500e24,
              au*np.array([-7.932203384657881E-03,
                           4.576434484384691E-03, 1.479483049627150E-04]),
              v_factor*np.array([-5.116440742689573E-06,
                                 -7.548741777331740E-06, 1.825765308106876E-07]),
              np.array([0, 0, 0]))

Sun_Correction = Objects('Sun',
              1988500e24,
              au*np.array([-7.932203384657881E-03,
                           4.576434484384691E-03, 1.479483049627150E-04]),
              v_factor * np.array([-2.632609686583844E-03,
                                   2.764737962269393E-03, 4.446950323113948E-05]),
              np.array([0, 0, 0]))

Another_Sun = Objects('Another_Sun',
                      1988500e24,
                      2*au * np.array([1.479571727799367E+01, 1.306770973748618E+01, -1.431474102367680E-01]),
                      2*v_factor *np.array([-2.632609686583844E-03,
                                            2.764737962269393E-03, 4.446950323113948E-05]),
                      np.array([0, 0, 0]))

Another_Sun_2 = Objects('Another_Sun_2',
                      1988500e24,
                      -0.5*au*np.array([1.538595512099490E+01, 1.241875975077764E+01, -1.532033630108008E-01]),
                      -1*v_factor *np.array([-2.499218584280511E-03,2.877287547390077E-03, 4.308752491196167E-05]),
                      np.array([0, 0, 0]))

Mercury = Objects('Mercury',
                  3.302e23,
                  au*np.array([-2.258744573853126E-01,
                               2.502770299695787E-01, 4.021760798332741E-02]),
                  v_factor*np.array([-2.674938028762872E-02, -1.755675852940837E-02, 1.019350715882785E-03]),
                  np.array([0, 0, 0]))

Venus = Objects('Venus',
                48.685e23,
                au*np.array([-6.120672492472573E-01, -3.906996999210303E-01, 2.958483012976075E-02]),
                v_factor*np.array([1.092695410675457E-02, -1.702850268989552E-02, -8.642525466268606E-04]),
                np.array([0, 0, 0]))

Earth = Objects('Earth',
                5.97219e24,
                au*np.array([6.395629420203809E-01,-7.769140281470991E-01, 1.835752196084453E-04]),
                v_factor*np.array([1.296818098337282E-02,1.090114898144773E-02, -9.693601006289686E-07]),
                np.array([0, 0, 0]))

Moon = Objects('Moon',
               7.349e22,
               au*np.array([6.410981302237438E-01,-7.746901149771338E-01, 1.282168170254214E-04]),
               v_factor*np.array([1.251232258393357E-02,1.122022039859994E-02, 4.737737905969339E-05]),
               np.array([0, 0, 0]))

Mars = Objects('Mars',
               6.4171e23,
               au*np.array([-1.613948148438230E+00, 4.372027834380768E-01, 4.860976754423750E-02]),
               v_factor*np.array([-3.123238923661745E-03,-1.232465630887759E-02, -1.814589041425858E-04]),
               np.array([0, 0, 0]))

Jupiter = Objects('Jupiter',
                  1898.13e24,
                  au*np.array([4.128063617906158E+00, -2.856498246757150E+00, -8.050447120129219E-02]),
                  v_factor * np.array([4.202083601147365E-03, 6.561307005242606E-03, -1.211923198261824E-04]),
                  np.array([0, 0, 0]))

Saturn = Objects('Saturn',
                 5.6834e26,
                 au*np.array([6.370896530654654E+00, -7.630885322259265E+00, -1.209644585741731E-01]),
                 v_factor * np.array([3.969868232078870E-03, 3.562972729982103E-03, -2.199405188789550E-04]),
                 np.array([0, 0, 0]))

Uranus = Objects('Uranus',
                 86.813e24,
                 au*np.array([1.479571727799367E+01, 1.306770973748618E+01, -1.431474102367680E-01]),
                 v_factor*np.array([-2.632609686583844E-03, 2.764737962269393E-03, 4.446950323113948E-05]),
                 np.array([0, 0, 0]))

Neptune = Objects('Neptune',
                  102.409e24,
                  au*np.array([2.955884739850362E+01,-4.562241206494599E+00,-5.872628016135284E-01]),
                  v_factor * np.array([4.582772330863828E-04, 3.121459213492627E-03, -7.462776064764451E-05]),
                  np.array([0, 0, 0]))

Pluto = Objects('Pluto',
                1.307e22,
                au*np.array([1.467673627807559E+01, -3.101557364151601E+01, -9.265382051562835E-01]),
                v_factor * np.array([2.906899017147553E-03, 6.557710096014214E-04, -9.211135139488575E-04]),
                np.array([0, 0, 0]))

F8_1 = Objects('F8_1',
               1,
               np.array([-0.97000436, 0.24308753, 0]),
               np.array([0.4662036850, 0.4323657300, 0]),
               np.array([0, 0, 0]))

F8_2 = Objects('F8_2',
               1,
               np.array([0.97000436, -0.24308753, 0]),
               np.array([0.4662036850, 0.4323657300, 0]),
               np.array([0, 0, 0]))

F8_3 = Objects('F8_3',
               1,
               np.array([0, 0, 0]),
               np.array([-0.93240737, -0.86473146, 0]),
               np.array([0, 0, 0]))

F8_I_1 = Objects('F8_I_1',
                 1,
                 np.array([-1, 0, 0]),
                 np.array([0.347111, 0.532728, 0]),
                 np.array([0, 0, 0]))
F8_I_2 = Objects('F8_I_2',
                 1,
                 np.array([1, 0, 0]),
                 np.array([0.347111, 0.532728, 0]),
                 np.array([0, 0, 0]))
F8_I_3 = Objects('F8_I_3',
                 1,
                 np.array([0, 0, 0]),
                 np.array([-2*0.347111, -2*0.532728, 0]),
                 np.array([0, 0, 0]))

Flower_in_circle_1 = Objects('Flower_1',
                 1,
                 np.array([-0.602885898116520, 1.059162128863347-1,0]),
                 np.array([0.122913546623784,0.747443868604908, 0]),
                 np.array([0, 0, 0]))

Flower_in_circle_2 = Objects('Flower_2',
                 1,
                 np.array([0.252709795391000, 1.058254872224370-1, 0]),
                 np.array([-0.019325586404545, 1.369241993562101, 0]),
                 np.array([0, 0, 0]))

Flower_in_circle_3 = Objects('Flower_3',
                 1,
                 np.array([-0.355389016941814,1.038323764315145-1, 0]),
                 np.array([-0.103587960218793,- 2.116685862168820, 0]),
                 np.array([0, 0, 0]))

F8_planet = Objects('F8_planet',
                    0.001,
                    np.array([-0.33, -0.3, 0]),
                    np.array([0, 0, 0]),
                    np.array([0, 0, 0]))

AC1 = Objects('AC1',
              1.1,
              np.array([-0.5, 0, 0]),
              np.array([0.085, 0.05, -0.1]),
              np.array([0, 0, 0]))

AC2 = Objects('AC2',
              0.9,
              np.array([0.5, 0, 0]),
              np.array([-0.085, -0.05, -0.1]),
              np.array([0, 0, 0]))

AC_star = Objects('AC_star',
                  1.0,
                  np.array([0, 1, 0]),
                  np.array([0, -0.01, 0]),
                  np.array([0, 0, 0]))

Objects_I_pos = [-1, 0, 0]
Objects_II_pos = [1, 0, 0]
Objects_III_pos = [0, 0, 0]


butterfly_I = [0.306893, 0.125507, 0, 6.2356]
butterfly_II = [0.39295, 0.09758, 0, 7.0039]
butterfly_III = [0.40592, 0.23016, 0, 13.8658]
bumblebee = [0.18428, 0.58719, 0, 63.5345]
moth_I = [0.46444, 0.39606, 0, 14.8939]
moth_II = [0.43917, 0.45297, 0, 28.6703]
moth_III = [0.38344, 0.37736, 0, 25.8406]
goggles = [0.08330, 0.12789, 0, 10.4668]
dragonfly = [0.08058, 0.58884, 0, 21.2710]
yarn = [0.55906, 0.34919, 55.5018]
yin_yang_I_a = [0.51394, 0.30474, 0, 17.3284]
yin_yang_I_b = [0.28270, 0.32721, 0, 10.9626]
yin_yang_II_a = [0.41682, 0.33033, 0, 55.7898]
yin_yang_II_b = [0.41734, 0.31310, 0, 54.2076]


Butterfly_I_1 = Objects('Butterfly I - Planet 1',
                        1,
                        np.array(Objects_I_pos),
                        np.array(
                            [butterfly_I[0], butterfly_I[1], butterfly_I[2]]),
                        np.array([0, 0, 0]))

Butterfly_I_2 = Objects('Butterfly I - Planet 2',
                        1,
                        np.array(Objects_II_pos),
                        np.array(
                            [butterfly_I[0], butterfly_I[1], butterfly_I[2]]),
                        np.array([0, 0, 0]))

Butterfly_I_3 = Objects('Butterfly I - Planet 3',
                        1,
                        np.array(Objects_III_pos),
                        np.array([-2*butterfly_I[0], -2 *
                                  butterfly_I[1], butterfly_I[2]]),
                        np.array([0, 0, 0]))

Butterfly_II_1 = Objects('Butterfly II - Planet 1',
                         1,
                         np.array(Objects_I_pos),
                         np.array(
                             [butterfly_II[0], butterfly_II[1], butterfly_II[2]]),
                         np.array([0, 0, 0]))

Butterfly_II_2 = Objects('Butterfly II - Planet 2',
                         1,
                         np.array(Objects_II_pos),
                         np.array(
                             [butterfly_II[0], butterfly_II[1], butterfly_II[2]]),
                         np.array([0, 0, 0]))

Butterfly_II_3 = Objects('Butterfly II - Planet 3',
                         1,
                         np.array(Objects_III_pos),
                         np.array([-2*butterfly_II[0], -2 *
                                   butterfly_II[1], butterfly_II[2]]),
                         np.array([0, 0, 0]))

Butterfly_III_1 = Objects('Butterfly III - Planet 1',
                          1,
                          np.array(Objects_I_pos),
                          np.array(
                              [butterfly_III[0], butterfly_III[1], butterfly_III[2]]),
                          np.array([0, 0, 0]))

Butterfly_III_2 = Objects('Butterfly III - Planet 2',
                          1,
                          np.array(Objects_II_pos),
                          np.array(
                              [butterfly_III[0], butterfly_III[1], butterfly_III[2]]),
                          np.array([0, 0, 0]))

Butterfly_III_3 = Objects('Butterfly III - Planet 3',
                          1,
                          np.array(Objects_III_pos),
                          np.array([-2*butterfly_III[0], -2 *
                                    butterfly_III[1], butterfly_III[2]]),
                          np.array([0, 0, 0]))

bumblebee_1 = Objects('bumblebee I - Planet 1',
                      1,
                      np.array(Objects_I_pos),
                      np.array([bumblebee[0], bumblebee[1], bumblebee[2]]),
                      np.array([0, 0, 0]))

bumblebee_2 = Objects('bumblebee I - Planet 2',
                      1,
                      np.array(Objects_II_pos),
                      np.array([bumblebee[0], bumblebee[1], bumblebee[2]]),
                      np.array([0, 0, 0]))

bumblebee_3 = Objects('bumblebee I - Planet 3',
                      1,
                      np.array(Objects_III_pos),
                      np.array(
                          [-2*bumblebee[0], -2*bumblebee[1], bumblebee[2]]),
                      np.array([0, 0, 0]))

moth_I_1 = Objects('moth I - Planet 1',
                   1,
                   np.array(Objects_I_pos),
                   np.array([moth_I[0], moth_I[1], moth_I[2]]),
                   np.array([0, 0, 0]))

moth_I_2 = Objects('moth I - Planet 2',
                   1,
                   np.array(Objects_II_pos),
                   np.array([moth_I[0], moth_I[1], moth_I[2]]),
                   np.array([0, 0, 0]))

moth_I_3 = Objects('moth I - Planet 3',
                   1,
                   np.array(Objects_III_pos),
                   np.array([-2*moth_I[0], -2*moth_I[1], moth_I[2]]),
                   np.array([0, 0, 0]))

moth_II_1 = Objects('moth II - Planet 1',
                    1,
                    np.array(Objects_I_pos),
                    np.array([moth_II[0], moth_II[1], moth_II[2]]),
                    np.array([0, 0, 0]))

moth_II_2 = Objects('moth II - Planet 2',
                    1,
                    np.array(Objects_II_pos),
                    np.array([moth_II[0], moth_II[1], moth_II[2]]),
                    np.array([0, 0, 0]))

moth_II_3 = Objects('moth II - Planet 3',
                    1,
                    np.array(Objects_III_pos),
                    np.array([-2*moth_II[0], -2*moth_II[1], moth_II[2]]),
                    np.array([0, 0, 0]))

moth_III_1 = Objects('moth III - Planet 1',
                     1,
                     np.array(Objects_I_pos),
                     np.array([moth_III[0], moth_III[1], moth_III[2]]),
                     np.array([0, 0, 0]))

moth_III_2 = Objects('moth III - Planet 2',
                     1,
                     np.array(Objects_II_pos),
                     np.array([moth_III[0], moth_III[1], moth_III[2]]),
                     np.array([0, 0, 0]))

moth_III_3 = Objects('moth III - Planet 3',
                     1,
                     np.array(Objects_III_pos),
                     np.array([-2*moth_III[0], -2*moth_III[1], moth_III[2]]),
                     np.array([0, 0, 0]))

goggles_1 = Objects('goggles - Planet 1',
                     1,
                     np.array(Objects_I_pos),
                     np.array([goggles[0], goggles[1], goggles[2]]),
                     np.array([0, 0, 0]))

goggles_2 = Objects('goggles - Planet 2',
                     1,
                     np.array(Objects_II_pos),
                     np.array([goggles[0], goggles[1], goggles[2]]),
                     np.array([0, 0, 0]))

goggles_3 = Objects('goggles - Planet 3',
                     1,
                     np.array(Objects_III_pos),
                     np.array([-2*goggles[0], -2*goggles[1], goggles[2]]),
                     np.array([0, 0, 0]))

dragonfly_1 = Objects('dragonfly - Planet 1',
                    1,
                    np.array(Objects_I_pos),
                    np.array([dragonfly[0], dragonfly[1], dragonfly[2]]),
                    np.array([0, 0, 0]))

dragonfly_2 = Objects('dragonfly - Planet 2',
                    1,
                    np.array(Objects_II_pos),
                    np.array([dragonfly[0], dragonfly[1], dragonfly[2]]),
                    np.array([0, 0, 0]))

dragonfly_3 = Objects('dragonfly - Planet 3',
                    1,
                    np.array(Objects_III_pos),
                    np.array([-2*dragonfly[0], -2*dragonfly[1], dragonfly[2]]),
                    np.array([0, 0, 0]))

yarn_1 = Objects('yarn - Planet 1',
                      1,
                      np.array(Objects_I_pos),
                      np.array([yarn[0], yarn[1], yarn[2]]),
                      np.array([0, 0, 0]))

yarn_2 = Objects('yarn - Planet 2',
                      1,
                      np.array(Objects_II_pos),
                      np.array([yarn[0], yarn[1], yarn[2]]),
                      np.array([0, 0, 0]))

yarn_3 = Objects('yarn - Planet 3',
                      1,
                      np.array(Objects_III_pos),
                      np.array(
                          [-2*yarn[0], -2*yarn[1], yarn[2]]),
                      np.array([0, 0, 0]))

yin_yang_I_a_1 = Objects('yin_yang_I_a - Planet 1',
                 1,
                 np.array(Objects_I_pos),
                 np.array([yin_yang_I_a[0], yin_yang_I_a[1], yin_yang_I_a[2]]),
                 np.array([0, 0, 0]))

yin_yang_I_a_2 = Objects('yin_yang_I_a - Planet 2',
                 1,
                 np.array(Objects_II_pos),
                 np.array([yin_yang_I_a[0], yin_yang_I_a[1], yin_yang_I_a[2]]),
                 np.array([0, 0, 0]))

yin_yang_I_a_3 = Objects('yin_yang_I_a - Planet 3',
                 1,
                 np.array(Objects_III_pos),
                 np.array(
                     [-2*yin_yang_I_a[0], -2*yin_yang_I_a[1], yin_yang_I_a[2]]),
                 np.array([0, 0, 0]))

pythag_1 = Objects('pythag_1',
                   1,
                   np.array([1, 3, 0]),
                   np.array([0, 0, 0]),
                   np.array([0, 0, 0]))

pythag_2 = Objects('pythag_2',
                   1,
                   np.array([-2, -1, 0]),
                   np.array([0, 0, 0]),
                   np.array([0, 0, 0]))

pythag_3 = Objects('pythag_3',
                   1,
                   np.array([1, -1, 0]),
                   np.array([0, 0, 0]),
                   np.array([0, 0, 0]))

pythag_I_1 = Objects('pythag_I_1',
                     1,
                     np.array([-0.0347, 1.1856, 0]),
                     np.array([0.2495, -0.1076, 0]),
                     np.array([0, 0, 0]))

pythag_I_2 = Objects('pythag_I_2',
                     1,
                     np.array([0.2693, -1.0020, 0]),
                     np.array([0.2059, -0.9396, 0]),
                     np.array([0, 0, 0]))

pythag_I_3 = Objects('pythag_I_3',
                     1,
                     np.array([-0.2328, -0.5978, 0]),
                     np.array([-0.4553, 1.0471, 0]),
                     np.array([0, 0, 0]))


Sun_I = Objects('Test Planet 1',
                1988500e24,
                au*np.array([-6.534087946884256E-03,
                             6.100454846284101E-03, 1.019968145073305E-04]),
                v_factor*np.array([-6.938967653087248E-06, -
                                   5.599052606952444E-06, 2.173251724105919E-07]),
                np.array([0, 0, 0]))

Sun_II = Objects('Test Planet 2',
                 1988500e24,
                 au*np.array([-6.534087946884256E-03,
                              6.100454846284101E-03, 1.019968145073305E-04]),
                 v_factor*np.array([-6.938967653087248E-06, -
                                    5.599052606952444E-06, 2.173251724105919E-07]),
                 np.array([0, 0, 0]))

Solar_System = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]
Figure_8 = [F8_I_1, F8_I_2, F8_I_3]
Alpha_Centauri = [AC1,AC2]
Butterfly_I = [Butterfly_I_1, Butterfly_I_2, Butterfly_I_3]
Butterfly_II = [Butterfly_II_1, Butterfly_II_2, Butterfly_II_3]
Butterfly_III = [Butterfly_III_1, Butterfly_III_2, Butterfly_III_3]
bumblebee = [bumblebee_1, bumblebee_2, bumblebee_3]
moth_I = [moth_I_1, moth_I_2, moth_I_3]
moth_II = [moth_II_1, moth_II_2, moth_II_3]
moth_III = [moth_III_1, moth_III_2, moth_III_3]
goggles = [goggles_1, goggles_2, goggles_3]
dragonfly = [dragonfly_1, dragonfly_2, dragonfly_3]
yarn = [yarn_1, yarn_2, yarn_3]
yin_yang_I_a = [yin_yang_I_a_1, yin_yang_I_a_2, yin_yang_I_a_3]

pythag = [pythag_1, pythag_2, pythag_3]
pythag_I = [pythag_I_1, pythag_I_2, pythag_I_3]

Flower_in_circle = [Flower_in_circle_1, Flower_in_circle_2, Flower_in_circle_3]
