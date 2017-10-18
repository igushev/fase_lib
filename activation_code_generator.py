import random

MIN_ACTIVATION_CODE = 100000
MAX_ACTIVATION_CODE = 1000000


class ActivationCodeGeneratorInterface(object):
  
  def Generate(self):
    raise NotImplemented()


class ActivationCodeGenerator(ActivationCodeGeneratorInterface):
  
  def Generate(self):
    return random.randrange(MIN_ACTIVATION_CODE, MAX_ACTIVATION_CODE)


class MockActivationCodeGenerator(ActivationCodeGeneratorInterface):
  
  def __init__(self, activation_code_generator):
    self.activation_code_generator = activation_code_generator
    self.codes = []
  
  def Generate(self):
    activation_code = self.activation_code_generator.Generate()
    self.codes.append(activation_code)
    return activation_code


