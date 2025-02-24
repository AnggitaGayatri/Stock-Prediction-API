from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"Received {request.method} request at {request.url.path}")
    return await call_next(request)

# @app.get("/")
# async def root():
#     return {"message": "Stock Prediction API for LQ45"}

@app.post("/predict/")
async def predict(symbols: list[str]):
    predictions = []
    
    for symbol in symbols:
        try:
            result = predict_stock(symbol)
            
            if result is None:
                raise HTTPException(
                    status_code=404,  
                    detail=f"Data atau model untuk {symbol} tidak ditemukan."
                )
            predictions.append(result)
        
        except HTTPException as e:
            raise e  
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Terjadi kesalahan pada pemrosesan untuk simbol {symbol}. Error: {str(e)}"
            )
    
    return {
        "error": False,
        "message": "success",
        "stocks": predictions
    }
