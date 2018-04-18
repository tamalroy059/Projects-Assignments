package week1

object worksheet1 {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(40); val res$0 = 
  1+2;System.out.println("""res0: Int(3) = """ + $show(res$0));$skip(49); 
  def abs(x:Double): Double = if (x<0) -x else x;System.out.println("""abs: (x: Double)Double""");$skip(329); 
  
  def sqrt(x:Double) = {
  
	  def sqrtIter(guess: Double): Double =
	  		if (isGoodEnough(guess)) guess
	  		else sqrtIter(improve(guess))
	  
	  def isGoodEnough(guess: Double): Boolean =
	  		abs(guess * guess - x)/x <0.001
	  		
	  	def improve(guess:Double): Double =
	  		(guess + x/guess)/2
	  		
	  	sqrtIter(1.0)
  };System.out.println("""sqrt: (x: Double)Double""");$skip(19); val res$1 = 
  
  
  
  sqrt(4);System.out.println("""res1: Double = """ + $show(res$1));$skip(65); 
  
  
  def gcd(a:Int, b:Int): Int = if (b==0) a else gcd(b,a%b);System.out.println("""gcd: (a: Int, b: Int)Int""");$skip(16); val res$2 = 
  
  gcd(14,21);System.out.println("""res2: Int = """ + $show(res$2));$skip(67); 
	
	def factorial(n:Int): Int = if (n==0) 1 else n * factorial(n-1);System.out.println("""factorial: (n: Int)Int""");$skip(17); val res$3 = 
	
	factorial(24);System.out.println("""res3: Int = """ + $show(res$3));$skip(160); 
	
	
	def pascal(c: Int, r: Int): Int = {
      
      if (c==0 && r==0) 1
      else if (c>r || c<0 ) 0
      else pascal(c-1,r-1) + pascal(c,r-1)
      
    };System.out.println("""pascal: (c: Int, r: Int)Int""");$skip(20); val res$4 = 
    
   pascal(1,3);System.out.println("""res4: Int = """ + $show(res$4));$skip(410); 
	
	def balance(chars: List[Char]): Boolean = {
        def positionCount(position: Int, result: Int):Int = {
            if (position<0) result
            else if (chars(position)=='(') positionCount(position-1,result+1)
            else if (chars(position)==')') positionCount(position-1,result-1)
            else positionCount(position-1,result)
        }
        positionCount(chars.length-1, 0)==0
    };System.out.println("""balance: (chars: List[Char])Boolean""");$skip(296); 
	
	
	def countChange(money: Int, coins: List[Int]): Int = {
      def loop(money: Int, coins: List[Int]): Int = {
        if (money<0 || coins.isEmpty) 0
        else if (money==0) 1
        else loop(money, coins.tail) + loop(money - coins.head, coins)
        }
      loop(money,coins)
      };System.out.println("""countChange: (money: Int, coins: List[Int])Int""");$skip(39); val res$5 = 
    
    
    countChange(3,List(1,2));System.out.println("""res5: Int = """ + $show(res$5))}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}
