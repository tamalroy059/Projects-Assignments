package week2

object rationals {
  val x = new Rational(1,3)                       //> x  : week2.Rational = 1/3
  x.numer                                         //> res0: Int = 1
  x.denom                                         //> res1: Int = 3
  
  val y = new Rational(5,7)                       //> y  : week2.Rational = 5/7
  x.add(y).toString                               //> res2: String = 22/21
  
  val z = new Rational(3,2)                       //> z  : week2.Rational = 3/2
  
  x.sub(y).sub(z)                                 //> res3: week2.Rational = -79/42
  y.add(y)                                        //> res4: week2.Rational = 10/7
  x<y                                             //> res5: Boolean = true
  x max y                                         //> res6: week2.Rational = 5/7
  
  val strange = new Rational(1,1)                 //> strange  : week2.Rational = 1/1
  x.add(strange)                                  //> res7: week2.Rational = 4/3
  
  
  	new Rational(1,2).numer                   //> res8: Int = 1
  	
  	
  	
  	
  
  
}



class Rational(x: Int, y:Int) {
	require(y !=0, "denominator must be non zero")
	
	def this(x:Int) = this(x,1)
	private def gcd(a:Int, b:Int): Int = if (b==0) a else gcd(b,a%b)
	private val g = gcd(x,y)
	
	def numer=x/g
	def denom =y/g
	
	def <(that:Rational) = this.numer*that.denom < that.numer*this.denom
	
	def max(that: Rational) = if (this < that) that else this
	def add(that: Rational): Rational =




	new Rational(
		numer * that.denom + that.numer * denom,
		denom * that.denom
	)
	
	def unary_- : Rational = new Rational(-numer, denom)
	
	def sub(that:Rational) = add(-that)
	
	override def toString =
		numer + "/" + denom
		
}