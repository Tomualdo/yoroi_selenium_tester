# from pyvirtualdisplay import Display
from selenium import webdriver
import time
from datetime import datetime
import secrets
import binascii
import hashlib
import threading, os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bip39 import words as wordlist
# from yoroi import gen_wordlist as gw

# display = Display(visible=0, size=(1650,1200))
# display.start()


class BraveTest(threading.Thread):
    def __init__(self, web_page: str):
        self.web_page = web_page
        threading.Thread.__init__(self)

    def run(self):
        # self.web_page = web_page

        options = Options()
        options.add_argument
        options.binary_location = 'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\\brave.exe'
        options.add_extension('extension_4_7_300_0.crx')
        # options.add_argument("--headless")
        browser = webdriver.Chrome('chromedriver.exe', options = options)
        browser.get(self.web_page)
        browser.minimize_window()
        # time.sleep(3)

        #browser.switch_to.frame(browser.find_element_by_xpath('/html/body/jsl/div[2]/div/div[1]/iframe'))
        #element = browser.find_element_by_id('introAgreeButton')
        #element.click()

        # Yoroi continue
        """/html/body/div/div/div[2]/div/div/div/div/div/div[2]/div/button"""
        # Checkbox

        browser.implicitly_wait(100)
        browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div/div/div[2]/div/button').click()
        browser.find_element_by_class_name('SimpleCheckbox_check').click()
        browser.find_element_by_class_name('TermsOfUseForm_submitButton').click()
        browser.find_element_by_class_name('UriPromptForm_submitButton').click()
        # time.sleep(5)
        # browser.find_element_by_class_name('finishButton').click()
        # OK
        browser.find_element_by_class_name('MainCards_bgRestoreWallet').click()
        """<button type="button" class="OptionBlock_optionSubmitButton PickCurrencyOptionDialog_cardano"><div class="OptionBlock_optionImage OptionBlock_cardano"></div><div class="OptionBlock_optionTitle">Cardano</div></button>"""
        browser.find_element_by_class_name('OptionBlock_cardano').click()
        """<button type="button" class="OptionBlock_optionSubmitButton WalletRestoreOptionDialog_restoreNormalWallet"><div class="OptionBlock_optionImage OptionBlock_restoreNormalWallet"></div><div class="OptionBlock_optionTitle">Enter a 15-word recovery phrase</div></button>"""
        browser.find_element_by_class_name('OptionBlock_restoreNormalWallet').click()
        """<button type="button" class="OptionBlock_optionSubmitButton WalletEraOptionDialog_bgShelleyMainnet"><div class="OptionBlock_optionImage OptionBlock_bgShelleyMainnet"></div><div class="OptionBlock_optionTitle">Shelley-era wallet</div></button>"""
        browser.find_element_by_class_name('OptionBlock_bgShelleyMainnet').click()
        # table area
        self.seed, self.entrophy = self.gen_wordlist(160)
        """<input class="SimpleInput_input InputOverrides_input InputOwnSkin_icon" id="walletName--2" name="walletName" type="text" label="Wallet name" placeholder="" required="" value="">"""
        # wallet_name = browser.find_element_by_class_name('SimpleInput_input')
        wallet_name = browser.find_element_by_id('walletName--2')
        wallet_name.send_keys(str(self.entrophy[:10]))

        recovery_phrase = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[2]/div[1]/fieldset/div[2]/div/input')
        # browser.find
        # recovery_phrase.send_keys('seed')
        recovery_phrase.click()
        recovery_phrase.send_keys(" \n".join(self.seed))
        recovery_phrase.send_keys("\n")
            
        """<input class="SimpleInput_input InputOverrides_input InputOwnSkin_icon" id="walletPassword--5" name="walletPassword" type="password" label="New spending password" placeholder="" required="" value="">"""
        pwd = browser.find_element_by_id('walletPassword--5')
        pwd.send_keys('qwertyqwerty')

        """<input class="SimpleInput_input InputOverrides_input InputOwnSkin_icon" id="repeatPassword--6" name="repeatPassword" type="password" label="Repeat new spending password" placeholder="" required="" value="">"""
        pwd = browser.find_element_by_id('repeatPassword--6')
        pwd.send_keys('qwertyqwerty')

        """<button class="primary SimpleButton_root ButtonOverrides_root" label="Restore wallet">Restore wallet</button>"""
        browser.find_element_by_class_name('ButtonOverrides_root').click()

        """/html/body/div[2]/div/div/div/div[3]/button[2]"""
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[3]/button[2]').click()
        # get value
        """<p class="UserSummary_value"><span>0<span class="UserSummary_decimal">.000000 </span> </span>ADA</p>"""
        """<div class="UserSummary_cardContent"><div><h3 class="UserSummary_label">Total ADA:</h3><p class="UserSummary_value"><span>0<span class="UserSummary_decimal">.000000 </span> </span>ADA</p></div><div class="UserSummary_amountNote">This balance includes rewards (withdrawal required to be able to send this full amount)</div></div>"""

        """/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span/span"""
        """/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span"""
        ada_decimal = browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span/span')
        ada_val =  browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div[1]/p/span')
        attr = ada_decimal.get_attribute('innerHTML')
        attr1 = ada_val.get_attribute('innerHTML')
        attr1 = attr1.split('<')
        self.total_ada = float(attr1[0]+attr)
        print(self.total_ada)
        if self.total_ada != 0:
            exit()
        self.save_wallet()
        # ada = ada_value.get_attribute('UserSummary_value')
        # print(ada_value)
        # print(ada)

        """<button type="button" class="NavBarBack_backButton"><span class="NavBarBack_backIcon"><svg width="12" height="12" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg"><path d="M8.5 1l-5 5 5 5" stroke="#8A92A3" stroke-width="0.833" fill="none" fill-rule="evenodd" opacity="0.85"></path></svg></span>Back to my wallets</button>"""
        browser.find_element_by_class_name('NavBarBack_backButton').click()
        """<div class="WalletRow_settingSection"><button type="button" class="WalletRow_settingButton"><svg div>"""
        """"""
        browser.find_element_by_class_name('WalletRow_settingSection').click()
        """<button class="primary RemoveWallet_submitButton removeWallet SimpleButton_root ButtonOverrides_root DangerousButton_root" label="Remove 7904380c71">Remove 7904380c71</button>"""
        browser.find_element_by_class_name('RemoveWallet_submitButton').click()
        """<div class="SimpleCheckbox_check CheckboxOverrides_check"></div>"""
        browser.find_element_by_class_name('SimpleCheckbox_check').click()
        """<button class="confirmButton primary SimpleButton_root ButtonOverrides_root DangerousButton_root" label="Remove">Remove</button>"""
        browser.find_element_by_class_name('confirmButton').click()
        ################################# wallet deleted ##################################
        while True:
            try:
                """<div class="MainCards_heroCardsItemBg MainCards_bgRestoreWallet"></div>"""
                browser.find_element_by_class_name('MainCards_bgRestoreWallet').click()
                """<button type="button" class="OptionBlock_optionSubmitButton PickCurrencyOptionDialog_cardano"><div class="OptionBlock_optionImage OptionBlock_cardano"></div><div class="OptionBlock_optionTitle">Cardano</div></button>"""
                browser.find_element_by_class_name('OptionBlock_cardano').click()
                browser.find_element_by_class_name('OptionBlock_restoreNormalWallet').click()
                browser.find_element_by_class_name('OptionBlock_bgShelleyMainnet').click()
                # table area
                self.seed, self.entrophy = self.gen_wordlist(160)
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
                browser.find_element_by_class_name('NavBarBack_backButton').click()
                browser.find_element_by_class_name('WalletRow_settingSection').click()
                browser.find_element_by_class_name('RemoveWallet_submitButton').click()
                browser.find_element_by_class_name('SimpleCheckbox_check').click()
                browser.find_element_by_class_name('confirmButton').click()
            except KeyboardInterrupt:
                break




        # time.sleep(5000)

        # try:
        #     browser.switch_to_default_content()
        #     browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0])
        #     browser.implicitly_wait(1)
        #     browser.find_element_by_id('introAgreeButton').click()
        #     browser.switch_to.default_content()
        # except:
        #     pass

        

        # browser.save_screenshot('_sele.png')
        browser.quit()

        # display.stop()
    def save_wallet(self):
        with open("wallets.txt", "a") as file1:
        # Writing data to a file
            tim = datetime.now().strftime('%d.%m.%y %H:%M:%S')
            filedata = f"{tim} {str(self.total_ada)}ADA {str(self.seed)} {self.entrophy}"
            file1.write(filedata)
            file1.write("\n")

    def gen_wordlist(self, bits):
        """Generuj seed na test bruteforce BIP39"""
        self.bits = bits
        s = bin(secrets.randbits(self.bits))
        s = s[2:].zfill(self.bits)
        print(f"Binary: {s}")
        h=int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
        entrophy = binascii.hexlify(h).decode()
        print(f"Entrophy: {entrophy}")
        a = binascii.hexlify(hashlib.sha256(h).digest()).decode()
        print(f"SHA256 of Entrophy: {a}")
        s_ = s
        # extract first x bits from sha256 hash
        # if bits == 160 :
        #     s_+=bin(int(a[:BITS//128]<<1,16))[2:].zfill(BITS//32)
        #     print(f"checksum = {bin(int(a[:BITS//128]<<1,16))[2:].zfill(BITS//32)}")
        # else:
        chsum = int(a[:2],16) # convert string to int and cut desired length
        chsum = bin(chsum)[2:].zfill(8) # convert to bits and fill desired length with zeroes
        chsum = chsum[:self.bits//32] # trim
        s_ += chsum
        print(f"checksum = {chsum}")
        # separate each 11 bits of entrophy to generate coresponding words
        seed = []
        for x,i in enumerate(range(0,len(s_),11)):
            # print(f"{int(s_[i:i+11],2)} = {k.words[int(s_[i:i+11],2)]}")
            seed.append(wordlist[int(s_[i:i+11],2)])
        # print(seed)
        # print(" ".join(seed))
        # seed = ''.join(seed)
        print(seed)
        return seed, entrophy

a = BraveTest('chrome-extension://ffnbelfdoeiohenkjibnmadjiehjhajb/main_window.html#/my-wallets')
a.start()
# b = BraveTest('https://www.google.com/maps/dir/')

# threads = []
# try:
#     for i in range(os.cpu_count()):
#         print(f"thread {i}")
#         threads.append(BraveTest('chrome-extension://ffnbelfdoeiohenkjibnmadjiehjhajb/main_window.html#/profile/language-selection'))
#         print(f"running {i} thread")

#     for thread in threads:
#         thread.start()
# except KeyboardInterrupt:
#     for thread in threads:
#         thread.join()
#         exit()
# for thread in threads:
#     thread.join()