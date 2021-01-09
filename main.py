# -----------------------------------------------------------------------
# ---------------------------- TINDER BOT APP ---------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_driver_path = r'chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_driver_path)

TINDER_URL = "http://www.tinder.com"

FACEBOOK_EMAIL = "XXXXXXXXXXXXXXXXXXXX"
FACEBOOK_PWD = "XXXXXXXX"


def wait_for_render():
    time.sleep(3)
# Wait for webpage to render


def convert_to_super_like(driver_x):
    """Upgrades like to a super like"""
    wait_for_render()
    try:
        super_like_text = driver_x.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[4]/h3")
        # print(super_like_text)
        if super_like_text.text == "Upgrade your like!":
            super_like_available = True
    except:
        super_like_available = False
    if super_like_available:
        super_like = driver_x.find_element_by_xpath("//*[@id=\"modal-manager\"]/div/div/button[1]")
        super_like.click()
        time.sleep(2)
        try:
            tinder_plus_text = driver_x.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[1]/div[1]/h3")
            tinder_plus_pop_up = True
        except:
            tinder_plus_pop_up = False
        if tinder_plus_pop_up:
            no_thanks_button = driver_x.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[3]/button[2]")
            no_thanks_button.click()


def process_tinder_home_screen_pop_up(driver_x):
    wait_for_render()
    try:
        add_to_home_screen_text = driver_x.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[1]/div[2]/h3").text
        if add_to_home_screen_text == "Add Tinder to your home screen":
            not_interested_button = driver_x.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[2]/button[2]")
            not_interested_button.click()
            return True
    except:
        return False
        pass

def process_matches_pop_up(driver_x):
    wait_for_render()
    try:
        close_button = driver_x.find_element_by_xpath("//*[@title='Back to Tinder']")
        close_button.click()
    except:
        pass

def swipe_right(driver_x):
    """Performs a right swipe"""
    wait_for_render()
    right_swipe = driver_x.find_element_by_xpath("//*[@id='content']/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button")
    right_swipe.click()
    try:
        convert_to_super_like(driver_x)
    finally:
        pass
    process_matches_pop_up(driver_x)


def swipe_left(driver_x):
    """Performs a left swipe"""
    wait_for_render()
    left_swipe = driver_x.find_element_by_xpath("//*[@id='content']/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button")
    left_swipe.click()


def evaluate_profile(driver_x):
    """This function would be used to evaluate prospective matches"""
    return True

driver.get(TINDER_URL)

wait_for_render()

# Set Base Window
base_window = driver.window_handles[0]

# Deal with Privacy marketing pop up
marketing_accept_button = driver.find_element_by_xpath("//*[@id=\"content\"]/div/div[2]/div/div/div[1]/button")
marketing_accept_button.click()

wait_for_render()
# Click Login Button
login_button = driver.find_element_by_xpath("//*[@id=\"content\"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button")
login_button.click()

wait_for_render()
# Login Via Facebook
fb_login_button = driver.find_element_by_xpath("//*[@aria-label='Login with Facebook']")
# fb_login_button = driver.find_element_by_xpath("//*[@id=\"modal-manager\"]/div/div/div[1]/div/div[3]/span/div[2]/button")
fb_login_button.click()

wait_for_render()

#Set FB Login Window
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)

if driver.title == "Facebook":
    # Enter Facebook Login Details
    fb_email_entry = driver.find_element_by_id("email")
    fb_email_entry.send_keys(FACEBOOK_EMAIL)
    fb_pwd_entry = driver.find_element_by_id("pass")
    fb_pwd_entry.send_keys(FACEBOOK_PWD)
    fb_login_button = driver.find_element_by_id("loginbutton")
    fb_login_button.click()
    # Switch back to base window
    driver.switch_to.window(base_window)
    wait_for_render()
    wait_for_render()
    # -----------------------------------------------------------------------------------------------
    # Navigate Pop Up Boxes
    # -----------------------------------------------------------------------------------------------
    # Share your location | Allow
    # share_location_allow_button = driver.find_element_by_xpath("//*[@aria-label='Allow']")
    try:
        share_location_allow_button = driver.find_element_by_xpath("//*[@id=\"modal-manager\"]/div/div/div/div/div[3]/button[1]")
        share_location_allow_button.click()
    finally:
        pass
    wait_for_render()
    wait_for_render()

    try:
         notifications_enable_button = driver.find_element_by_xpath("//*[@id=\"modal-manager\"]/div/div/div/div/div[3]/button[2]")
         notifications_enable_button.click()
    finally:
        pass
    # -----------------------------------------------------------------------------------------------
    # Let the swipe animation happen
    wait_for_render()
    time.sleep(5)
    # driver.switch_to.window(base_window)
    # Swipe like a maniac -- Where dem girls at?!
    Swipe_Available = True
    while Swipe_Available:
        try:
            # This function evaluates a prospective match, returns true if good and false if bad
            profile_outcome = evaluate_profile(driver)
            if profile_outcome:
                swipe_right(driver)

            else:
                swipe_left(driver)
        except:
            # Handle Additional pop-ups
            exit_loop = not process_tinder_home_screen_pop_up(driver)
            print(f"exit_loop: {exit_loop}")
            if exit_loop:
                # Run out of swipes
                Swipe_Available = False
        finally:
            pass



