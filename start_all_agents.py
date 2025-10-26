"""
Start all three agents in separate processes
"""
import subprocess
import sys
import time
import signal

processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\nShutting down agents...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def start_agent(script_path, name):
    """Start an agent in a subprocess"""
    print(f"Starting {name}...")
    process = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    processes.append(process)
    return process

def main():
    print("="*60)
    print("STARTING EMAIL ANALYSIS AGENTS")
    print("="*60)
    print("\nStarting agents in sequence...\n")

    # Start agents
    analyzer = start_agent("agents/analyzer.py", "Analyzer Agent (Port 8001)")
    time.sleep(2)

    evaluator = start_agent("agents/evaluator.py", "Evaluator Agent (Port 8002)")
    time.sleep(2)

    output = start_agent("agents/output.py", "Output Agent (Port 8003)")
    time.sleep(2)

    print("\n" + "="*60)
    print("ALL AGENTS RUNNING")
    print("="*60)
    print("\nAgent addresses:")
    print(f"  Analyzer:  {analyzer.pid}")
    print(f"  Evaluator: {evaluator.pid}")
    print(f"  Output:    {output.pid}")
    print("\nPress Ctrl+C to stop all agents")
    print("="*60 + "\n")

    # Monitor output from all processes
    import select

    while True:
        for process in processes:
            if process.poll() is not None:
                print(f"\n⚠️  Process {process.pid} exited!")
                break

            # Check for output (non-blocking)
            if process.stdout:
                line = process.stdout.readline()
                if line:
                    print(f"[{process.pid}] {line.rstrip()}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
