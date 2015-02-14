def fastCurve(x, val_at_1, val_at_100):
	init = val_at_1
	final = val_at_100

	a = (final - init) / 9.0
	b = 0.5
	c = init - a

	return int(round(a*x**b + c))

def linear(x, val_at_1, val_at_100):
	init = val_at_1
	final = val_at_100

	a = (final - init) / 99.0
	b = init - a

	return int(round(a*x + b))