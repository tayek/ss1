https://stackoverflow.com/questions/55891999/passing-dataset-from-tensor-slices-a-list-vs-a-tuple

ldscd has examples of datasets from tensor slices.
but the parse function throws: Input filename tensor must be scalar, but had shape: [3] [Op:ReadFile]
so maybe try a vanilla ing example.
ldscd.py show us that we need to pass args as a tuple.
all of the examples of image processing use list files dataset or flow from.
can we find one that uses from tendor slices

2 problems
    1: from file dataset takes forever
    2. can't seem to get the from tensor slices to work (triple)

images.py works:
list_ds = tf.data.Dataset.list_files(str(data_dir/'*/*'))
def process_path(file_path):
labeled_ds = list_ds.map(process_path, num_parallel_calls=AUTOTUNE)
looks like process path matches the dataset

also my version of ingpipe works:
list_ds = tf.data.Dataset.list_files(str(flowers_root/'*/*'),shuffle=False)
def parse_function(image,json,label):
def train_preprocess(image,json,label):
(image,json,label)=parse_function(name,None,None)

# also investigate doing a list files from each of the camera directories
image_generator.flow_from_directory(directory=str(data_dir),

# looks like everything is broken :(
so start over with very small dataset and get the tuples working again
import the functions as fu if you are going to use the variable f!

i fixed ldscd - see the code in template.py. this let me fix everthing else.

see the stuff at the bottom of ingpipe.py

ok, plan is to use one list of files and make a pipe, then tune it.

