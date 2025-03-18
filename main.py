from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired
import time
import random
import os
import json
from datetime import datetime

cl = Client()
SESSION_FILE = "instagram_session.json"

def login():
    """Secure login with 2FA and challenge support."""
    username = input("Enter your Instagram username: ")
    password = input("Enter your password: ")
    
    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            print("✅ Logged in with saved session")
        else:
            cl.login(username, password)
            cl.dump_settings(SESSION_FILE)
            print("✅ New session saved")
    except ChallengeRequired:
        print("\n🔐 Instagram requires verification!")
        method = cl.challenge_resolve(cl.last_json)
        if method == "email":
            print("Check your email for the verification code")
        elif method == "sms":
            print("Check your phone for the SMS code")
        code = input("Enter the 6-digit code: ")
        cl.challenge_send(code, method)
        cl.dump_settings(SESSION_FILE)
        print("✅ Successfully verified")
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        exit()

def retrieve_messages_with_pagination(thread_id, own_user_id, amount=1000):
    own_messages = []
    try:
        thread_info = cl.direct_thread(thread_id, amount=amount)
        messages = thread_info.messages
        print(f"Batch retrieved: {len(messages)} messages in thread {thread_id}.")
        for msg in messages:
            if str(msg.user_id) == str(own_user_id):
                own_messages.append((msg.id, thread_id))
    except Exception as e:
        print(f"❌ Error fetching messages: {str(e)}")
    return own_messages

def display_progress(current, total, start_time, success_count):
    """Display a visual progress bar with statistics."""
    elapsed = time.time() - start_time
    avg_time = elapsed / current if current > 0 else 0
    remaining = avg_time * (total - current)
    success_rate = (success_count / current) * 100 if current > 0 else 0
    progress = current / total
    bar_length = 30
    filled = int(bar_length * progress)
    bar = '█' * filled + '-' * (bar_length - filled)
    print(
        f"[{bar}] {current}/{total} ({progress:.1%}) | "
        f"Success: {success_rate:.1f}% | "
        f"Speed: {60/avg_time:.1f} messages/min | "
        f"Remaining: {int(remaining // 60)}m {int(remaining % 60)}s",
        end='\r'
    )

def delete_message(msg_data):
    msg_id, thread_id = msg_data
    try:
        return cl.direct_message_delete(thread_id=thread_id, message_id=msg_id)
    except Exception as e:
        print(f"First method error: {e}")
        try:
            return cl.private_request(
                f"direct_v2/threads/{thread_id}/items/{msg_id}/delete/",
                data={}
            )
        except Exception as e:
            print(f"API call 1 error: {e}")
            try:
                return cl.private_request(
                    f"direct_v2/threads/delete_items/",
                    data={"thread_ids": json.dumps([thread_id]), "item_ids": json.dumps([msg_id])}
                )
            except Exception as e:
                print(f"API call 2 error: {e}")
                try:
                    return cl.private_request(
                        f"direct_v2/threads/{thread_id}/delete_items/",
                        data={"item_ids": json.dumps([msg_id])}
                    )
                except Exception as e:
                    print(f"API call 3 error: {e}")
                    raise AttributeError("No suitable method found to delete messages in this version of instagrapi")

def main():
    login()
    
    direct_methods = [method for method in dir(cl) if 'direct' in method.lower()]
    print(f"\nAvailable direct message methods in your instagrapi version:")
    for method in sorted(direct_methods):
        print(f"  - {method}")
    
    print("\n📨 Fetching chats...")
    threads = cl.direct_threads()

    for idx, thread in enumerate(threads):
        names = [user.username for user in thread.users if str(user.pk) != str(cl.user_id)]
        last_active = (thread.last_activity_at.strftime("%d-%m-%Y %H:%M") 
                       if hasattr(thread, 'last_activity_at') and thread.last_activity_at else "Unknown")
        print(f"[{idx}] Chat with: {', '.join(names)} | Last activity: {last_active}")
    
    print(f"\nLogged in as: {cl.username} (User ID: {cl.user_id})")
    

    selected = input("\n➤ Enter chat numbers (e.g., '0,2-4'): ")
    selected_indices = []
    for part in selected.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            selected_indices.extend(range(start, end+1))
        elif part.isdigit():
            selected_indices.append(int(part))
    
    print("\n⚡ Speed settings")
    print("1) Normal (2-5 sec between messages)")
    print("2) Fast (0.5-2 sec between messages)")
    print("3) Turbo (0.2-0.7 sec between messages, risk of rate limiting)")
    speed_choice = input("Choose speed (1-3): ") or "1"
    
    if speed_choice == "1":
        min_delay, max_delay = 2.0, 5.0
        batch_size, batch_delay = 10, 5.0
    elif speed_choice == "2":
        min_delay, max_delay = 0.5, 2.0
        batch_size, batch_delay = 50, 3.0
    else:
        min_delay, max_delay = 0.2, 0.7
        batch_size, batch_delay = 30, 2.0
    
    continue_until_all_deleted = input("\nContinue until all messages are deleted? (y/n): ").lower() == 'y'
    test_mode = input("Do you want to test with one message first? (y/n): ").lower() == 'y'
    
    while True:
        total_deleted = 0
        for idx in selected_indices:
            if idx >= len(threads):
                continue
            thread = threads[idx]
            print(f"\n🔍 Scanning chat {idx} (retrieving all messages via pagination)...")
            own_messages = retrieve_messages_with_pagination(thread.id, cl.user_id, amount=1000)
            print(f"Own messages found in chat {idx}: {len(own_messages)}")
            if not own_messages:
                continue
            
            if test_mode:
                print(f"\n🔍 TEST MODE: Deleting one message out of {len(own_messages)} messages")
                test_msg_data = own_messages[0]
                print(f"Test: Deleting message ID {test_msg_data[0]} in thread {test_msg_data[1]}")
                try:
                    delete_message(test_msg_data)
                    print("✅ Test successful! Message deleted.")
                    total_deleted += 1
                except Exception as e:
                    print(f"❌ Test failed: {str(e)}")
                    if input("Do you want to continue with full deletion? (y/n): ").lower() != 'y':
                        return
                test_mode = False
            else:
                success = 0
                errors = []
                start_time = time.time()
                for i, msg_data in enumerate(own_messages, 1):
                    try:
                        delete_message(msg_data)
                        success += 1
                        total_deleted += 1
                        if i % 5 == 0:
                            print(f"✓ Message {i}/{len(own_messages)} deleted")
                    except Exception as e:
                        errors.append((msg_data[0], str(e)))
                        print(f"❌ Message {i}/{len(own_messages)} error: {str(e)}")
                    display_progress(i, len(own_messages), start_time, success)
                    delay = random.uniform(min_delay, max_delay)
                    if i % batch_size == 0:
                        delay += random.uniform(batch_delay * 0.8, batch_delay * 1.2)
                    time.sleep(delay)
                
                print(f"\n\n🎉 Batch result for chat {idx}:")
                print(f"- Total attempted: {len(own_messages)}")
                print(f"- Successful: {success}")
                print(f"- Failed: {len(errors)}")
                if errors:
                    print("\n❌ Errors:")
                    for msg_id, error in errors[:5]:
                        print(f"  Message {msg_id}: {error}")
        
        if total_deleted == 0:
            print("\n✅ No own messages found in the current scans.")
            break
        
        if not continue_until_all_deleted:
            break
        
        print("\n⏱️ Pausing briefly before rescanning...")
        time.sleep(3)
        threads = cl.direct_threads()
        print("\n🔄 New scan started.")

if __name__ == "__main__":
    main()
