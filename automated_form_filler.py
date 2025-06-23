from playwright.sync_api import sync_playwright
import time
import threading
from datetime import datetime
import json
import os
import yaml


class FormAutomation:
    """Class to handle form automation with timing and multiple instances"""
    
    def __init__(self, instance_id=1, headless=False, customer_data=None):
        self.instance_id = instance_id
        self.headless = headless
        self.customer_data = customer_data
        self.start_time = None
        self.end_time = None
        self.success = False
        self.error_message = None
        self.screenshot_path = None
        
    def fill_form(self):
        """Fill the form with proper error handling and timing"""
        self.start_time = time.time()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                print(f"[Instance {self.instance_id}] Starting form automation...")
                
                # Navigate to the form page
                print(f"[Instance {self.instance_id}] Navigating to form page...")
                page.goto("https://www.tutorialspoint.com/selenium/practice/selenium_automation_practice.php", timeout=60000)
                
                # Wait for the page to fully load
                page.wait_for_load_state("networkidle")
                print(f"[Instance {self.instance_id}] Page loaded successfully")
                
                # Wait for the form to be visible
                page.wait_for_selector("#name", timeout=10000)
                print(f"[Instance {self.instance_id}] Form elements are ready")
                
                # ===== FORM FILLING WITH CUSTOMER DATA =====
                
                # 1. First Name
                print(f"[Instance {self.instance_id}] Filling first name: {self.customer_data['first_name']}")
                page.wait_for_selector("#name", state="visible")
                page.fill("#name", self.customer_data['first_name'])
                
                # 2. Email
                print(f"[Instance {self.instance_id}] Filling email: {self.customer_data['email']}")
                page.wait_for_selector("#email", state="visible")
                page.fill("#email", self.customer_data['email'])
                
                # 3. Gender
                print(f"[Instance {self.instance_id}] Selecting gender: {self.customer_data['gender']}")
                gender = self.customer_data['gender'].strip().capitalize()
                page.locator(f"//label[normalize-space(text())='{gender}']/preceding-sibling::input[@type='radio']").check()
                
                # 4. Mobile number
                print(f"[Instance {self.instance_id}] Filling mobile: {self.customer_data['mobile']}")
                page.wait_for_selector("#mobile", state="visible")
                page.fill("#mobile", self.customer_data['mobile'])
                
                # 5. Date of Birth
                print(f"[Instance {self.instance_id}] Filling date of birth: {self.customer_data['date_of_birth']}")
                page.wait_for_selector("#dob", state="visible")
                page.fill("#dob", self.customer_data['date_of_birth'])
                
                # 6. Subjects
                print(f"[Instance {self.instance_id}] Selecting subjects: {self.customer_data['subjects']}")
                page.fill("#subjects", self.customer_data['subjects'])
                
                # 7. Hobbies
                print(f"[Instance {self.instance_id}] Selecting hobbies: {self.customer_data['hobbies']}")
                for hobby in self.customer_data['hobbies']:
                    if hobby.lower() == 'sport':
                        page.locator("input[type='checkbox'].form-check-input").nth(0).check()
                    elif hobby.lower() == 'reading':
                        page.locator("input[type='checkbox'].form-check-input").nth(1).check()
                    elif hobby.lower() == 'music':
                        page.locator("input[type='checkbox'].form-check-input").nth(2).check()
                
                # 8. Picture
                print(f"[Instance {self.instance_id}] Uploading picture...")
                picture_path = self.customer_data['picture_path']
                if os.path.exists(picture_path):
                    page.set_input_files("input[type='file']#picture", picture_path)
                else:
                    print(f"[Instance {self.instance_id}] Warning: Picture file not found at {picture_path}")
                
                # 9. Current Address
                print(f"[Instance {self.instance_id}] Filling address: {self.customer_data['current_address']}")
                page.fill("textarea#picture", self.customer_data['current_address'])
                
                # 10. State dropdown
                print(f"[Instance {self.instance_id}] Selecting state: {self.customer_data['state']}")
                page.click("#state")
                page.select_option("#state", value=self.customer_data['state'])
                
                # 11. City dropdown
                print(f"[Instance {self.instance_id}] Selecting city: {self.customer_data['city']}")
                page.click("#city")
                page.select_option("#city", value=self.customer_data['city'])
                
                # 12. Submit form
                print(f"[Instance {self.instance_id}] Submitting form...")
                page.click("input[value='Login']")
                
                # Wait to see the results
                print(f"[Instance {self.instance_id}] Form submitted successfully!")
                self.success = True
                
            except Exception as e:
                self.error_message = str(e)
                print(f"[Instance {self.instance_id}] Error occurred: {e}")
                
                # Take a screenshot for debugging
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.screenshot_path = f"error_screenshot_instance_{self.instance_id}_{timestamp}.png"
                page.screenshot(path=self.screenshot_path)
                print(f"[Instance {self.instance_id}] Screenshot saved as {self.screenshot_path}")
                
            finally:
                browser.close()
                
        self.end_time = time.time()
        
    def get_execution_time(self):
        """Get the execution time in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
        
    def get_status(self):
        """Get the status of the automation"""
        return {
            'instance_id': self.instance_id,
            'customer_name': self.customer_data['first_name'] if self.customer_data else 'Unknown',
            'success': self.success,
            'execution_time': self.get_execution_time(),
            'error_message': self.error_message,
            'screenshot_path': self.screenshot_path,
            'start_time': self.start_time,
            'end_time': self.end_time
        }


def load_customer_data(yaml_file="customer_details.yml"):
    """Load customer data from YAML file"""
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Error: {yaml_file} not found!")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None


def run_single_instance(instance_id=1, headless=False, customer_data=None):
    """Run a single instance of form automation"""
    automation = FormAutomation(instance_id, headless, customer_data)
    automation.fill_form()
    return automation.get_status()


def run_multiple_instances(num_instances=3, headless=False, parallel=False, customer_data_list=None):
    """Run multiple instances of form automation"""
    results = []
    
    if parallel:
        # Run instances in parallel using threads
        print(f"Running {num_instances} instances in parallel...")
        threads = []
        automations = []
        
        for i in range(num_instances):
            customer_data = customer_data_list[i] if customer_data_list and i < len(customer_data_list) else None
            automation = FormAutomation(i + 1, headless, customer_data)
            automations.append(automation)
            thread = threading.Thread(target=automation.fill_form)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        for automation in automations:
            results.append(automation.get_status())
            
    else:
        # Run instances sequentially
        print(f"Running {num_instances} instances sequentially...")
        for i in range(num_instances):
            customer_data = customer_data_list[i] if customer_data_list and i < len(customer_data_list) else None
            result = run_single_instance(i + 1, headless, customer_data)
            results.append(result)
    
    return results


def print_results_summary(results):
    """Print a summary of all results"""
    print("\n" + "="*60)
    print("AUTOMATION RESULTS SUMMARY")
    print("="*60)
    
    successful_runs = [r for r in results if r['success']]
    failed_runs = [r for r in results if not r['success']]
    
    print(f"Total instances: {len(results)}")
    print(f"Successful: {len(successful_runs)}")
    print(f"Failed: {len(failed_runs)}")
    print(f"Success rate: {(len(successful_runs)/len(results)*100):.1f}%")
    
    if successful_runs:
        execution_times = [r['execution_time'] for r in successful_runs if r['execution_time']]
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
            
            print(f"\nExecution Times (successful runs):")
            print(f"Average: {avg_time:.2f} seconds")
            print(f"Minimum: {min_time:.2f} seconds")
            print(f"Maximum: {max_time:.2f} seconds")
    
    print("\nDetailed Results:")
    for result in results:
        status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
        time_str = f"{result['execution_time']:.2f}s" if result['execution_time'] else "N/A"
        customer_name = result.get('customer_name', 'Unknown')
        print(f"Instance {result['instance_id']} ({customer_name}): {status} ({time_str})")
        if result['error_message']:
            print(f"  Error: {result['error_message']}")
        if result['screenshot_path']:
            print(f"  Screenshot: {result['screenshot_path']}")
    
    print("="*60)


def save_results_to_file(results, filename="automation_results.json"):
    """Save results to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {filename}")


