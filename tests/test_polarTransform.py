import os
import sys

import numpy as np

# Look on level up for polarTransform.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import polarTransform
import unittest

from tests.util import loadImage


class TestPolarConversion(unittest.TestCase):
    def setUp(self):
        self.shortAxisApexImage = loadImage('shortAxisApex.png', False, True)
        self.verticalLinesImage = loadImage('verticalLines.png', False)
        self.horizontalLinesImage = loadImage('horizontalLines.png', False)
        self.checkerboardImage = loadImage('checkerboard.png', False)

        self.shortAxisApexPolarImage = loadImage('shortAxisApexPolarImage.png')
        self.shortAxisApexPolarImage_centerMiddle = loadImage('shortAxisApexPolarImage_centerMiddle.png')
        self.verticalLinesPolarImage = loadImage('verticalLinesPolarImage.png')
        self.verticalLinesPolarImage_scaled = loadImage('verticalLinesPolarImage_scaled.png')

    def test_default(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage,
                                                                    center=np.array([401, 365]))

        np.testing.assert_array_equal(ptSettings.center, np.array([401, 365]))
        self.assertEqual(ptSettings.initialRadius, 0)
        self.assertEqual(ptSettings.finalRadius, 543)
        self.assertEqual(ptSettings.initialAngle, 0.0)
        self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.shortAxisApexImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([ptSettings.finalRadius, self.shortAxisApexImage.shape[1] * 2]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage)

    def test_defaultCenter(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage)

        np.testing.assert_array_equal(ptSettings.center, np.array([400, 304]))
        self.assertEqual(ptSettings.initialRadius, 0)
        self.assertEqual(ptSettings.finalRadius, 503)
        self.assertEqual(ptSettings.initialAngle, 0.0)
        self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.shortAxisApexImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([ptSettings.finalRadius, self.shortAxisApexImage.shape[1] * 2]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage_centerMiddle)

    def test_notNumpyArrayCenter(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage,
                                                                    center=[401, 365])
        np.testing.assert_array_equal(ptSettings.center, np.array([401, 365]))
        np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage)

        polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage,
                                                                    center=(401, 365))
        np.testing.assert_array_equal(ptSettings.center, np.array([401, 365]))
        np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage)

    def test_RGBA(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage)

        np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
        self.assertEqual(ptSettings.initialRadius, 0)
        self.assertEqual(ptSettings.finalRadius, 182)
        self.assertEqual(ptSettings.initialAngle, 0.0)
        self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([ptSettings.finalRadius, self.verticalLinesImage.shape[1] * 2]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage)

    def test_IFRadius(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, initialRadius=30,
                                                                    finalRadius=100)

        np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
        self.assertEqual(ptSettings.initialRadius, 30)
        self.assertEqual(ptSettings.finalRadius, 100)
        self.assertEqual(ptSettings.initialAngle, 0.0)
        self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([70, self.verticalLinesImage.shape[1] * 2]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage[30:100, :, :])

    def test_IFRadiusAngle(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, initialRadius=30,
                                                                    finalRadius=100, initialAngle=2 / 4 * np.pi,
                                                                    finalAngle=5 / 4 * np.pi)

        np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
        self.assertEqual(ptSettings.initialRadius, 30)
        self.assertEqual(ptSettings.finalRadius, 100)
        self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
        self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([70, 192]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage[30:100, 128:320, :])

    def test_IFRadiusAngleScaled(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, initialRadius=30,
                                                                    finalRadius=100, initialAngle=2 / 4 * np.pi,
                                                                    finalAngle=5 / 4 * np.pi, radiusSize=140,
                                                                    angleSize=700)

        np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
        self.assertEqual(ptSettings.initialRadius, 30)
        self.assertEqual(ptSettings.finalRadius, 100)
        self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
        self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([140, 700]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage_scaled)

    def test_origin(self):
        polarImage, ptSettings = polarTransform.convertToPolarImage(np.flipud(self.verticalLinesImage),
                                                                    initialRadius=30,
                                                                    finalRadius=100, initialAngle=2 / 4 * np.pi,
                                                                    finalAngle=5 / 4 * np.pi, radiusSize=140,
                                                                    angleSize=700, origin='lower')

        np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
        self.assertEqual(ptSettings.initialRadius, 30)
        self.assertEqual(ptSettings.finalRadius, 100)
        self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
        self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([140, 700]))
        self.assertEqual(ptSettings.origin, 'lower')

        np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage_scaled)

    def test_settings(self):
        polarImage1, ptSettings1 = polarTransform.convertToPolarImage(self.verticalLinesImage,
                                                                      initialRadius=30,
                                                                      finalRadius=100, initialAngle=2 / 4 * np.pi,
                                                                      finalAngle=5 / 4 * np.pi, radiusSize=140,
                                                                      angleSize=700)

        polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, settings=ptSettings1)

        np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
        self.assertEqual(ptSettings.initialRadius, 30)
        self.assertEqual(ptSettings.finalRadius, 100)
        self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
        self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
        self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
        np.testing.assert_array_equal(ptSettings.polarImageSize,
                                      np.array([140, 700]))
        self.assertEqual(ptSettings.origin, 'upper')

        np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage_scaled)

        polarImage2 = ptSettings1.convertToPolarImage(self.verticalLinesImage)
        np.testing.assert_almost_equal(polarImage2, self.verticalLinesPolarImage_scaled)


