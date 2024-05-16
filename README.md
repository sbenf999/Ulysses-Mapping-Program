# Ulysses Mapping Program
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

An offline and online mapping program created using CustomTkinter and TkinterMapview. Incorporates a settings system and an offline tile downloading addon. 

Originally designed to be used on a 7-inch raspberry pi display, for usage on an offline cyberdeck system. Can be utilised on Windows, Linux and Mac however.

Useful for situations where the internet is unreachable and therefore and offline tile database needs to be used for mapping. The program will switch to this mode as soon as it detects that there is no internet connection.
## Features

- Light/dark/system mode toggle
- Fullscreen mode
- Cross platform
- Add markers to database
- Select marker overlay from mutiple databases through settings
- Set default database for markers to be added to
- Ability to delete databases through settings UI
- Included tool to download offline tiles off of either OSM or Google Sattelite Servers
- Automatic internet connection detection for setting tile database to offline

## Installation
**Either**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/offline-map-explorer.git](https://github.com/sbenf999/Ulysses-Mapping-Program.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python UMS/main.py
   ```
**or**
Download the latest [release](https://github.com/sbenf999/Ulysses-Mapping-Program/tags) 

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License - see 'LICENSE' file for details.



