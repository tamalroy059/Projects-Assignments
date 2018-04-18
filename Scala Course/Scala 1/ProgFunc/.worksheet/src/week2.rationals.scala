package week2

object rationals {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(61); 
  val x = new Rational(1,3);System.out.println("""x  : week2.Rational = """ + $show(x ));$skip(10); val res$0 = 
  x.numer;System.out.println("""res0: Int = """ + $show(res$0));$skip(10); val res$1 = 
  x.denom;System.out.println("""res1: Int = """ + $show(res$1));$skip(31); 
  
  val y = new Rational(5,7);System.out.println("""y  : week2.Rational = """ + $show(y ));$skip(20); val res$2 = 
  x.add(y).toString;System.out.println("""res2: String = """ + $show(res$2));$skip(31); 
  
  val z = new Rational(3,2);System.out.println("""z  : week2.Rational = """ + $show(z ));$skip(21); val res$3 = 
  
  x.sub(y).sub(z);System.out.println("""res3: week2.Rational = """ + $show(res$3));$skip(11); val res$4 = 
  y.add(y);System.out.println("""res4: week2.Rational = """ + $show(res$4));$skip(6); val res$5 = 
  x<y;System.out.println("""res5: Boolean = """ + $show(res$5));$skip(10); val res$6 = 
  x max y;System.out.println("""res6: week2.Rational = """ + $show(res$6));$skip(37); 
  
  val strange = new Rational(1,1);System.out.println("""strange  : week2.Rational = """ + $show(strange ));$skip(17); val res$7 = 
  x.add(strange);System.out.println("""res7: week2.Rational = """ + $show(res$7));$skip(33); val res$8 = 
  
  
  	new Rational(1,2).numer;System.out.println("""res8: Int = """ + $show(res$8))}
  	
  	
  	
  	
  
  
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
