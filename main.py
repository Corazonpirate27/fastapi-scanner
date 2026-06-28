from fastapi import FastAPI
from pydantic import BaseModel, Field
import socket
from concurrent.futures import ThreadPoolExecutor
from fastapi import Header, HTTPException

app = FastAPI(title="Security Scanner API")
API_KEY = "secret-scanner-key-2026"

def verify_key(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

class ScanRequest(BaseModel):
    ip: str = Field(pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    ports: list[int] = Field(default=[80, 443, 22, 21,53])
class ScanResult(BaseModel):
    ip: str
    open_ports: list[int]
    closed_ports: list[int]
def scan_port(ip: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

@app.get("/health")
def health_check():
    return {"status": "running", "message": "Security Scanner API is live!"}

@app.post("/scan", response_model=ScanResult)
def run_scan(request: ScanRequest, api_key: str = Header(alias="x-api-key")):
    verify_key(api_key)
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda p: (p, scan_port(request.ip, request.ports[0])), request.ports))

    open_ports = [p for p, is_open in results if is_open]
    closed_ports = [p for p, is_open in results if not is_open]

    return ScanResult(ip=request.ip, open_ports=open_ports, closed_ports=closed_ports)

@app.get("/scan/{ip}")
def quick_span(ip: str):
    common_ports = [80, 443, 22, 21, 53, 8080]
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda p: (p, scan_port(ip, p)), common_ports))
    open_ports = [p for p, is_open in results if is_open]
    return {"ip": ip, "open_ports": open_ports}

if __name__ == "__main__":
     import uvicorn
     uvicorn.run(app, host="0.0.0.0", port=8000)