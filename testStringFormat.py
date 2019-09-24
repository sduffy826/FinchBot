def removeLeadingTrailingChar(string2Check,character):
  newString = string2Check
  strLen    = len(newString)
  print("In removeLeadingTrailingChar with {0} len:{1}, character is:{2}".format(newString,strLen,character))

  if newString[0] == character:
    newString = newString[1:strLen]
    strLen -= 1
  if newString[strLen-1] == character:
    newString = newString[0:strLen-1]
  return newString

quantity = 3
itemno = 567
price = 49
myorder = "I want {} pieces of item number {} for {:.2f} dollars."
print(myorder.format(quantity, itemno, price))

print("\nExample with using index (and duplicating values)")
person = "Sean"
age = 2932
print("{0} is {1} years old, but {0} doesn't act it".format(person,age))


print("\nExample with using named references, note they have to be named, can't use variables")
print("In example below the :,.f means comma as thousands separator, 1 decimal place in floating format")
print("{person} is {personAge:,.1f} years old, that's {personAge:X} hex".format(person=person,personAge=age))

print("Below is integer format (not sure why they call it decimal)")
print("{person} is {personAge:,d} years old, that's {personAge:X} hex".format(person=person,personAge=age))

string2Test = "(This,is,a,string,version,of,a,tuple)"
aString = removeLeadingTrailingChar(removeLeadingTrailingChar(string2Test,"("),")")
print("astring is:{0}:".format(aString))
print("Using strip('()') is:{0}:".format(string2Test.strip("()")))
