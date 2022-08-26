# Solana NFT Crawler

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/rybakisa/solana_nft_crawler)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
![GitHub stars](https://img.shields.io/github/stars/rybakisa/solana_nft_crawler?style=social)
![GitHub forks](https://img.shields.io/github/forks/rybakisa/solana_nft_crawler?style=social)

![Solana NFT Crawler](https://github.com/rybakisa/solana_nft_crawler/blob/main/assets/logo.png)

App to parse NFT metadata from Solana blockchain.

App starts listening to block production in Solana blockchain from the N-th block and then syncs up to the current block number.
The script catches all NFT mints and print an array of NFT token ids and their metadata to the stdout.

The input is the start block number.
The output is printing all associated with this block NFT token mints and their content.

## Contributors
* [@rybakisa](https://github.com/rybakisa) 📖
