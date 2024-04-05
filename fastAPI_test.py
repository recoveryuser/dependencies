from fastapi import FastAPI
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from io import BytesIO

app = FastAPI()

# Mock function to generate Plotly chart
def generate_plot():
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 11, 12, 13, 14]
    })
    fig = go.Figure(data=go.Scatter(x=df['x'], y=df['y']))
    return fig

# Function to generate response based on input question
def generate_response(question):
    if "plot" in question.lower():
        fig = generate_plot()
        svg_bytes = pio.to_image(fig, format="svg")
        return BytesIO(svg_bytes), "image/svg+xml"
    elif "dataframe" in question.lower():
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 11, 12, 13, 14]
        })
        return df.to_json(orient='records'), "application/json"
    else:
        return "This is a simple string response", "text/plain"

# Route to handle user queries
@app.get("/query")
async def handle_query(question: str):
    response, content_type = generate_response(question)
    return response, {"Content-Type": content_type}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8084)
