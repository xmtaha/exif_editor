import os

def find_json_files(folder):
    json_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".json"):
                full_path = os.path.join(root, file)
                json_files.append(full_path)
    return json_files

def delete_files(file_list):
    deleted = 0
    for path in file_list:
        try:
            os.remove(path)
            print(f"[DELETED] {path}")
            deleted += 1
        except Exception as e:
            print(f"[ERROR] Failed to delete: {path} ({e})")
    print(f"\n✅ {deleted} .json files deleted.")

if __name__ == "__main__":
    folder = input("Enter the path to the root folder: ").strip()
    if not os.path.exists(folder):
        print("❌ Invalid folder path.")
        exit()

    json_files = find_json_files(folder)
    if not json_files:
        print("No .json files found.")
        exit()

    print(f"\nFound {len(json_files)} .json files:\n")
    for path in json_files:
        print(path)

    confirm = input("\nDo you want to delete these files? (y/n): ").strip().lower()
    if confirm == "y":
        delete_files(json_files)
    else:
        print("Operation canceled.")
