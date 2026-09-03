FROM python:3.12-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH=/home/agent/.local/bin:$PATH

RUN groupadd --gid 10001 agent \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin agent \
    && mkdir -p /workspace /home/agent/.local \
    && chown -R agent:agent /workspace /home/agent

WORKDIR /workspace
COPY requirements.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY --chmod=0555 entrypoint.sh /usr/local/bin/agent-entrypoint
USER agent
ENTRYPOINT ["/usr/local/bin/agent-entrypoint"]
CMD ["python", "-m", "score2gp.cli", "--help"]
