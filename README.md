# Black_Loft_Hunter

A proactive, fault-tolerant cryptocurrency trading bot for **Bybit API** (Unified Trading Account). Designed to operate reliably under unstable network conditions.

## Key Features
* **Connection Resilience:** Integrated infinite loop logic with `try-except` blocks to handle network timeouts and VPN drops without crashing.
* **Proactive Monitoring:** Continuously tracks market price movements to identify entry points based on pre-defined percentage drops.
* **Automated Execution:** Handles the full cycle from price monitoring to Market Buy and subsequent Profit-Taking (Sell) orders.
* **Demo Mode Support:** Pre-configured for Bybit Testnet/Demo accounts for safe strategy validation.

## Technical Stack
* **Language:** Python 3.10+
* **Library:** `pybit` (Official Bybit SDK)
* **Environment:** Optimized for Pydroid 3 and desktop IDEs.

## Logic Flow
1.  **Market Analysis:** Fetches current price and calculates the target Support level.
2.  **Hunting Mode:** Waits for the price to hit the target `drop_percent`.
3.  **Persistence:** If connection fails, the bot enters a silent wait state and resumes immediately upon reconnection.
4.  **Profit Fixation:** Once the asset is bought, it calculates the exit point and waits for the `profit_percent` target.

## Configuration
```python
# Set your parameters in the main block:
pro_active_hunter(
    symbol="BTCUSDT", 
    drop_percent=4.5, 
    profit_percent=6.5, 
    usdt_budget=900
)
