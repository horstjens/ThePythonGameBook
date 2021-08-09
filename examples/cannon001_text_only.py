# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion

# this variant is text-only
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress

# initial values





t = 0 # start time value
x_target = 100
print("the target is at x position ", x_target, "and at y position 0" )
try:
	vx0 = float(input("speed in x direction in [m/s] (enter=10)"))
except ValueError:
	vx0 = 10
try:
	vy0 = float(input("speed in y direction in [m/s] (enter=12)"))
except ValueError:
	vy0 = 12
g = -9.81
x0 = 0   # position of cannon
y0 = 0   # position of cannon
t = 0 # start time
dt = 0.05 # delta-time
y=0
while y >= 0:
	t += dt          # next time step
	x = x0 + vx0 * t # constant horizontal speed
	y = y0 + vy0 * t + 0.5 * g *  t * t

	print(f"time: {t:.3f}, x:{x:.3f} y:{y:.3f} ")

