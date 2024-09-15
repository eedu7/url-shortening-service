import argparse

import uvicorn

parser = argparse.ArgumentParser(description="PORT")

parser.add_argument("--host", type=str, default="127.0.0.1")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()

if __name__ == "__main__":
    uvicorn.run(app="routes:app", host=args.host, port=args.port, reload=True)
