import unittest

import numpy as np
import pandas as pd

from finance_tools.returns import (
    cumulative_percentage_return,
    drawdown,
    simple_returns,
)


class ReturnTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prices = pd.Series([100.0, 110.0, 99.0])

    def test_simple_returns(self) -> None:
        result = simple_returns(self.prices)
        np.testing.assert_allclose(result.iloc[1:].to_numpy(), [0.10, -0.10])

    def test_cumulative_percentage_return(self) -> None:
        result = cumulative_percentage_return(self.prices)
        np.testing.assert_allclose(result.to_numpy(), [0.0, 10.0, -1.0])

    def test_drawdown(self) -> None:
        result = drawdown(self.prices)
        np.testing.assert_allclose(result.to_numpy(), [0.0, 0.0, -0.10])


if __name__ == "__main__":
    unittest.main()
