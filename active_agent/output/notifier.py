import subprocess

def notify(title, message, sound=True):
    """
    Sends a macOS system notification using osascript.
    Handles escaping double quotes in the message.
    """
    try:
        # Escape double quotes for AppleScript
        escaped_message = message.replace('"', '\\"')
        escaped_title = title.replace('"', '\\"')

        command = f'display notification "{escaped_message}" with title "{escaped_title}"'
        if sound:
            command += ' sound name "default"'

        # Execute AppleScript via subprocess
        subprocess.run(['osascript', '-e', command])
        print(f"🔔 Notification sent: {title} - {message}")
        return True
    except Exception as e:
        print(f"🔥 Error sending macOS notification: {e}")
        return False

if __name__ == "__main__":
    # Test notification with quotes
    notify("Active Agent", '이것은 "따옴표" 테스트입니다!')
