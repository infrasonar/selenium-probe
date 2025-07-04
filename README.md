[![CI](https://github.com/infrasonar/selenium-probe/workflows/CI/badge.svg)](https://github.com/infrasonar/selenium-probe/actions)
[![Release Version](https://img.shields.io/github/release/infrasonar/selenium-probe)](https://github.com/infrasonar/selenium-probe/releases)

# InfraSonar Selenium Probe

Documentation: https://docs.infrasonar.com/collectors/probes/selenium/

## Environment variable

Variable            | Default                        | Description
------------------- | ------------------------------ | ------------
`COMMAND_EXECUTER`  | `http://localhost:4444`        | Selenium Command Executer address.
`AGENTCORE_HOST`    | `127.0.0.1`                    | Hostname or Ip address of the AgentCore.
`AGENTCORE_PORT`    | `8750`                         | AgentCore port to connect to.
`INFRASONAR_CONF`   | `/data/config/infrasonar.yaml` | File with probe and asset configuration like credentials.
`MAX_PACKAGE_SIZE`  | `500`                          | Maximum package size in kilobytes _(1..2000)_.
`MAX_CHECK_TIMEOUT` | `300`                          | Check time-out is 80% of the interval time with `MAX_CHECK_TIMEOUT` in seconds as absolute maximum.
`DRY_RUN`           | _none_                         | Do not run demonized, just return checks and assets specified in the given yaml _(see the [Dry run section](#dry-run) below)_.
`LOG_LEVEL`         | `warning`                      | Log level (`debug`, `info`, `warning`, `error` or `critical`).
`LOG_COLORIZED`     | `0`                            | Log using colors (`0`=disabled, `1`=enabled).
`LOG_FMT`           | `%y%m%d %H:%M:%S`              | Log format prefix.

## Docker build

```
docker build -t selenium-probe . --no-cache
```

## Config

No config is required but you might want to set a password and/or secret for usage in your script.

```
selenium:
  config:
    password: myPassword
    secret: mySecret
```

## Dry run

Dry run for this collector is not possible. Instead, use the `infrasonar-selenium` test suite to build a test script.

## Creating tests

See https://github.com/infrasonar/selenium for building InfraSonar Selenium tests.
