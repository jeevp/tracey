import cv2 as cv

class Tracey:
    def __init__(self, source, params):
        self.source = source
        self.height, self.width = self.source.shape[:2]
        self.area = self.width * self.height
        self.trace_type = params['trace_type']
        self.threshold_type = params['threshold_type']
        self.threshold_value = params['threshold_value']
        self.min_edge_value = params['min_edge_value']
        self.max_edge_value = params['max_edge_value']
        self.min_path_area = params['min_path_area']
        self.max_path_area = params['max_path_area']
        self.path_complexity = params['path_complexity']
        self.stroke_width = params['stroke_width']
        
        self.threshold = None
        self.edges = None
        self.contours = []
        self.paths = []
        self.svg_string = None

    def to_grayscale(self):
        self.source = cv.cvtColor(self.source, cv.COLOR_BGR2GRAY)

    def blur(self, val):
        self.source = cv.medianBlur(self.source, val)

    def get_threshold(self):
        threshold = None
        if self.threshold_type == 'gaussian':
            threshold = cv.adaptiveThreshold(self.source, self.threshold_value, cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY,11,2)
        elif self.threshold_type == 'mean value':
            threshold = cv.adaptiveThreshold(self.source, self.threshold_value, cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY,11,2)
        else:
            ret, threshold = cv.threshold(self.source, self.threshold_value, 255, cv.THRESH_BINARY)

        self.threshold = cv.Canny(threshold, 200, 200)

    def get_edges(self):
        self.edges = cv.Canny(self.source, self.min_edge_value, self.max_edge_value)

    def get_contours(self):
        threshold_contours = []
        edge_contours = []
        if self.threshold is not None:
            threshold_contours, _ = cv.findContours(self.threshold, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if self.edges is not None:
            edge_contours, _ = cv.findContours(self.edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        self.contours = list(threshold_contours) + (list(edge_contours))

    def smooth_contours(self):
        smoothened = []

        for contour in self.contours:
            epsilon = float((5 - self.path_complexity) / 1000) * cv.arcLength(contour,True)
            approx = cv.approxPolyDP(contour,epsilon,True)
            smoothened.append(approx)

        self.contours = smoothened

    def get_paths(self):
        for c in self.contours:
            area = cv.contourArea(c)
            if area > self.min_path_area:
                path = []
                for i in range(len(c)):
                    x, y = c[i][0]
                    point = [int(x), int(y)] 
                    path.append(point)

                self.paths.append(path)