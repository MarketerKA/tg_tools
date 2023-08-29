
def install_requirements():
    import subprocess

    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

def configure_data():
    print("Your API ID : ")
    api_id = input()

    print("Your API HASH : ")
    api_hash = input()

    print("Your Phone Number : ")
    phone_number = input()

    print("Enter the text to be sent. Twice press Enter to finish")
    text = ''
    sentinel = ''  # ends when this string is seen
    for line in iter(input, sentinel):
        text+= f'{line}\delpop'

    with open('config.py', 'w') as f:
        f.write(f"api_id = '{api_id}'\n")
        f.write(f"api_hash = '{api_hash}'\n")
        f.write(f"phone_number = '{phone_number}'\n")
        f.write(f"text = '{text}'\n")

if __name__ == '__main__':
    install_requirements()
    configure_data()