import Augmentor
p = Augmentor.Pipeline("./input")
p.random_distortion(probability=1, grid_width=14, grid_height=4, magnitude=13)
p.rotate_without_crop( probability=0.5, max_left_rotation=5, max_right_rotation=5, fillcolor='white')
p.process()
