FROM yifanmai/crfm-helm-deps
RUN uv pip install --system --no-deps crfm-helm@git+https://github.com/stanford-crfm/helm.git@main
RUN useradd --create-home --shell /bin/bash crfm-helm
USER crfm-helm
WORKDIR /home/crfm-helm
ENTRYPOINT ["helm-run"]
