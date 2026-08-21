# Kasparro AI Readiness Auditor

Kasparro is a tool for Shopify merchants.

Its goal is to check whether a store's product information is clear and complete enough for an AI shopping assistant to understand and recommend the product.

For example, Kasparro will eventually look for:

- Clear product titles and descriptions
- Important details such as material, sizes, colors, and price
- Shipping and return information
- Reviews and other trust information
- Vague or missing information that could make an AI unsure about recommending the product

The planned workflow is:

```text
Product information
        ->
AI audit
        ->
Problems and missing information
        ->
AI Readiness Score
        ->
Recommendations for improvement
```

## What Works Right Now

The current version is only the backend foundation. It has a small FastAPI server with two endpoints:

- `GET /` confirms that the Kasparro API is running
- `GET /api/health` checks that the server is healthy

The product auditor, database, OpenAI integration, Shopify integration, and frontend dashboard have not been built yet.

## Technology

- **Python**: Main programming language
- **FastAPI**: Creates the backend API
- **Uvicorn**: Runs the FastAPI server
- **Pydantic**: Will validate product data in the next phase
- **OpenAI**: Will eventually analyze product information
- **Next.js**: Will eventually provide the frontend dashboard

## Run the Backend

From the project root:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## Test It

Open these URLs in a browser:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/api/health
http://127.0.0.1:8000/docs
```

The `/docs` page is an interactive Swagger page where the endpoints can be tested.

## Project Roadmap

1. Add Product data models with Pydantic
2. Create a small synthetic product dataset
3. Add the audit endpoint without AI
4. Connect the OpenAI API
5. Add a deterministic scoring engine
6. Generate recommendations and suggested improvements
7. Compare before and after scores
8. Connect Shopify data
9. Build the Next.js dashboard