class TestCartesianConversion(unittest.TestCase):
    def setUp(self):
        self.shortAxisApexImage = loadImage('shortAxisApex.png', False, True)
        self.verticalLinesImage = loadImage('verticalLines.png', False)
        self.horizontalLinesImage = loadImage('horizontalLines.png', False)
        self.checkerboardImage = loadImage('checkerboard.png', False)

        self.shortAxisApexPolarImage = loadImage('shortAxisApexPolarImage.png')
        self.shortAxisApexPolarImage_centerMiddle = loadImage('shortAxisApexPolarImage_centerMiddle.png')
        self.verticalLinesPolarImage = loadImage('verticalLinesPolarImage.png')
        self.verticalLinesPolarImage_scaled = loadImage('verticalLinesPolarImage_scaled.png')

    # def test_default(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage,
    #                                                                 center=np.array([401, 365]))
    #
    #     cartesianImage, ptSettings = polarTransform.convertToCartesianImage(polarImage,
    #                                                                 center=np.array([401, 365]))
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([401, 365]))
    #     self.assertEqual(ptSettings.initialRadius, 0)
    #     self.assertEqual(ptSettings.finalRadius, 543)
    #     self.assertEqual(ptSettings.initialAngle, 0.0)
    #     self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.shortAxisApexImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([ptSettings.finalRadius, self.shortAxisApexImage.shape[1] * 2]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage)

    # def test_defaultCenter(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage)
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([400, 304]))
    #     self.assertEqual(ptSettings.initialRadius, 0)
    #     self.assertEqual(ptSettings.finalRadius, 503)
    #     self.assertEqual(ptSettings.initialAngle, 0.0)
    #     self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.shortAxisApexImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([ptSettings.finalRadius, self.shortAxisApexImage.shape[1] * 2]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage_centerMiddle)
    #
    # def test_notNumpyArrayCenter(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage,
    #                                                                 center=[401, 365])
    #     np.testing.assert_array_equal(ptSettings.center, np.array([401, 365]))
    #     np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage)
    #
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.shortAxisApexImage,
    #                                                                 center=(401, 365))
    #     np.testing.assert_array_equal(ptSettings.center, np.array([401, 365]))
    #     np.testing.assert_almost_equal(polarImage, self.shortAxisApexPolarImage)
    #
    # def test_RGBA(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage)
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
    #     self.assertEqual(ptSettings.initialRadius, 0)
    #     self.assertEqual(ptSettings.finalRadius, 182)
    #     self.assertEqual(ptSettings.initialAngle, 0.0)
    #     self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([ptSettings.finalRadius, self.verticalLinesImage.shape[1] * 2]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage)
    #
    # def test_IFRadius(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, initialRadius=30,
    #                                                                 finalRadius=100)
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
    #     self.assertEqual(ptSettings.initialRadius, 30)
    #     self.assertEqual(ptSettings.finalRadius, 100)
    #     self.assertEqual(ptSettings.initialAngle, 0.0)
    #     self.assertEqual(ptSettings.finalAngle, 2 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([70, self.verticalLinesImage.shape[1] * 2]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage[30:100, :, :])
    #
    # def test_IFRadiusAngle(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, initialRadius=30,
    #                                                                 finalRadius=100, initialAngle=2 / 4 * np.pi,
    #                                                                 finalAngle=5 / 4 * np.pi)
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
    #     self.assertEqual(ptSettings.initialRadius, 30)
    #     self.assertEqual(ptSettings.finalRadius, 100)
    #     self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
    #     self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([70, 192]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage[30:100, 128:320, :])
    #
    # def test_IFRadiusAngleScaled(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, initialRadius=30,
    #                                                                 finalRadius=100, initialAngle=2 / 4 * np.pi,
    #                                                                 finalAngle=5 / 4 * np.pi, radiusSize=140,
    #                                                                 angleSize=700)
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
    #     self.assertEqual(ptSettings.initialRadius, 30)
    #     self.assertEqual(ptSettings.finalRadius, 100)
    #     self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
    #     self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([140, 700]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage_scaled)
    #
    # def test_origin(self):
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(np.flipud(self.verticalLinesImage),
    #                                                                 initialRadius=30,
    #                                                                 finalRadius=100, initialAngle=2 / 4 * np.pi,
    #                                                                 finalAngle=5 / 4 * np.pi, radiusSize=140,
    #                                                                 angleSize=700, origin='lower')
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
    #     self.assertEqual(ptSettings.initialRadius, 30)
    #     self.assertEqual(ptSettings.finalRadius, 100)
    #     self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
    #     self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([140, 700]))
    #     self.assertEqual(ptSettings.origin, 'lower')
    #
    #     np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage_scaled)
    #
    # def test_settings(self):
    #     polarImage1, ptSettings1 = polarTransform.convertToPolarImage(self.verticalLinesImage,
    #                                                                   initialRadius=30,
    #                                                                   finalRadius=100, initialAngle=2 / 4 * np.pi,
    #                                                                   finalAngle=5 / 4 * np.pi, radiusSize=140,
    #                                                                   angleSize=700)
    #
    #     polarImage, ptSettings = polarTransform.convertToPolarImage(self.verticalLinesImage, settings=ptSettings1)
    #
    #     np.testing.assert_array_equal(ptSettings.center, np.array([128, 128]))
    #     self.assertEqual(ptSettings.initialRadius, 30)
    #     self.assertEqual(ptSettings.finalRadius, 100)
    #     self.assertEqual(ptSettings.initialAngle, 2 / 4 * np.pi)
    #     self.assertEqual(ptSettings.finalAngle, 5 / 4 * np.pi)
    #     self.assertEqual(ptSettings.cartesianImageSize, self.verticalLinesImage.shape)
    #     np.testing.assert_array_equal(ptSettings.polarImageSize,
    #                                   np.array([140, 700]))
    #     self.assertEqual(ptSettings.origin, 'upper')
    #
    #     np.testing.assert_almost_equal(polarImage, self.verticalLinesPolarImage_scaled)
    #
    #     polarImage2 = ptSettings1.convertToPolarImage(self.verticalLinesImage)
    #     np.testing.assert_almost_equal(polarImage2, self.verticalLinesPolarImage_scaled)


if __name__ == '__main__':
    unittest.main()
