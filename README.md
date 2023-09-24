# Reddit Cryptocurrency Data Analysis Project

## Overview

This project is a personal learning exercise focused on web scraping and data visualization using Python. It aims to collect cryptocurrency data from Reddit's /r/cryptocurrency and CoinGecko's API, perform basic analysis, and visualize the results using Matplotlib. The script takes coins found in the top posts and plots the change in price percentage since the last time the script was run. This will create 2 files when run, one to store data gathered from CoinGecko and another to store data for the graph.

## Purpose

The primary purpose of this project is educational. It provides an opportunity to learn and practice web scraping techniques, data manipulation with Pandas, and data visualization with Matplotlib.

## Limitations

It's important to note the following limitations of this project:

1. **Data Plotting Method:** Does not account for data older than the previous time the script was run, such as data from 2+ runs ago

2. **Error Handling:** Error handling is minimal. In a production environment, more robust error handling and data validation would be necessary.

3. **Security:** This project does not cover security measures typically required in a production-level application, especially when interacting with external APIs.

## Future Enhancements

1. More robust data plotting method

2. More robust error handling

3. Security measure

## Dependencies

This project uses the following Python libraries:

- requests
- pandas
- Matplotlib
- pycoingecko

You can install these dependencies using `pip`:

  pip install requests pandas matplotlib pycoingecko

## Installation

1. Clone the repository:

     git clone https://github.com/dRussell68/Reddit-Crypto-Analysis.git

2. Navigate to the project directory:

      cd Reddit-Crypto-Analysis

3. Run the main script:

      python crypto_trends.py

## Acknowledgments

This project was created as part of a learning experience, and it may not be very useful for real-world applications. Thank you to the creators of requests, pandas, matplotlib, pycoingecko and reddit.
## License

This project is provided under the [MIT License](LICENSE). Feel free to use, modify, and distribute it for educational purposes or as a starting point for your own projects.
