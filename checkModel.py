import sys
import onnx

filename = './model.onnx'
model = onnx.load(filename)

print("The model is :\n{}".format(model))
      
try:
    onnx.checker.check_model(model)
except onnx.checker.ValidationError as e:
    print("Model is invalid: %s" % e)
else:
    print("Model is valid")