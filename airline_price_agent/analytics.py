from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Sequence


@dataclass(frozen=True)
class AlertDecision:
    should_alert: bool
    average_price: float | None
    threshold_price: float | None
    reason: str


def evaluate_alert(
    current_price: float,
    historical_prices: Sequence[float],
    below_avg_percent: float,
    min_samples: int,
) -> AlertDecision:
    if len(historical_prices) < min_samples:
        return AlertDecision(
            should_alert=False,
            average_price=None,
            threshold_price=None,
            reason=f"insufficient_samples({len(historical_prices)}/{min_samples})",
        )

    avg_price = mean(historical_prices)
    threshold = avg_price * (1 - (below_avg_percent / 100.0))
    should_alert = current_price <= threshold
    reason = "below_threshold" if should_alert else "normal_price"
    return AlertDecision(
        should_alert=should_alert,
        average_price=avg_price,
        threshold_price=threshold,
        reason=reason,
    )
