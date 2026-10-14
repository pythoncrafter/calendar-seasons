"""Small OpenStep parser for structural validation; not an Apple compiler."""
import re
def loads(text):
 text=re.sub(r'/\*.*?\*/','',text,flags=re.S);text=re.sub(r'//[^\n]*','',text)
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|[{}()=;,]|[^\s{}()=;,]+',text);i=0
 def take(expected=None):
  nonlocal i
  assert i<len(tokens),'Unexpected end'
  item=tokens[i];i+=1
  if expected:assert item==expected,(expected,item)
  return item
 def parse():
  item=take()
  if item=='{':
   result={}
   while tokens[i]!='}':
    key=take().strip('"');take('=');v=parse();take(';');assert key not in result;result[key]=v
   take('}');return result
  if item=='(':
   result=[]
   while tokens[i]!=')':
    result.append(parse())
    if tokens[i]!=')':take(',')
   take(')');return result
  return item.strip('"')
 result=parse();assert i==len(tokens);return result
