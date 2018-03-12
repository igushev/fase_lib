import unittest

import phone_number_verifier


class PhoneNumberVerifierTest(unittest.TestCase):
  
  def setUp(self):
    unittest.TestCase.setUp(self)
  
  def testNoCountryCode(self):
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('4803210000', 'US'))
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('(480) 321-0000', 'US'))
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('480.321.00.00', 'US'))
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('480 321 00 00', 'US'))

  def testNoCountry(self):
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('+14803210000', None))
    self.assertEqual(
        '+14803210000',
        phone_number_verifier.Format('+1 (480) 321-0000', None))

  def testCountryCodeSameAsCountry(self):
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('+14803210000', 'US'))
    self.assertEqual(
        '+14803210000',
        phone_number_verifier.Format('+1 (480) 321-0000', 'US'))

  def testCountryCodeOverridesCounty(self):
    self.assertEqual('+14803210000',
                     phone_number_verifier.Format('+14803210000', 'RU'))
    self.assertEqual(
        '+14803210000',
        phone_number_verifier.Format('+1 (480) 321-0000', 'RU'))

  def testCountryCouldNotBeInferreds(self):
    self.assertRaises(
        phone_number_verifier.NoCountryCodeException,
        phone_number_verifier.Format, '4803210000', None)

  def testInvalidPhoneNumber(self):
    self.assertRaises(phone_number_verifier.InvalidPhoneNumberException,
                      phone_number_verifier.Format, '48032100', 'US')

  def testCountryCode(self):
    self.assertEqual(
        'US',
        phone_number_verifier.GetCountryCode('+14803210000', None))
    self.assertEqual(
        'US',
        phone_number_verifier.GetCountryCode('+1 (480) 321-0000', None))


if __name__ == '__main__':
    unittest.main()
