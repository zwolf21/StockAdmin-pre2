def get_narcotic_classes(req):
	general = [0] if req.get('general') else []
	narcotic = [1] if req.get('narcotic') else []
	psychotic = [2] if req.get('psychotic') else []
	return general+narcotic+psychotic or []