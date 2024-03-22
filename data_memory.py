word_lenght = 32
size = 50

data_memory = {hex(i): bin(0).zfill(word_lenght)[:word_lenght - 2]  for i in range(size)}

