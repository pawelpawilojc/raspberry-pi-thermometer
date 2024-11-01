import subprocess

def listen_for_ir_commands():
    process = subprocess.Popen(['irw'], stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'':
            break
        if output:
            print(f"Detected IR command: {output.strip()}")

if __name__ == "__main__":
    listen_for_ir_commands()