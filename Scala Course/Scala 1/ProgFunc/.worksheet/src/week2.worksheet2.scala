package week2
import math.abs


object worksheet2 {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(85); 
  println("Fixed Point Function");$skip(28); 
  
  val tolerance = 0.0001;System.out.println("""tolerance  : Double = """ + $show(tolerance ));$skip(71); 
  def isCloseEnough(x:Double, y:Double) =
  		abs((x-y)/x)/x<tolerance;System.out.println("""isCloseEnough: (x: Double, y: Double)Boolean""");$skip(266); 
  		
  	def fixedPoint(f:Double => Double)(FirstGuess: Double) = {
  		def iterate(guess:Double):Double = {
  			println("guess = " + guess)
  			val next = f(guess)
  			if (isCloseEnough(guess,next)) next
  			else iterate(next)
  		}
  		iterate(FirstGuess)
  	};System.out.println("""fixedPoint: (f: Double => Double)(FirstGuess: Double)Double""");$skip(35); val res$0 = 
  	
  	
  	fixedPoint(x=>1+x/2)(1);System.out.println("""res0: Double = """ + $show(res$0));$skip(93); 
  	
  		
  	
  	
  	
  	
  	
  	def averageDamp(f:Double => Double)(x:Double) = (x + f(x))/2;System.out.println("""averageDamp: (f: Double => Double)(x: Double)Double""");$skip(70); 
  	
  		def sqrt(x: Double)=
  		fixedPoint(averageDamp(y=>x/y))(1.0);System.out.println("""sqrt: (x: Double)Double""");$skip(16); val res$1 = 
  		
  	sqrt(2);System.out.println("""res1: Double = """ + $show(res$1))}
  	
}
