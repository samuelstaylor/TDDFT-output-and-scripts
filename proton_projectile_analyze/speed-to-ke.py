mass = 103.64269314
hydrogen_speeds = [0.1,0.3,0.5,0.7,0.9,1.1,1.3]
hydrogen_ke = [((0.5) * (mass) * (speed ** 2)) for speed in hydrogen_speeds]
for ke in hydrogen_ke:
    print(f"{ke:.2f} eV")