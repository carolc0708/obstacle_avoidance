from math import sqrt

class CustomFilter(object):
	def __init__(self, sampleCount=10, sigmaFactor=1.5):
		# public data
		self.sampleCount = sampleCount
		self.sigmaFactor = sigmaFactor
		self.observations = []
		# private data
		self.__sum        = 0.0
		self.__squaredSum = 0.0
		self.__mean       = 0.0
		self.__sigma      = 0.0
		self.__lastQualified = float("-INF")

	def setSampleCount(self, sampleCount):
		self.sampleCount = sampleCount

	def setSigmaFactor(self, sigmaFactor):
		self.sigmaFactor = sigmaFactor
		

	def observe(self, observedValue):
		# determine
		halfWindow = self.sigmaFactor * self.__sigma
		if (self.__mean - halfWindow <= observedValue <= self.__mean + halfWindow) or (self.__lastQualified == float("-INF")):
			# qualified
			self.__lastQualified = observedValue

		# update observations
		self.observations.append(observedValue)
		self.observations = self.observations[-(self.sampleCount):]
		self.__compute()
		
		return self.__lastQualified

	def __compute(self):
		"""
		compute the __sum and __squaredSum
		"""
		self.__sum = sum(self.observations)
		self.__squaredSum = sum(map(lambda x: x**2, self.observations))
		self.__mean = self.__sum / len(self.observations)
		self.__sigma = sqrt((self.__squaredSum / len(self.observations)) - (self.__mean ** 2))


