"""Package entry point for async execution."""
import asyncio
from .main import main

if __name__ == '__main__':
    asyncio.run(main())
