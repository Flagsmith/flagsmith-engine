[![Feature Flag, Remote Config and A/B Testing platform, Flagsmith](https://github.com/Flagsmith/flagsmith/raw/main/static-files/hero.png)](https://www.flagsmith.com/)

[Flagsmith](https://www.flagsmith.com/) is an open source, fully featured, Feature Flag and Remote Config service. Use
our hosted API, deploy to your own private cloud, or run on-premise.

# Flagsmith Flag Engine

This project powers the core [Flagsmith API](https://github.com/Flagsmith/flagsmith-api) flag evaluations engine.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Design

- Marshmallow Schemas
- Plain Python
