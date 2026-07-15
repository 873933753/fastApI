def get_full_name(first_name, last_name):
    full_name = first_name + ' ' + last_name
    # title() 方法将每个单词的首字母大写
    return full_name.title()

print(get_full_name('hanber', 'tang')) # Hanber Tang
print(get_full_name('hanber', '1')) # Hanber 1

def get_full_name_str(first_name:str, last_name:str):
  full_name = first_name + ' ' + last_name
  return full_name.title()

print(get_full_name_str('hanber', '1')) # Hanber Tang
