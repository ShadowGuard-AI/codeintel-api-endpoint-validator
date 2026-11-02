![A hillside cloud watch with no lettering: ridge grass bent by the wind, a closed atlas on the camp table, a rain gauge rim catching light, a kite string rising out of frame, and one building cumulus with a flat base and towered top over the valley](intro-banner.png)


# codeintel-API-Endpoint-Validator

![A hillside watch with three members seen from behind around a camp table, one standing with a rain gauge, a kite high in the violet sky, one large cumulus building over the valley, and codeintel-api-endpoint-validator entered across the open left page of the atlas on the table](banner.png)

![An open cloud atlas plate with a copper hinge, one cumulus with a flat grey base and a white domed top inside a violet border, and an empty ruled line beneath the drawing, the heading plate](logo.png)

![Hillside watch in three depths: the cumulus towers rise by small stages and subside at the edges, a weather vane turns in gusts and settles while a kite tail streams beside it, and a rain gauge at the lower edge rises drop by drop during a passing shower and holds steady](scene.svg)

Scans a codebase for defined API endpoints and validates them against a defined schema (e.g., OpenAPI/Swagger). Detects endpoint definitions written as route, get, post, put, delete, or patch decorators on app, blueprint, router, or similar objects, checks each collected endpoint path against the schema paths and their method keys, and flags inconsistencies between the collected endpoints and the schema. The tool makes no judgement about whether an endpoint is a vulnerability or a misconfiguration. A code path that does not exist exits 1, and each run logs how many files were scanned and how many endpoints were checked.

> **Logbook marginalia: a closing slash is a different path.** Each collected path is compared as an exact string, so a route written with a closing slash and a schema path written without one are reported as different.

![Major separator: rain drops falling through the full width of the rule, each ending in a copper splash ring](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowStrikeHQ/codeintel-api-endpoint-validator`

> **Logbook marginalia: clone line flagged.** The install line above points to ShadowStrikeHQ, not to ShadowGuard-AI. It is preserved as printed and flagged here, not quietly corrected. The repository also carries a requirements.txt naming PyYAML, a step the README does not give.

![Minor separator: a centred cluster of three rain drops falling through the rule, each ending in a copper splash ring](sep-light.svg)

## Usage
`./codeintel-api-endpoint-validator [params]`

> **Logbook marginalia: usage line flagged.** The usage line above is a placeholder. The parser in main.py requires two positional arguments, a code path and a schema path, with -v available after them.

![Major separator: rain drops falling through the full width of the rule, each ending in a copper splash ring](sep-heavy.svg)

## Parameters
- `-h`: Show help message and exit
- `-v`: Enable verbose logging.

> **Logbook marginalia: the README omits both paths.** The parameter list above lists only -h and -v. The two positional paths the run cannot start without, the code path and the schema path, are supplied only in these flagged notes, never inserted into the preserved list as if the README had contained them.

![Major separator: rain drops falling through the full width of the rule, each ending in a copper splash ring](sep-heavy.svg)

## License
Copyright (c) ShadowStrikeHQ

> **Logbook marginalia: copyright line flagged.** The closing line above reads Copyright (c) ShadowStrikeHQ, preserved as printed. The repository LICENSE file carries the MIT License.
