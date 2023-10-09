import tensorflow as tf

class Dataset:
    def __init__(self, df, tfms):
        self.df = df.to_numpy()  # Convert DataFrame to numpy array for easier indexing
        self.tfms = tfms

    def open_im(self, p, gray=False):
        im = tf.io.read_file(p)
        im = tf.image.decode_image(im, channels=1 if gray else 3)
        return im

    def tf_augment(self, im_path, dp_path):
        im = self.open_im(im_path.decode('utf-8'))
        dp = self.open_im(dp_path.decode('utf-8'), gray=True)
        
        # Apply augmentations here. 
        # Note: You might need to implement or use a library that provides a TensorFlow equivalent 
        # of the augmentations you used with albumentations.
        
        # Example of normalization (if it's part of your augmentations)
        im = tf.image.per_image_standardization(im)
        dp = tf.image.per_image_standardization(dp)

        return im, dp

    def create_tf_dataset(self):
        # Convert the image and mask paths to tensors
        image_paths = tf.convert_to_tensor(self.df[:, 0], dtype=tf.string)
        mask_paths = tf.convert_to_tensor(self.df[:, 1], dtype=tf.string)
        
        # Create a TensorFlow dataset from the paths
        dataset = tf.data.Dataset.from_tensor_slices((image_paths, mask_paths))
        
        # Apply the augmentation function
        dataset = dataset.map(lambda im, dp: tf.py_function(self.tf_augment, [im, dp], [tf.float32, tf.float32]), 
                              num_parallel_calls=tf.data.experimental.AUTOTUNE)
        
        return dataset

# Example usage:
# tf_dataset = TF_Dataset(df, tfms).create_tf_dataset()
