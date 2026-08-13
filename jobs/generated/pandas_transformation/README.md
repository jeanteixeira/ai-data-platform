# pandas_transformation

This directory is a deterministic job candidate generated from `notebooks/examples/pandas-transformation.ipynb`.

The candidate must be reviewed and validated before promotion. Publishing did not register, schedule, build, deploy, or execute this job.

## Review checklist

- Review `src/main.py` for notebook-only assumptions and hidden state.
- Confirm every dependency and version in `requirements.txt`.
- Review `job.yaml`, including any schedule metadata.
- Build and run the container manually when the candidate is ready for validation.

```bash
docker build --tag data-platform-ai/pandas_transformation:candidate jobs/generated/pandas_transformation
docker run --rm data-platform-ai/pandas_transformation:candidate
```
