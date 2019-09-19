`object` = singleton

## Imports
`import java.util.{Date, Locale}` curly braces to import multiple classes
To import all the names use `_` instead of `*`

`val` = immutable
`var` = mutable



## For loops
```
    for(i <- 0 until limit){}
    for(item : Item <- List[Item])
```
##  Type casting
```
    val x: Long = 1252323
    val y: Float = x
```
Casting is _unidirectional_, you can't cast a value back after casting it.

`Nothing` = Subtype of all types used for non-termination e.g. thrown exception, program exit or infinite loop
`Null` = Subtype for all refence types.

## Tuples
Tuples are immutable

Can be accessed using `._1` or `._2` or with pattern matching `val (name, ingredient) = ingredient`


# Classes
If function do not have any arguments, we can omit the parenthesis to allow is being called like a field
```
    def re() = real 
to
    def re = real
```

Class members are public by default, explicitely use `private` otherwise.


## Case classes
Like in Haskell `Tree  = Node Int Tree Tree | Leaf Int`
* No `new` keyword is needed to create instances
* Getter functions auto defined
* Pattern matching

*Type* = alias in Haskell e.g. `type Environment = String => Int`
*Guards*: `case Var(n) if(v == n) => Const(1)`

## Class composition using Mixins
Mixins allow multiple inheritance. 
It uses the following syntax: `class RichStringIter extends StringIterator with RichIterator` where `RichIterator` is the Mixin class.  _the child class can still inherit all the features of the parent class, but, the semantics about the child "being a kind of" the parent need not be necessarily applied._. So it is not a subtype but merely adds its set of methods into another object.

## Defaults
Use `_` for default value, 0 for numeric types, `false` for boolean, `()`  for `Unit type` and `null` for all others


# Traits
Like Java interfaces, you can also add a default implementation

# Generics
`class Reference[T]`

# Lists
Normal Lists are immutable, use `ArrayBuffer[T]` or `ListBuffer[T]`
Add to list: `list += item`

