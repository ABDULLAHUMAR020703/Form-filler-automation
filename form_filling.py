def fixed_form_filling():
    """Fixed version that properly handles element waiting and uses correct selectors"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to the form page
            print("Navigating to form page...")
            page.goto("https://www.tutorialspoint.com/selenium/practice/selenium_automation_practice.php",timeout=60000)
            
            # Wait for the page to fully load
            page.wait_for_load_state("networkidle")
            print("Page loaded successfully")
            
            # Wait for the form to be visible
            page.wait_for_selector("#name", timeout=10000)
            print("Form elements are ready")
            
            # ===== FIXED FORM FILLING WITH PROPER WAITS =====
            
            # 1. First Name - wait for element to be visible
            print("Filling first name...")
            page.wait_for_selector("#name", state="visible")
            page.fill("#name", "John")
            
            # 3. Email - wait for element to be visible
            print("Filling email...")
            page.wait_for_selector("#email", state="visible")
            page.fill("#email", "john.doe@example.com")
            
            #4. Gender
            print("Selecting gender...")
            page.locator("input[name='gender']").nth(0).check()
            
            # 4. Phone number
            print("Filling phone number...")
            page.wait_for_selector("#mobile", state="visible")
            page.fill("#mobile", "1234567890")
            
            # 5. Date of Birth
            print("Filling date of birth...")
            page.wait_for_selector("#dob", state="visible")
            page.fill("#dob", "1990-07-09")
            # 6. Subject 
            print("Selecting subject...")
            page.fill("#subjects","English")

            # 7. Hobbies
            print("Selecting hobbies...")
            # page.wait_for_selector("#hobbies", state="visible")
            # page.check("#hobbies")
            page.locator("input[type='checkbox'].form-check-input").nth(0).check()
            page.locator("input[type='checkbox'].form-check-input").nth(2).check()

            # 8. Picture
            print("Uploading picture...")
            page.set_input_files("#picture", "C:\\Users\\abdul\\Downloads\\ok.png")


            # 9. Current Address
            print("Filling address...")
            # page.wait_for_selector("#picture", state="visible")
            # page.fill("#address", "123 Main Street, City, State")
            page.fill("textarea#picture", "123 Main Street, City, State")
            
            # # 7. Gender (Radio button)
            # print("Selecting gender...")
            # page.wait_for_selector("input[value='Male']", state="visible")
            # page.check("input[value='Male']")
            
            # 8. Hobbies (Checkboxes)

            
            # 9. State dropdown
            print("Selecting state...")
            page.click("#state")
            page.select_option("#state", value="NCR") 
            
                   
            # 10. City dropdown
            print("Selecting city...")
            page.click("#city")
            page.select_option("#city", value="Agra")
            
            # 11. Submit form
            print("Submitting form...")
            page.click("input[value='Login']")
            
            # Wait to see the results
            time.sleep(3)
            print("Form submitted successfully!")
            
        except Exception as e:
            print(f"Error occurred: {e}")
            # Take a screenshot for debugging
            page.screenshot(path="error_screenshot.png")
            print("Screenshot saved as error_screenshot.png")
        
        finally:
            browser.close()