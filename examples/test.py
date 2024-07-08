# pylint: skip-file
# flake8: noqa


def calculate_discount(price):
    return price - 10  # Magic number used directly


total_price = 100
discounted_price = calculate_discount(total_price)
print(discounted_price)

# This will provoke the C3001 pylint error
# add = lambda x, y: x + y

# test.py
config_path = "/etc/config/settings.conf"  # This should trigger R9999
relative_path = "settings.conf"  # This should not trigger R9999

# test opening a file in a fixed path
with open("/Users/aitorarnaiz/Desktop/guts-test/test.py") as file:
    print(file.read())

# example_for_binop.py

base_dir = "/usr/local"
config_file = base_dir + "/etc/config.txt"  # This line should trigger the checker

# This should not trigger the checker
relative_base = "user/data"
relative_config_file = relative_base + "/info.txt"

built_path = "/workspace" + "/project"  # This should trigger the checker


# Function attempting to create virtual units using subprocess (Windows-specific)
def create_virtual_unit_windows():
    try:
        # Example command that might create or interact with virtual units on Windows
        subprocess.check_output(["subst", "Z:", "C:\\Temp"])
    except subprocess.CalledProcessError as e:
        # Handle errors if needed
        print(f"Error creating virtual unit: {e}")


subprocess.check_output(["mount", "-t", "tmpfs", "none", "/mnt/virtual"])

result = subprocess.run(["subst", "Z:", "C:\\Temp"], capture_output=True, text=True)
output = result.stdout.strip()

os.system("subst Z: C:\\Temp")

subprocess.Popen(
    ["subst", "Z:", "C:\\Temp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()

os.system("subst Z: C:\\Temp")
