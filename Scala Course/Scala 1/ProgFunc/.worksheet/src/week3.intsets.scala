package week3

object intsets {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(75); 
  println("Welcome to the Scala worksheet");$skip(48); 
  val t1 =new NonEmpty(3, new Empty, new Empty);System.out.println("""t1  : week3.NonEmpty = """ + $show(t1 ));$skip(21); 
  val t2 = t1 incl 4;System.out.println("""t2  : week3.IntSet = """ + $show(t2 ))}
  
  
  
    
}

abstract class IntSet {
	def incl(x:Int): IntSet
	def contains(x: Int): Boolean
}


class Empty extends IntSet {
	def contains(x:Int):Boolean = false
	def incl(x:Int): IntSet = new NonEmpty(x, new Empty, new Empty)
	override def toString = "."
}


class NonEmpty(elem: Int, Left: IntSet, Right: IntSet) extends IntSet{
	
	def contains(x:Int) =
		if (x<elem) Left contains x
		else if (x>elem) Right contains x
		else true
		
	def incl(x:Int): IntSet =
		if (x<elem) new NonEmpty(elem, Left incl x, Right)
		else if (x>elem) new NonEmpty(elem, Left, Right incl x)
		else this
	
	override def toString = "{" + Left + elem + Right + "}"
	
}


abstract class Base {
	def foo =1
	def bar: Int
}

class Sub extends Base {
	override def foo =2
	def bar = 3
}