def main():
    """Main function to run the automation"""
    print("Automated Form Filler with Customer Data")
    print("="*40)
    
    # Load customer data
    data = load_customer_data()
    if not data:
        print("Failed to load customer data. Exiting...")
        return
    
    customers = data.get('customers', {})
    customer_list = list(customers.values())
    
    print(f"Loaded {len(customer_list)} customer profiles from YAML file.")
    
    while True:
        print("\nChoose an option:")
        print("1. Run single instance with customer data")
        print("2. Run multiple instances sequentially with customer data")
        print("3. Run multiple instances in parallel with customer data")
        print("4. Run with specific customer (by index)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            headless = input("Run in headless mode? (y/n): ").lower() == 'y'
            customer_data = customer_list[0] if customer_list else None
            result = run_single_instance(1, headless, customer_data)
            print_results_summary([result])
            
        elif choice == "2":
            try:
                num_instances = int(input(f"Enter number of instances (max {len(customer_list)}): "))
                num_instances = min(num_instances, len(customer_list))
                headless = input("Run in headless mode? (y/n): ").lower() == 'y'
                selected_customers = customer_list[:num_instances]
                results = run_multiple_instances(num_instances, headless, parallel=False, customer_data_list=selected_customers)
                print_results_summary(results)
                save_results_to_file(results)
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "3":
            try:
                num_instances = int(input(f"Enter number of instances (max {len(customer_list)}): "))
                num_instances = min(num_instances, len(customer_list))
                headless = input("Run in headless mode? (y/n): ").lower() == 'y'
                selected_customers = customer_list[:num_instances]
                results = run_multiple_instances(num_instances, headless, parallel=True, customer_data_list=selected_customers)
                print_results_summary(results)
                save_results_to_file(results)
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "4":
            try:
                print(f"Available customers (1-{len(customer_list)}):")
                for i, customer in enumerate(customer_list, 1):
                    print(f"{i}. {customer['first_name']} - {customer['email']}")
                
                customer_index = int(input(f"Enter customer number (1-{len(customer_list)}): ")) - 1
                if 0 <= customer_index < len(customer_list):
                    headless = input("Run in headless mode? (y/n): ").lower() == 'y'
                    customer_data = customer_list[customer_index]
                    result = run_single_instance(customer_index + 1, headless, customer_data)
                    print_results_summary([result])
                else:
                    print("Invalid customer number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "5":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 