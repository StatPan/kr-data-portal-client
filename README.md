# kr-data-portal-client

Production-ready, async-first Python client for the KR Public Data Portal (공공데이터포털).

## Features

- **Async First**: Built on `httpx` for high-performance asynchronous operations.
- **Spec-Driven**: Generated from YAML specifications to ensure accuracy.
- **Robust Models**: Uses Pydantic for strict response validation and easy data access.
- **Rate Limiting**: Built-in async rate limiter to comply with portal usage policies.
- **Google-Style Docstrings**: Full IDE support with detailed parameter descriptions and data update policies.

## Installation

```bash
pip install kr-data-portal-client
```

> [!IMPORTANT]
> **Recommended Version: 0.1.8+**  
> Previous versions (0.1.7 and below) are considered deprecated (yanked) due to critical API encoding and consistency issues. Version 0.1.8 introduces a custom URL construction logic to properly handle Service Key encoding requirements of the KR Public Data Portal.

## Quick Start

```python
import asyncio
from kr_data_portal.financial_services import FinancialClient
from kr_data_portal.models.financial_services import StockPriceInfoItem

async def main():
    service_key = "YOUR_SERVICE_KEY"
    
    async with FinancialClient(service_key=service_key) as client:
        # Fetch stock price info
        response = await client.getStockPriceInfo(itmsNm="삼성전자")
        
        # Access validated items
        items = response.items(StockPriceInfoItem)
        for item in items:
            print(f"{item.itmsNm}: {item.clpr} KRW")

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

### Project Structure

- `src/kr_data_portal/`: Core package.
- `specs/`: API specification files (YAML).
- `scripts/`: Code generation scripts.
- `tests/`: Unit tests.

### Code Generation

To regenerate the client from specifications:

```bash
python scripts/generate_client.py
```

### Running Tests

```bash
uv run pytest
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests. We use [Conventional Commits](https://www.conventionalcommits.org/) for automated release management.

## License

MIT
