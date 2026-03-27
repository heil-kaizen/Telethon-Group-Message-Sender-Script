import asyncio
import os
from telethon import TelegramClient, errors

# ==========================================
# Configuration: Replace these with your own
# ==========================================
API_ID = 1234567  # Replace with your API ID (integer)
API_HASH = 'your_api_hash_here'  # Replace with your API Hash (string)
SESSION_NAME = 'user_broadcast_session'
GROUPS_FILE = 'groups.txt'
MAX_GROUPS = 7
DELAY_SECONDS = 3

def get_groups():
    if not os.path.exists(GROUPS_FILE):
        return []
    with open(GROUPS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def save_groups(groups):
    with open(GROUPS_FILE, 'w', encoding='utf-8') as f:
        for g in groups:
            f.write(f"{g}\n")

async def send_broadcast(client):
    groups = get_groups()
    if not groups:
        print("\nError: Group list is empty. Add groups first.")
        return

    print("\n[BROADCAST] Enter your message (Press Enter when done):")
    message_text = input("> ")
    if not message_text.strip():
        print("Error: Message cannot be empty.")
        return

    print("\n" + "="*20)
    print("MESSAGE PREVIEW:")
    print(message_text)
    print("="*20)
    
    confirm = input(f"Send to {len(groups)} groups? (y/n): ").lower()
    if confirm != 'y':
        print("Action cancelled.")
        return

    print("\nStarting broadcast...")
    for index, group in enumerate(groups):
        print(f"[{index + 1}/{len(groups)}] Sending to {group}...")
        try:
            target = int(group) if group.lstrip('-').isdigit() else group
            await client.send_message(target, message_text)
            print("  Success")
        except errors.FloodWaitError as e:
            print(f"  Rate limit: Must wait {e.seconds} seconds. Stopping broadcast.")
            break 
        except Exception as e:
            print(f"  Failed: {e}")
        
        if index < len(groups) - 1:
            await asyncio.sleep(DELAY_SECONDS)
    print("\nBroadcast task finished.")

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    
    while True:
        groups = get_groups()
        print(f"\n--- TELEGRAM SENDER MENU ({len(groups)}/{MAX_GROUPS} Groups) ---")
        print("1. Add a Group")
        print("2. List all Groups")
        print("3. Delete a Specific Group")
        print("4. Clear All Groups")
        print("5. START BROADCAST")
        print("6. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1':
            if len(groups) >= MAX_GROUPS:
                print(f"Limit reached: Maximum is {MAX_GROUPS} groups.")
            else:
                new_group = input("Enter @username, link, or ID: ").strip()
                if new_group:
                    groups.append(new_group)
                    save_groups(groups)
                    print(f"Added: {new_group}")

        elif choice == '2':
            print("\n--- CURRENT GROUPS ---")
            for i, g in enumerate(groups, 1):
                print(f"{i}. {g}")
            if not groups: print("List is empty.")

        elif choice == '3':
            if not groups:
                print("Nothing to delete.")
                continue
            for i, g in enumerate(groups, 1):
                print(f"{i}. {g}")
            try:
                idx = int(input("Enter the number of the group to delete: ")) - 1
                if 0 <= idx < len(groups):
                    removed = groups.pop(idx)
                    save_groups(groups)
                    print(f"Removed: {removed}")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            confirm = input("Clear all groups? (y/n): ").lower()
            if confirm == 'y':
                save_groups([])
                print("Group list cleared.")

        elif choice == '5':
            await send_broadcast(client)

        elif choice == '6':
            print("Exiting.")
            break
        else:
            print("Invalid selection.")

if __name__ == '__main__':
    asyncio.run(main())