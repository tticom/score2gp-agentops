FROM python:3.12-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254

ARG ANTIGRAVITY_CLI_VERSION=1.1.26

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH=/home/agent/.local/bin:$PATH

RUN groupadd --gid 10001 agent \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin agent \
    && mkdir -p /workspace/score2gp/.venv /home/agent/.local \
    && chown -R agent:agent /workspace /home/agent

RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install --yes --no-install-recommends bash ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/* \
    && curl --fail --silent --show-error --location https://antigravity.google/cli/install.sh \
      | bash -s -- --dir /usr/local/bin \
    && test "$(/usr/local/bin/agy --version)" = "$ANTIGRAVITY_CLI_VERSION" \
    && mkdir -p -m 755 /etc/apt/keyrings \
    && curl --fail --silent --show-error --location \
      https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      --output /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install --yes --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY --chmod=0555 entrypoint.sh github-askpass.sh /usr/local/bin/
COPY --chmod=0555 task_branch.py task-checkpoint /usr/local/bin/
USER agent
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "-m", "score2gp.cli", "--help"]
