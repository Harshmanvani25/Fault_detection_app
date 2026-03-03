import os

# Change this if needed
server_root = r"/home/minsha/adserver_mount/adityadata/data/aditya"
shot_path   = r"/home/minsha/adserver_mount/adityadata/data/sht32322"

print("Testing server access...\n")

print("Server root exists:", os.path.exists(server_root))
print("Shot folder exists:", os.path.exists(shot_path))

if os.path.exists(server_root):
    print("\nListing first 10 items in server root:")
    try:
        items = os.listdir(server_root)
        for item in items[:10]:
            print("  ", item)
    except Exception as e:
        print("Error listing server root:", e)

if os.path.exists(shot_path):
    print("\nListing first 10 items in shot folder:")
    try:
        items = os.listdir(shot_path)
        for item in items[:10]:
            print("  ", item)
    except Exception as e:
        print("Error listing shot folder:", e)

print("\nDone.")
