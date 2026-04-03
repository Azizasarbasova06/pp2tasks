import json 

# 'with open' is a safe way to open a file. 
# It ensures the file closes itself, even if an error occurs in the program.
with open("json1.py", 'r') as f:
    # json.load(f) converts a JSON text file into a standard Python dictionary.
    data = json.load(f)

# 2. PRINT THE TABLE HEADER
# We create a header so the data looks professional.
print("Interface Status")
print("=" * 80)

# f"{...:<50}" is formatting magic (padding).
# <50 means: "reserve 50 characters for this text and align it to the left."
# This is needed so that the table columns are even and don't "drift."
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
print(f"{'-' * 50} {'-' * 20} {'-' * 8} {'-' * 6}")

# 3. DATA PARSING
# JSON data is often nested inside each other like Russian nesting dolls.
# We access the main key "imdata", which is a list of interfaces.
for item in data["imdata"]:
    # Dive deeper: l1PhysIf -> attributes
    attr = item["l1PhysIf"]["attributes"]
    
    # Extract specific values
    dn = attr["dn"]
    # If there is no description (descr), use an empty string to avoid errors
    descr = attr["descr"] if attr["descr"] else ""
    speed = attr["speed"]
    mtu = attr["mtu"]
    
    # 4. PRINTING THE TABLE ROW
    # Use the same formatting as in the header so that data aligns strictly under the headings.
    print(f"{dn:<50} {descr:<20} {speed:<8} {mtu:<6}")