import logging

import pandas as pd


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger("hello_world_job")

    logger.info("Starting hello world Python job")
    source = pd.DataFrame(
        {
            "category": ["books", "books", "games"],
            "amount": [10, 15, 20],
        }
    )
    totals = (
        source.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("category")
        .reset_index(drop=True)
    )

    logger.info("Input rows: %d", len(source))
    logger.info("Transformation result:\n%s", totals.to_string(index=False))
    logger.info("Hello world Python job completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
