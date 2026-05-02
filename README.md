# Facade

A single URL that serves different content based on your user agent header.

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

Visit `http://127.0.0.1:8000/`. Change your user agent to `ABC` to see alternate content.

## How it works

The server checks the `user agent` header on every request. Normal visitors see `index.html`. Visitors with the switch user agent see `switch.html`.

This is the same technique malware uses to hide command and control servers. A compromised machine sends a specific user agent, the server recognizes it, and sends back payloads. Normal visitors see nothing suspicious.

The example pages are just placeholders. Replace `index.html` and `switch.html` with any content you want: login portals, admin dashboards, malware payloads, or blank pages.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SWITCH_UA` | `ABC` | user agent that triggers alternate content |
| `SWITCH_FILE` | `switch.html` | File served on alternate content trigger |
| `DEFAULT_FILE` | `index.html` | File served to everyone else |
| `HOST` | `127.0.0.1` | Bind address |
| `PORT` | `8000` | Bind port |
| `LOG_FILE` | *(none)* | Optional file to persist logs |

## Changing the user agent in Firefox based browsers

1. Go to `about:config`
2. Search `general.useragent.override`
3. Set it to `ABC`
4. Refresh the page
5. Clear the value when done

## With curl

```bash
# Default content
curl http://127.0.0.1:8000/

# Alternate content
curl http://127.0.0.1:8000/ -A "ABC"
```
