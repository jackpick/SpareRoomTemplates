from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ProfessionalURLS = []
ProfessionalNewURLs = []

StudentURLS = []
StudentNewURLs = []

# Copy username from txt file
with open('Username.txt', 'r') as file:
    Username = file.read().rstrip('\n')

# Copy password from txt file
with open('Password.txt', 'r') as file:
    Password = file.read().rstrip('\n')

# Copy professional template from txt file
with open('Professional_Template.txt', 'r') as file:
    ProfessionalTemplate = file.read().rstrip('\n')

# Copy student template from txt file
with open('Student_Template.txt', 'r') as file:
    StudentTemplate = file.read().rstrip('\n')

# Create a new instance of the Chrome driver
driver = webdriver.Edge()

# Open the SpareRoom website
driver.get("https://www.spareroom.co.uk/")

# Press accept cookies button
cookiesButton = driver.find_element(By.ID, "onetrust-accept-btn-handler")
cookiesButton.click()

# Press login button
loginButton = driver.find_element(By.ID, "loginButtonNav")
loginButton.click()

# Put in username
usernameBox = driver.find_element(By.ID, "loginemail")
usernameBox.clear()
usernameBox.send_keys(Username)

# Put in password
passwordBox = driver.find_element(By.ID, "loginpass")
passwordBox.clear()
passwordBox.send_keys(Password, Keys.RETURN)

# Search for rooms wanted in LS6
time.sleep(5)
driver.get("https://www.spareroom.co.uk/flatmate/flatmates.pl?search_id=1387512595&mode=list")

# Loop through each page until next page token can't be found (final page)
while True:
    try:
        # Get next page link
        nextPage = driver.find_element(By.ID, "paginationNextPageLink")
        nextPageLink = nextPage.get_attribute("href")

        # Get listing results
        Listings = driver.find_elements(By.CLASS_NAME, "listing-result")

        # Iterate through listings
        for Listing in Listings:
            # Find if they are professional or student
            ProfessionalOrStudent = Listing.find_element(By.CLASS_NAME,'advertiser-info__role')
            ProfessionalOrStudentText = ProfessionalOrStudent.text
            # Find if they are contacted
            ContactedOrNot = Listing.find_element(By.CLASS_NAME,'button__text')
            ContactedOrNotText = ContactedOrNot.text
            if ContactedOrNotText == "Save":
                if "Couple" not in ProfessionalOrStudentText:
                    # Find webpage
                    article = Listing.find_element(By.TAG_NAME,'article')
                    a = article.find_element(By.TAG_NAME,'a')
                    Webpage = a.get_attribute("href")
                    # Separate into professional and student lists
                    if "Student" in ProfessionalOrStudentText:
                        StudentURLS.append(Webpage)
                    else:
                        ProfessionalURLS.append(Webpage)
        driver.get(nextPageLink)
    except: 
        # Get listing results
        Listings = driver.find_elements(By.CLASS_NAME, "listing-result")

        # Iterate through listings
        for Listing in Listings:
            # Find if they are professional or student
            ProfessionalOrStudent = Listing.find_element(By.CLASS_NAME,'advertiser-info__role')
            ProfessionalOrStudentText = ProfessionalOrStudent.text
            # Find if they are contacted
            ContactedOrNot = Listing.find_element(By.CLASS_NAME,'button__text')
            ContactedOrNotText = ContactedOrNot.text
            if ContactedOrNotText == "Save":
                if "Couple" not in ProfessionalOrStudentText:
                    # Find webpage
                    article = Listing.find_element(By.TAG_NAME,'article')
                    a = article.find_element(By.TAG_NAME,'a')
                    Webpage = a.get_attribute("href")
                    # Separate into professional and student lists
                    if "Student" in ProfessionalOrStudentText:
                        StudentURLS.append(Webpage)
                    else:
                        ProfessionalURLS.append(Webpage)
        # Stop looping through
        break
    
# Iterate through webpages found in student listings
for URL in StudentURLS:
    # Go to webpage
    driver.get(URL)
    # Find messagebox URL
    listingContactBody = driver.find_element(By.CLASS_NAME, "listing-contact__body")
    listingContact = listingContactBody.find_element(By.CLASS_NAME, "listing-contact__contact-buttons")
    contactMethods = listingContact.find_element(By.CLASS_NAME, "contact_methods")
    emailAdvertiser = contactMethods.find_element(By.TAG_NAME, "li")
    messageButton = emailAdvertiser.find_element(By.TAG_NAME, "a")
    messageWebpage = messageButton.get_attribute("href")
    StudentNewURLs.append(messageWebpage)

# Iterate through webpages found in professional listings
for URL in ProfessionalURLS:
    # Go to webpage
    driver.get(URL)
    # Find messagebox URL
    listingContactBody = driver.find_element(By.CLASS_NAME, "listing-contact__body")
    listingContact = listingContactBody.find_element(By.CLASS_NAME, "listing-contact__contact-buttons")
    contactMethods = listingContact.find_element(By.CLASS_NAME, "contact_methods")
    emailAdvertiser = contactMethods.find_element(By.TAG_NAME, "li")
    messageButton = emailAdvertiser.find_element(By.TAG_NAME, "a")
    messageWebpage = messageButton.get_attribute("href")
    ProfessionalNewURLs.append(messageWebpage)

# Iterate through message webpages found on each student webpage
for newURL in StudentNewURLs:
    # Go to webpage
    driver.get(newURL)
    # Find messagebox
    messageBox = driver.find_element(By.ID, "message")
    # Input text
    messageBox.send_keys(StudentTemplate)
    # Click submit
    submitButton = driver.find_element(By.XPATH, "//button[@class='button button--large button--wide']")
    submitButton.click()

# Iterate through message webpages found on each professional webpage
for newURL in ProfessionalNewURLs:
    # Go to webpage
    driver.get(newURL)
    # Find messagebox
    messageBox = driver.find_element(By.ID, "message")
    # Input text
    messageBox.send_keys(ProfessionalTemplate)
    # Click submit
    submitButton = driver.find_element(By.XPATH, "//button[@class='button button--large button--wide']")
    submitButton.click()


# Close the browser window
driver.close()

print ("Completed")
print ("Number of professionals messaged:")
print (len(ProfessionalNewURLs))

print ("Number of students messaged:")
print (len(StudentNewURLs))


#TO DO:
#add in text docs - sort why password isn't working
