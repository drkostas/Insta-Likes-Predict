from keras.layers import *
from keras.models import *

IMAGESIZE = (200, 200)


def create_model():
	# create model and add layers
	inp_img = Input(shape=(IMAGESIZE[0], IMAGESIZE[1], 3))
	inp_followers = Input(shape=(1,))

	# Branch 1
	x = Conv2D(10, (5, 5), activation='relu', input_shape=(IMAGESIZE[0], IMAGESIZE[1], 3))(inp_img)   
	x = Conv2D(10, (5, 5), activation='relu')(x)
	x = MaxPool2D((5, 5))(x)
	out_img= Flatten()(x)

	# Branch 2
	out_followers = Dense(10, activation='relu', input_shape=(1,))(inp_followers)

	# Merge the results by concatenation
	merged = concatenate([out_img, out_followers])

	# Final Output
	x = Dense(50)(merged)
	x = Activation('relu')(x)
	output = Dense(1)(x)

	model = Model([inp_img, inp_followers], output)
	model.compile(loss=rmse,
				  optimizer='rmsprop', metrics=[r_square, rmse])
	return model


# root mean squared error (rmse) for regression (only for Keras tensors)
def rmse(y_true, y_pred):
	from keras import backend
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))


# mean squared error (mse) for regression  (only for Keras tensors)
def mse(y_true, y_pred):
	from keras import backend
	return backend.mean(backend.square(y_pred - y_true), axis=-1)


# coefficient of determination (R^2) for regression  (only for Keras tensors)
def r_square(y_true, y_pred):
	from keras import backend as K
	SS_res =  K.sum(K.square(y_true - y_pred)) 
	SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
	return ( 1 - SS_res/(SS_tot + K.epsilon()) )
