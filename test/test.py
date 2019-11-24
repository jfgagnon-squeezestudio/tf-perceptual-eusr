import argparse
import os

import numpy as np
import tensorflow as tf


# params
parser = argparse.ArgumentParser()
parser.add_argument('--model_name', default='model.pb', help='path of the model file (.pb)')
parser.add_argument('--input_path', default='Sources', help='base path of low resolution (input) images')
parser.add_argument('--output_path', default='Results', help='base path of super resolution (output) images')
parser.add_argument('--use_gpu', action='store_true', help='enable GPU utilization (default: disabled)')
args = parser.parse_args()


def main():
  if (not args.use_gpu):
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

  # load and build graph
  with tf.Graph().as_default():
    model_input_path = tf.placeholder(tf.string, [])
    model_output_path = tf.placeholder(tf.string, [])

    image = tf.read_file(model_input_path)
    image = [tf.image.decode_png(image, channels=3, dtype=tf.uint8)]
    image = tf.cast(image, tf.float32)

    with tf.gfile.GFile(args.model_name, 'rb') as f:
      model_graph_def = tf.GraphDef()
      model_graph_def.ParseFromString(f.read())

    model_output = tf.import_graph_def(model_graph_def, name='model', input_map={'sr_input:0': image}, return_elements=['sr_output:0'])[0]

    model_output = model_output[0, :, :, :]
    model_output = tf.round(model_output)
    model_output = tf.clip_by_value(model_output, 0, 255)
    model_output = tf.cast(model_output, tf.uint8)

    image = tf.image.encode_png(model_output)
    write_op = tf.write_file(model_output_path, image)

    init = tf.global_variables_initializer()

    sess = tf.Session(config=tf.ConfigProto(
        log_device_placement=False,
        allow_soft_placement=True
    ))
    sess.run(init)

  # get image path list
  image_path_list = []
  for root, subdirs, files in os.walk(args.input_path):
    for filename in files:
      filenameLowerCase = filename.lower()
      if (filenameLowerCase.endswith('.png') or filenameLowerCase.endswith('.jpg')):
        input_path = os.path.join(args.input_path, filename)

        # use a different file naming scheme; easier to compare
        # output_path = os.path.join(args.output_path, filename )
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(args.output_path, f"{name}_4pp_eusr{ext}" )

        image_path_list.append([input_path, output_path])
  print('Found %d images' % (len(image_path_list)))

  # iterate
  for input_path, output_path in image_path_list:
    print('- %s -> %s' % (input_path, output_path))
    sess.run([write_op], feed_dict={model_input_path:input_path, model_output_path:output_path})

  print('Done')


if __name__ == '__main__':
  main()