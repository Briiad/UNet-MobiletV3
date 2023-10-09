import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2DTranspose, Concatenate
from tensorflow.keras.models import Model

def create_unet_mobilenetv3(input_shape=(224, 224, 3)):
    # Load the MobileNetV3 Small model with ImageNet weights and without the top classification layers
    base_model = tf.keras.applications.MobileNetV3Small(input_shape=input_shape, include_top=False, weights='imagenet')
    
    # Encoder layers: We'll use the outputs of these layers as skip connections in the decoder
    encoder_layers = [
        'input_1',
        'expanded_conv/project/BatchNorm',
        'expanded_conv_3/project/BatchNorm',
        'expanded_conv_6/project/BatchNorm',
    ]
    encoder_outputs = [base_model.get_layer(name).output for name in encoder_layers]
    
    # Create the encoder model
    encoder = tf.keras.Model(inputs=base_model.input, outputs=encoder_outputs)

    # Decoder
    last_encoder_layer = 'expanded_conv_9/project/BatchNorm'
    decoder_input = Input(shape=encoder.get_layer(last_encoder_layer).output.shape[1:])
    x = decoder_input

    for i in range(len(encoder_outputs) -2, -1, -1):
        num_filters = encoder_outputs[i].shape[-1]
        x = Conv2DTranspose(num_filters, (3,3), strides=2, padding='same', activation='relu')(x)
        x = Concatenate()([x, encoder_outputs[i]])

    # Create the decoder model
    x = Conv2DTranspose(3, (3,3), strides=2, padding='same', activation='sigmoid')(x)

    decoder = Model(decoder_input, x)

    # Create the full model
    model = Model(inputs=encoder.input, outputs=decoder(encoder.output))
    
    model.summary()

    return model

# Example usage:
unet_model = create_unet_mobilenetv3()

# Print the number of trainable parameters
print(f"Number of trainable parameters: {unet_model.count_params()}")