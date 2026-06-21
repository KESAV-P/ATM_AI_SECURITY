import time
import subprocess
import os

# Your Details
POLICE_NUMBER = "+917010142014"
ADB_PATH = "/Users/kesavp/Library/Android/sdk/platform-tools/adb"

def run_adb(command):
    full_cmd = f"{ADB_PATH} shell {command}"
    print(f"👉 Running: {command}")
    os.system(full_cmd)

def test_call_methods():
    print(f"📞 DEBUGGER: Testing call to {POLICE_NUMBER}...")
    
    # 1. Wake up screen
    run_adb("input keyevent 26") # Power (toggle)
    run_adb("input keyevent 82") # Menu/Unlock
    time.sleep(1)

    # 2. Open Dialer
    print("\n--- Step 1: Opening Dialer ---")
    run_adb(f"am start -a android.intent.action.DIAL -d tel:{POLICE_NUMBER}")
    time.sleep(2)
    
    print("\n--- Step 2: Attempting to Click Call Button ---")
    
    # Method A: KEY EVENT 66 (Enter)
    print("Method A: Pressing ENTER key...")
    run_adb("input keyevent 66")
    time.sleep(1)
    
    # Method B: KEY EVENT 5 (Call Hardware Key)
    print("Method B: Pressing CALL key...")
    run_adb("input keyevent 5")
    time.sleep(1)
    
    # Method C: TAB + ENTER (Navigation)
    print("Method C: Tabbing to button...")
    run_adb("input keyevent 61") # Tab
    run_adb("input keyevent 61") # Tab
    run_adb("input keyevent 66") # Enter
    time.sleep(1)
    
    # Method D: COORDINATE TAP (Brute force)
    # Most phones have the green button at the bottom center.
    # Assuming valid FHD resolution (1080x2400) -> Center x=540, Bottom y=2200
    print("Method D: Tapping screen coordinates (540, 2200)...")
    run_adb("input tap 540 2000") 
    run_adb("input tap 540 2100") 
    run_adb("input tap 540 2200") 
    
    print("\n✅ Test Complete. Check phone to see if call started.")

if __name__ == "__main__":
    if not os.path.exists(ADB_PATH):
        print("❌ Error: ADB not found at path.")
    else:
        test_call_methods()
