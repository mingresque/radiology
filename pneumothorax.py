#@title Pneumothorax { vertical-output: true, display-mode: "form" }
def pneumothorax(values:str):
  
  array = values.split()
  while len(array) < 3:
    array += [0]
  a, b, c=list(map(float, array))
  formula = round(4.2 + (4.7 * (a+b+c)),1)
  text = f'## 4.2 + [4.7 * ({a} + {b} + {c})] = {formula}'
  
  print(text + '\n' + \
        f"There is {formula}% pneumothorax (using the Collins method).")
  
  return ''

pneumothorax('0.7')
