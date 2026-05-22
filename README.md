# epub.yazi

Plugin for [Yazi](https://github.com/sxyazi/yazi) to preview epub cover images.

Requires Python 3 (pre-installed on macOS and most Linux systems).

## Installation

```bash
git clone https://github.com/mickmcq/epub.yazi.git ~/.config/yazi/plugins/epub.yazi
```

## Configuration

Add the following to your `yazi.toml`:

```toml
[plugin]
prepend_previewers = [
  { url = "*.epub", run = "epub" },
]

prepend_preloaders = [
  { url = "*.epub", run = "epub" },
]
```

## Requirements

- Yazi 26.x or later
- Python 3

## Notes

- Tested on macOS and Linux
- On Windows, `python` must be in your PATH
