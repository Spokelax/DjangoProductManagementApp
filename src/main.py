"""Main"""
# TODO: Complete Docstring

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "DjangoProductManagementApp.asgi:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
