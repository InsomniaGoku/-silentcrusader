from math import log, e

# modified from 3rd party source, added some functions, need further improvement.
try:
    from scipy.stats import norm
except ImportError:
    print('models require scipy to work properly')


def implied_volatility( model, args, CallPrice=None, PutPrice=None, high=500.0, low=0.0 ):
    '''Returns the estimated implied volatility'''
    target = 10
    if CallPrice:
        target = CallPrice
    if PutPrice:
        target = PutPrice
    # accuracy
    epsilon = 0.005
    decimals = 2
    for i in range( 10000 ):  # To avoid infinite loops
        mid = (high + low) / 2
        if mid < 0.00001:
            mid = 0.00001
        if CallPrice:
            estimate = eval( model )( args, volatility=mid, performance=True ).CallPrice
        if PutPrice:
            estimate = eval( model )( args, volatility=mid, performance=True ).PutPrice
        if abs( round( estimate, decimals ) - target ) <= epsilon:
            break
        elif estimate > target:
            high = mid
        elif estimate < target:
            low = mid
    return mid


class BS:
    '''Black-Scholes
	Used for pricing European options on stocks without dividends

	b_s([underlyingPrice, strikePrice, interestRate, daysToExpiration], \
			volatility=x, CallPrice=y, PutPrice=z)

	eg:
		c = b_s([1.4565, 1.45, 1, 30], volatility=20)
		c.CallPrice				# Returns the Call price
		c.PutPrice				# Returns the Put price
		c.CallDelta				# Returns the Call delta
		c.PutDelta				# Returns the Put delta
		c.CallDelta2			# Returns the Call dual delta
		c.PutDelta2				# Returns the Put dual delta
		c.CallTheta				# Returns the Call theta
		c.PutTheta				# Returns the Put theta
		c.CallRho				# Returns the Call rho
		c.PutRho				# Returns the Put rho
		c.vega					# Returns the option vega
		c.gamma					# Returns the option gamma

		c = b_s([1.4565, 1.45, 1, 30], CallPrice=0.0359)
		c.impliedVolatility		# Returns the implied volatility from the Call price

		c = b_s([1.4565, 1.45, 1, 30], PutPrice=0.0306)
		c.impliedVolatility		# Returns the implied volatility from the Put price

		c = b_s([1.4565, 1.45, 1, 30], CallPrice=0.0359, PutPrice=0.0306)
		c.PutCallParity			# Returns the Put-Call parity
		'''

    def __init__( self, args, volatility=None, CallPrice=None, PutPrice=None, \
                  performance=None ):
        self.underlyingPrice = float( args[ 0 ] )
        self.strikePrice = float( args[ 1 ] )
        self.interestRate = float( args[ 2 ] ) / 100
        self.daysToExpiration = float( args[ 3 ] ) / 365

        for i in [ 'CallPrice', 'PutPrice', 'CallDelta', 'PutDelta', \
                   'CallDelta2', 'PutDelta2', 'CallTheta', 'PutTheta', \
                   'CallRho', 'PutRho', 'vega', 'gamma', 'impliedVolatility', \
                   'PutCallParity' ]:
            self.__dict__[ i ] = None

        if volatility:
            self.volatility = float( volatility ) / 100

            self._a_ = self.volatility * self.daysToExpiration ** 0.5
            self._d1_ = (log( self.underlyingPrice / self.strikePrice ) + \
                         (self.interestRate + (self.volatility ** 2) / 2) * \
                         self.daysToExpiration) / self._a_
            self._d2_ = self._d1_ - self._a_
            if performance:
                [ self.CallPrice, self.PutPrice ] = self._price( )
            else:
                [ self.CallPrice, self.PutPrice ] = self._price( )
                [ self.CallDelta, self.PutDelta ] = self._delta( )
                [ self.CallDelta2, self.PutDelta2 ] = self._delta2( )
                [ self.CallTheta, self.PutTheta ] = self._theta( )
                [ self.CallRho, self.PutRho ] = self._rho( )
                self.vega = self._vega( )
                self.gamma = self._gamma( )
                self.exerciceProbability = norm.cdf( self._d2_ )
        if CallPrice:
            self.CallPrice = round( float( CallPrice ), 6 )
            self.impliedVolatility = implied_volatility( \
                self.__class__.__name__, args, CallPrice=self.CallPrice )
        if PutPrice and not CallPrice:
            self.PutPrice = round( float( PutPrice ), 6 )
            self.impliedVolatility = implied_volatility( \
                self.__class__.__name__, args, PutPrice=self.PutPrice )
        if CallPrice and PutPrice:
            self.CallPrice = float( CallPrice )
            self.PutPrice = float( PutPrice )
            self.PutCallParity = self._parity( )

    def _price( self ):
        '''Returns the option price: [Call price, Put price]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = max( 0.0, self.underlyingPrice - self.strikePrice )
            Put = max( 0.0, self.strikePrice - self.underlyingPrice )
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            Call = self.underlyingPrice * norm.cdf( self._d1_ ) - \
                   self.strikePrice * e ** (-self.interestRate * \
                                            self.daysToExpiration) * norm.cdf( self._d2_ )
            Put = self.strikePrice * e ** (-self.interestRate * \
                                           self.daysToExpiration) * norm.cdf( -self._d2_ ) - \
                  self.underlyingPrice * norm.cdf( -self._d1_ )
        return [ Call, Put ]

    def _delta( self ):
        '''Returns the option delta: [Call delta, Put delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = 1.0 if self.underlyingPrice > self.strikePrice else 0.0
            Put = -1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            Call = norm.cdf( self._d1_ )
            Put = -norm.cdf( -self._d1_ )
        return [ Call, Put ]

    def _delta2( self ):
        '''Returns the dual delta: [Call dual delta, Put dual delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = -1.0 if self.underlyingPrice > self.strikePrice else 0.0
            Put = 1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            _b_ = e ** -(self.interestRate * self.daysToExpiration)
            Call = -norm.cdf( self._d2_ ) * _b_
            Put = norm.cdf( -self._d2_ ) * _b_
        return [ Call, Put ]

    def _vega( self ):
        '''Returns the option vega'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            return 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            return self.underlyingPrice * norm.pdf( self._d1_ ) * \
                   self.daysToExpiration ** 0.5 / 100

    def _theta( self ):
        '''Returns the option theta: [Call theta, Put theta]'''
        _b_ = e ** -(self.interestRate * self.daysToExpiration)
        Call = -self.underlyingPrice * norm.pdf( self._d1_ ) * self.volatility / \
               (2 * self.daysToExpiration ** 0.5) - self.interestRate * \
                                                    self.strikePrice * _b_ * norm.cdf( self._d2_ )
        Put = -self.underlyingPrice * norm.pdf( self._d1_ ) * self.volatility / \
              (2 * self.daysToExpiration ** 0.5) + self.interestRate * \
                                                   self.strikePrice * _b_ * norm.cdf( -self._d2_ )
        return [ Call / 365, Put / 365 ]

    def _rho( self ):
        '''Returns the option rho: [Call rho, Put rho]'''
        _b_ = e ** -(self.interestRate * self.daysToExpiration)
        Call = self.strikePrice * self.daysToExpiration * _b_ * \
               norm.cdf( self._d2_ ) / 100
        Put = -self.strikePrice * self.daysToExpiration * _b_ * \
              norm.cdf( -self._d2_ ) / 100
        return [ Call, Put ]

    def _gamma( self ):
        '''Returns the option gamma'''
        return norm.pdf( self._d1_ ) / (self.underlyingPrice * self._a_)

    def _parity( self ):
        '''Put-Call Parity'''
        return self.CallPrice - self.PutPrice - self.underlyingPrice + \
               (self.strikePrice / \
                ((1 + self.interestRate) ** self.daysToExpiration))

    def update( self, update_data ):
        '''use to accept parameter update from market'''
        self.__dict__.update( {'underlyingPrice':update_data['BP1']} )
        print self._price()


class merton:
    '''merton
	Used for pricing European options on stocks with dividends

	merton([underlyingPrice, strikePrice, interestRate, annualDividends, \
			daysToExpiration], volatility=x, CallPrice=y, PutPrice=z)

	eg:
		c = merton([52, 50, 1, 1, 30], volatility=20)
		c.CallPrice				# Returns the Call price
		c.PutPrice				# Returns the Put price
		c.CallDelta				# Returns the Call delta
		c.PutDelta				# Returns the Put delta
		c.CallDelta2			# Returns the Call dual delta
		c.PutDelta2				# Returns the Put dual delta
		c.CallTheta				# Returns the Call theta
		c.PutTheta				# Returns the Put theta
		c.CallRho				# Returns the Call rho
		c.PutRho				# Returns the Put rho
		c.vega					# Returns the option vega
		c.gamma					# Returns the option gamma

		c = merton([52, 50, 1, 1, 30], CallPrice=0.0359)
		c.impliedVolatility		# Returns the implied volatility from the Call price

		c = merton([52, 50, 1, 1, 30], PutPrice=0.0306)
		c.impliedVolatility		# Returns the implied volatility from the Put price

		c = merton([52, 50, 1, 1, 30], CallPrice=0.0359, PutPrice=0.0306)
		c.PutCallParity			# Returns the Put-Call parity
	'''

    def __init__( self, args, volatility=None, CallPrice=None, PutPrice=None, \
                  performance=None ):
        self.underlyingPrice = float( args[ 0 ] )
        self.strikePrice = float( args[ 1 ] )
        self.interestRate = float( args[ 2 ] ) / 100
        self.dividend = float( args[ 3 ] )
        self.dividendYield = self.dividend / self.underlyingPrice
        self.daysToExpiration = float( args[ 4 ] ) / 365

        for i in [ 'CallPrice', 'PutPrice', 'CallDelta', 'PutDelta', \
                   'CallDelta2', 'PutDelta2', 'CallTheta', 'PutTheta', \
                   'CallRho', 'PutRho', 'vega', 'gamma', 'impliedVolatility', \
                   'PutCallParity' ]:
            self.__dict__[ i ] = None

        if volatility:
            self.volatility = float( volatility ) / 100

            self._a_ = self.volatility * self.daysToExpiration ** 0.5
            self._d1_ = (log( self.underlyingPrice / self.strikePrice ) + \
                         (self.interestRate - self.dividendYield + \
                          (self.volatility ** 2) / 2) * self.daysToExpiration) / \
                        self._a_
            self._d2_ = self._d1_ - self._a_
            if performance:
                [ self.CallPrice, self.PutPrice ] = self._price( )
            else:
                [ self.CallPrice, self.PutPrice ] = self._price( )
                [ self.CallDelta, self.PutDelta ] = self._delta( )
                [ self.CallDelta2, self.PutDelta2 ] = self._delta2( )
                [ self.CallTheta, self.PutTheta ] = self._theta( )
                [ self.CallRho, self.PutRho ] = self._rho( )
                self.vega = self._vega( )
                self.gamma = self._gamma( )
                self.exerciceProbability = norm.cdf( self._d2_ )
        if CallPrice:
            self.CallPrice = round( float( CallPrice ), 6 )
            self.impliedVolatility = implied_volatility( \
                self.__class__.__name__, args, self.CallPrice )
        if PutPrice and not CallPrice:
            self.PutPrice = round( float( PutPrice ), 6 )
            self.impliedVolatility = implied_volatility( \
                self.__class__.__name__, args, PutPrice=self.PutPrice )
        if CallPrice and PutPrice:
            self.CallPrice = float( CallPrice )
            self.PutPrice = float( PutPrice )
            self.PutCallParity = self._parity( )

    def _price( self ):
        '''Returns the option price: [Call price, Put price]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = max( 0.0, self.underlyingPrice - self.strikePrice )
            Put = max( 0.0, self.strikePrice - self.underlyingPrice )
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            Call = self.underlyingPrice * e ** (-self.dividendYield * \
                                                self.daysToExpiration) * norm.cdf( self._d1_ ) - \
                   self.strikePrice * e ** (-self.interestRate * \
                                            self.daysToExpiration) * norm.cdf( self._d2_ )
            Put = self.strikePrice * e ** (-self.interestRate * \
                                           self.daysToExpiration) * norm.cdf( -self._d2_ ) - \
                  self.underlyingPrice * e ** (-self.dividendYield * \
                                               self.daysToExpiration) * norm.cdf( -self._d1_ )
        return [ Call, Put ]

    def _delta( self ):
        '''Returns the option delta: [Call delta, Put delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = 1.0 if self.underlyingPrice > self.strikePrice else 0.0
            Put = -1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            _b_ = e ** (-self.dividendYield * self.daysToExpiration)
            Call = _b_ * norm.cdf( self._d1_ )
            Put = _b_ * (norm.cdf( self._d1_ ) - 1)
        return [ Call, Put ]

    # Verify
    def _delta2( self ):
        '''Returns the dual delta: [Call dual delta, Put dual delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = -1.0 if self.underlyingPrice > self.strikePrice else 0.0
            Put = 1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            _b_ = e ** -(self.interestRate * self.daysToExpiration)
            Call = -norm.cdf( self._d2_ ) * _b_
            Put = norm.cdf( -self._d2_ ) * _b_
        return [ Call, Put ]

    def _vega( self ):
        '''Returns the option vega'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            return 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            return self.underlyingPrice * e ** (-self.dividendYield * \
                                                self.daysToExpiration) * norm.pdf( self._d1_ ) * \
                   self.daysToExpiration ** 0.5 / 100

    def _theta( self ):
        '''Returns the option theta: [Call theta, Put theta]'''
        _b_ = e ** -(self.interestRate * self.daysToExpiration)
        _d_ = e ** (-self.dividendYield * self.daysToExpiration)
        Call = -self.underlyingPrice * _d_ * norm.pdf( self._d1_ ) * \
               self.volatility / (2 * self.daysToExpiration ** 0.5) + \
               self.dividendYield * self.underlyingPrice * _d_ * \
               norm.cdf( self._d1_ ) - self.interestRate * \
                                       self.strikePrice * _b_ * norm.cdf( self._d2_ )
        Put = -self.underlyingPrice * _d_ * norm.pdf( self._d1_ ) * \
              self.volatility / (2 * self.daysToExpiration ** 0.5) - \
              self.dividendYield * self.underlyingPrice * _d_ * \
              norm.cdf( -self._d1_ ) + self.interestRate * \
                                       self.strikePrice * _b_ * norm.cdf( -self._d2_ )
        return [ Call / 365, Put / 365 ]

    def _rho( self ):
        '''Returns the option rho: [Call rho, Put rho]'''
        _b_ = e ** -(self.interestRate * self.daysToExpiration)
        Call = self.strikePrice * self.daysToExpiration * _b_ * \
               norm.cdf( self._d2_ ) / 100
        Put = -self.strikePrice * self.daysToExpiration * _b_ * \
              norm.cdf( -self._d2_ ) / 100
        return [ Call, Put ]

    def _gamma( self ):
        '''Returns the option gamma'''
        return e ** (-self.dividendYield * self.daysToExpiration) * \
               norm.pdf( self._d1_ ) / (self.underlyingPrice * self._a_)

    # Verify
    def _parity( self ):
        '''Put-Call Parity'''
        return self.CallPrice - self.PutPrice - self.underlyingPrice + \
               (self.strikePrice / \
                ((1 + self.interestRate) ** self.daysToExpiration))

    def update( self, update_data ):
        '''use to accept parameter update from market'''
        self.__dict__.update( update_data )


class g_k:
    """Garman-Kohlhagen
	Used for pricing European options on currencies

	g_k([underlyingPrice, strikePrice, domesticRate, foreignRate, \
			daysToExpiration], volatility=x, CallPrice=y, PutPrice=z)

	eg:
		c = g_k([1.4565, 1.45, 1, 2, 30], volatility=20)
		c.CallPrice				# Returns the Call price
		c.PutPrice				# Returns the Put price
		c.CallDelta				# Returns the Call delta
		c.PutDelta				# Returns the Put delta
		c.CallDelta2			# Returns the Call dual delta
		c.PutDelta2				# Returns the Put dual delta
		c.CallTheta				# Returns the Call theta
		c.PutTheta				# Returns the Put theta
		c.CallRhoD				# Returns the Call domestic rho
		c.PutRhoD				# Returns the Put domestic rho
		c.CallRhoF				# Returns the Call foreign rho
		c.PutRhoF				# Returns the Call foreign rho
		c.vega					# Returns the option vega
		c.gamma					# Returns the option gamma

		c = g_k([1.4565, 1.45, 1, 2, 30], CallPrice=0.0359)
		c.impliedVolatility		# Returns the implied volatility from the Call price

		c = g_k([1.4565, 1.45, 1, 2, 30], PutPrice=0.03)
		c.impliedVolatility		# Returns the implied volatility from the Put price

		c = GK([1.4565, 1.45, 1, 2, 30], CallPrice=0.0359, PutPrice=0.03)
		c.PutCallParity			# Returns the Put-Call parity
	"""

    def __init__( self, args, volatility=None, CallPrice=None, PutPrice=None, \
                  performance=None ):
        self.underlyingPrice = float( args[ 0 ] )
        self.strikePrice = float( args[ 1 ] )
        self.domesticRate = float( args[ 2 ] ) / 100
        self.foreignRate = float( args[ 3 ] ) / 100
        self.daysToExpiration = float( args[ 4 ] ) / 365

        for i in [ 'CallPrice', 'PutPrice', 'CallDelta', 'PutDelta', \
                   'CallDelta2', 'PutDelta2', 'CallTheta', 'PutTheta', \
                   'CallRhoD', 'PutRhoD', 'CallRhoF', 'CallRhoF', 'vega', \
                   'gamma', 'impliedVolatility', 'PutCallParity' ]:
            self.__dict__[ i ] = None

        if volatility:
            self.volatility = float( volatility ) / 100

            self._a_ = self.volatility * self.daysToExpiration ** 0.5
            self._d1_ = (log( self.underlyingPrice / self.strikePrice ) + \
                         (self.domesticRate - self.foreignRate + \
                          (self.volatility ** 2) / 2) * self.daysToExpiration) / self._a_
            self._d2_ = self._d1_ - self._a_
            # Reduces performance overhead when comPuting implied volatility
            if performance:
                [ self.CallPrice, self.PutPrice ] = self._price( )
            else:
                [ self.CallPrice, self.PutPrice ] = self._price( )
                [ self.CallDelta, self.PutDelta ] = self._delta( )
                [ self.CallDelta2, self.PutDelta2 ] = self._delta2( )
                [ self.CallTheta, self.PutTheta ] = self._theta( )
                [ self.CallRhoD, self.PutRhoD ] = self._rhod( )
                [ self.CallRhoF, self.PutRhoF ] = self._rhof( )
                self.vega = self._vega( )
                self.gamma = self._gamma( )
                self.exerciceProbability = norm.cdf( self._d2_ )
        if CallPrice:
            self.CallPrice = round( float( CallPrice ), 6 )
            self.impliedVolatility = implied_volatility( \
                self.__class__.__name__, args, CallPrice=self.CallPrice )
        if PutPrice and not CallPrice:
            self.PutPrice = round( float( PutPrice ), 6 )
            self.impliedVolatility = implied_volatility( \
                self.__class__.__name__, args, PutPrice=self.PutPrice )
        if CallPrice and PutPrice:
            self.CallPrice = float( CallPrice )
            self.PutPrice = float( PutPrice )
            self.PutCallParity = self._parity( )

    def _price( self ):
        '''Returns the option price: [Call price, Put price]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = max( 0.0, self.underlyingPrice - self.strikePrice )
            Put = max( 0.0, self.strikePrice - self.underlyingPrice )
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            Call = e ** (-self.foreignRate * self.daysToExpiration) * \
                   self.underlyingPrice * norm.cdf( self._d1_ ) - \
                   e ** (-self.domesticRate * self.daysToExpiration) * \
                   self.strikePrice * norm.cdf( self._d2_ )
            Put = e ** (-self.domesticRate * self.daysToExpiration) * \
                  self.strikePrice * norm.cdf( -self._d2_ ) - \
                  e ** (-self.foreignRate * self.daysToExpiration) * \
                  self.underlyingPrice * norm.cdf( -self._d1_ )
        return [ Call, Put ]

    def _delta( self ):
        '''Returns the option delta: [Call delta, Put delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = 1.0 if self.underlyingPrice > self.strikePrice else 0.0
            Put = -1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            _b_ = e ** -(self.foreignRate * self.daysToExpiration)
            Call = norm.cdf( self._d1_ ) * _b_
            Put = -norm.cdf( -self._d1_ ) * _b_
        return [ Call, Put ]

    def _delta2( self ):
        '''Returns the dual delta: [Call dual delta, Put dual delta]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            Call = -1.0 if self.underlyingPrice > self.strikePrice else 0.0
            Put = 1.0 if self.underlyingPrice < self.strikePrice else 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            _b_ = e ** -(self.domesticRate * self.daysToExpiration)
            Call = -norm.cdf( self._d2_ ) * _b_
            Put = norm.cdf( -self._d2_ ) * _b_
        return [ Call, Put ]

    def _vega( self ):
        '''Returns the option vega'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            return 0.0
        if self.strikePrice == 0:
            raise ZeroDivisionError( 'The strike price cannot be zero' )
        else:
            return self.underlyingPrice * e ** -(self.foreignRate * \
                                                 self.daysToExpiration) * norm.pdf( self._d1_ ) * \
                   self.daysToExpiration ** 0.5

    def _theta( self ):
        '''Returns the option theta: [Call theta, Put theta]'''
        _b_ = e ** -(self.foreignRate * self.daysToExpiration)
        Call = -self.underlyingPrice * _b_ * norm.pdf( self._d1_ ) * \
               self.volatility / (2 * self.daysToExpiration ** 0.5) + \
               self.foreignRate * self.underlyingPrice * _b_ * \
               norm.cdf( self._d1_ ) - self.domesticRate * self.strikePrice * \
                                       _b_ * norm.cdf( self._d2_ )
        Put = -self.underlyingPrice * _b_ * norm.pdf( self._d1_ ) * \
              self.volatility / (2 * self.daysToExpiration ** 0.5) - \
              self.foreignRate * self.underlyingPrice * _b_ * \
              norm.cdf( -self._d1_ ) + self.domesticRate * self.strikePrice * \
                                       _b_ * norm.cdf( -self._d2_ )
        return [ Call / 365, Put / 365 ]

    def _rhod( self ):
        '''Returns the option domestic rho: [Call rho, Put rho]'''
        Call = self.strikePrice * self.daysToExpiration * \
               e ** (-self.domesticRate * self.daysToExpiration) * \
               norm.cdf( self._d2_ ) / 100
        Put = -self.strikePrice * self.daysToExpiration * \
              e ** (-self.domesticRate * self.daysToExpiration) * \
              norm.cdf( -self._d2_ ) / 100
        return [ Call, Put ]

    def _rhof( self ):
        '''Returns the option foreign rho: [Call rho, Put rho]'''
        Call = -self.underlyingPrice * self.daysToExpiration * \
               e ** (-self.foreignRate * self.daysToExpiration) * \
               norm.cdf( self._d1_ ) / 100
        Put = self.underlyingPrice * self.daysToExpiration * \
              e ** (-self.foreignRate * self.daysToExpiration) * \
              norm.cdf( -self._d1_ ) / 100
        return [ Call, Put ]

    def _gamma( self ):
        '''Returns the option gamma'''
        return (norm.pdf( self._d1_ ) * e ** -(self.foreignRate * \
                                               self.daysToExpiration)) / (self.underlyingPrice * self._a_)

    def _parity( self ):
        '''Returns the Put-Call parity'''
        return self.CallPrice - self.PutPrice - (self.underlyingPrice / \
                                                 ((1 + self.foreignRate) ** self.daysToExpiration)) + \
               (self.strikePrice / \
                ((1 + self.domesticRate) ** self.daysToExpiration))

    def update( self, update_data ):
        '''use to accept parameter update from market'''
        self.__dict__.update( update_data )
