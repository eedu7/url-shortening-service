import uvicorn
import argparse

parser = argparse.ArgumentParser(description="A Port to server")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",
        port=args.port,
        reload=True,
    )